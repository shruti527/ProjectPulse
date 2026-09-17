import sqlite3
from datetime import datetime
import os

DB_PATH = "projectpulse.db"

def init_db():
    """Initialize database with schema if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create conversations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tasks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            task TEXT,
            owner TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    ''')
    
    # Create decisions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            decision_text TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    ''')
    
    # Create pending_approvals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS pending_approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            item_text TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_extraction(raw_text, parsed_json):
    """Save conversation and extracted data to database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Insert conversation
    c.execute(
        'INSERT INTO conversations (raw_text, summary) VALUES (?, ?)',
        (raw_text, parsed_json.get('summary', ''))
    )
    conversation_id = c.lastrowid
    
    # Insert tasks
    for task_data in parsed_json.get('tasks', []):
        c.execute(
            'INSERT INTO tasks (conversation_id, task, owner, deadline) VALUES (?, ?, ?, ?)',
            (conversation_id, task_data.get('task', ''), task_data.get('owner', 'unassigned'), task_data.get('deadline', 'none'))
        )
    
    # Insert decisions
    for decision in parsed_json.get('decisions', []):
        c.execute(
            'INSERT INTO decisions (conversation_id, decision_text) VALUES (?, ?)',
            (conversation_id, decision)
        )
    
    # Insert pending approvals
    for approval in parsed_json.get('pending_approvals', []):
        c.execute(
            'INSERT INTO pending_approvals (conversation_id, item_text) VALUES (?, ?)',
            (conversation_id, approval)
        )
    
    conn.commit()
    conn.close()
    return conversation_id

def get_all_tasks():
    """Retrieve all tasks from database with conversation date."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT t.id, t.task, t.owner, t.deadline, t.status, c.created_at
        FROM tasks t
        JOIN conversations c ON t.conversation_id = c.id
        ORDER BY c.created_at DESC
    ''')
    results = c.fetchall()
    conn.close()
    return results

def get_tasks_by_owner(owner):
    """Retrieve tasks filtered by owner."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT t.id, t.task, t.owner, t.deadline, t.status, c.created_at
        FROM tasks t
        JOIN conversations c ON t.conversation_id = c.id
        WHERE t.owner = ?
        ORDER BY c.created_at DESC
    ''', (owner,))
    results = c.fetchall()
    conn.close()
    return results

def get_all_owners():
    """Get list of unique task owners."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT DISTINCT owner FROM tasks WHERE owner != "unassigned" ORDER BY owner')
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]

def update_task_status(task_id, status):
    """Update task status."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

def get_all_decisions():
    """Retrieve all decisions from database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT d.decision_text, c.created_at
        FROM decisions d
        JOIN conversations c ON d.conversation_id = c.id
        ORDER BY c.created_at DESC
    ''')
    results = c.fetchall()
    conn.close()
    return results

def search(keyword):
    """Search across summaries, tasks, decisions by keyword."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    search_term = f"%{keyword}%"
    
    results = {
        'summaries': [],
        'tasks': [],
        'decisions': [],
        'approvals': []
    }
    
    # Search summaries
    c.execute(
        'SELECT id, summary, created_at FROM conversations WHERE summary LIKE ? ORDER BY created_at DESC',
        (search_term,)
    )
    results['summaries'] = c.fetchall()
    
    # Search tasks
    c.execute(
        'SELECT t.task, t.owner, t.deadline, c.created_at FROM tasks t JOIN conversations c ON t.conversation_id = c.id WHERE t.task LIKE ? ORDER BY c.created_at DESC',
        (search_term,)
    )
    results['tasks'] = c.fetchall()
    
    # Search decisions
    c.execute(
        'SELECT d.decision_text, c.created_at FROM decisions d JOIN conversations c ON d.conversation_id = c.id WHERE d.decision_text LIKE ? ORDER BY c.created_at DESC',
        (search_term,)
    )
    results['decisions'] = c.fetchall()
    
    # Search pending approvals
    c.execute(
        'SELECT p.item_text, c.created_at FROM pending_approvals p JOIN conversations c ON p.conversation_id = c.id WHERE p.item_text LIKE ? ORDER BY c.created_at DESC',
        (search_term,)
    )
    results['approvals'] = c.fetchall()
    
    conn.close()
    return results

def get_conversation_by_id(conv_id):
    """Get full conversation text by ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT raw_text, summary, created_at FROM conversations WHERE id = ?', (conv_id,))
    result = c.fetchone()
    conn.close()
    return result
