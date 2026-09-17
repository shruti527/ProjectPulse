import streamlit as st
import json
import os
from datetime import datetime
from db import (
    init_db, save_extraction, get_all_tasks, get_tasks_by_owner,
    get_all_owners, update_task_status, get_all_decisions, search,
    get_conversation_by_id
)
from extraction import extract_from_conversation, validate_extraction
from sample_data import get_all_samples, get_sample_by_index

# Page configuration
st.set_page_config(
    page_title="ProjectPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Load cached results for fallback
CACHED_RESULTS = {}
if os.path.exists("cached_results.json"):
    with open("cached_results.json", "r") as f:
        CACHED_RESULTS = json.load(f)

# Streamlit session state for tracking extraction attempts
if 'last_extraction' not in st.session_state:
    st.session_state.last_extraction = None
if 'use_cache' not in st.session_state:
    st.session_state.use_cache = False


# CSS Styling
st.markdown("""
    <style>

    .main-header {
        font-size: 2.5em;
        color: #60a5fa;
        font-weight: bold;
        margin-bottom: 0.2em;
    }

    /* Summary */
    .summary-box {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-left: 5px solid #3b82f6;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Completed task */
    .task-complete {
        color: #4ade80;
        text-decoration: line-through;
    }

    /* Pending task */
    .task-pending {
        color: #f87171;
        font-weight: bold;
    }

    /* Decisions */
    .decision-box {
        background-color: #292524;
        color: #fef3c7;
        padding: 14px;
        border-left: 4px solid #facc15;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 16px;
        line-height: 1.5;
    }

    /* Pending approvals */
    .approval-box {
        background-color: #3f1d2e;
        color: #fecdd3;
        padding: 14px;
        border-left: 4px solid #fb7185;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 16px;
        line-height: 1.5;
    }

    </style>
""", unsafe_allow_html=True)


# Main title
st.markdown('<div class="main-header">📊 ProjectPulse</div>', unsafe_allow_html=True)
st.markdown("**Turn scattered project chatter into structured, searchable intelligence**")
st.divider()

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Process Conversation", "Task Board", "Project Memory"]
)

st.sidebar.divider()
st.sidebar.markdown("### About ProjectPulse")
st.sidebar.markdown("""
ProjectPulse extracts actionable project data from raw communication:
- **Summaries** of what was discussed
- **Tasks** with owners and deadlines
- **Decisions** made
- **Pending approvals** needed

All data is searchable and aggregated across conversations.
""")

# PAGE 1: Process Conversation
if page == "Process Conversation":
    st.header("📝 Process Conversation")
    st.markdown("Paste a conversation (chat, email thread, meeting transcript) and we'll extract structured project data.")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Quick Load")
        samples = get_all_samples()
        selected_sample = st.selectbox(
            "Load sample conversation:",
            range(len(samples)),
            format_func=lambda i: samples[i]['title'],
            key="sample_selector"
        )
        if st.button("📂 Load Sample"):
            st.session_state.conversation_text = get_sample_by_index(selected_sample)
            st.rerun()
    
    with col1:
        st.subheader("Paste Conversation")
    
    # Text area for conversation input
    if 'conversation_text' not in st.session_state:
        st.session_state.conversation_text = ""
    
    conversation_text = st.text_area(
        "Paste chat logs, meeting notes, or email thread here:",
        value=st.session_state.conversation_text,
        height=250,
        key="conv_input"
    )
    
    # Process button
    col1, col2 = st.columns([1, 4])
    with col1:
        process_btn = st.button("🔄 Process", use_container_width=True, type="primary")
    with col2:
        st.info("💡 Try loading a sample first to see how it works!")
    
    if process_btn:
        if not conversation_text.strip():
            st.error("Please paste a conversation or load a sample.")
        else:
            with st.spinner("🤖 Analyzing conversation..."):
                try:
                    # Try to extract from API
                    st.session_state.use_cache = False
                    extracted_data = extract_from_conversation(conversation_text)
                    
                except Exception as e:
                    st.warning(f"API call failed: {str(e)}. Using cached sample result for demo.")
                    st.session_state.use_cache = True
                    extracted_data = CACHED_RESULTS.get("sample_0", {
                        "summary": "Processing failed",
                        "tasks": [],
                        "decisions": [],
                        "pending_approvals": []
                    })
                
                # Validate extraction
                if validate_extraction(extracted_data):
                    st.session_state.last_extraction = extracted_data
                    st.success("✅ Extraction complete!")
                else:
                    st.error("Extraction failed validation. Please try again.")
    
    # Display extraction results if available
    if st.session_state.last_extraction:
        extracted_data = st.session_state.last_extraction
        
        if st.session_state.use_cache:
            st.info("📌 Showing cached demo result (API unavailable)")
        
        # Summary
        st.markdown("### 📋 Summary")
        st.markdown(f'<div class="summary-box">{extracted_data.get("summary", "No summary")}</div>', unsafe_allow_html=True)
        
        # Tasks
        st.markdown("### ✅ Tasks")
        tasks = extracted_data.get("tasks", [])
        if tasks:
            task_data = []
            for task in tasks:
                task_data.append({
                    "Task": task.get("task", ""),
                    "Owner": task.get("owner", "unassigned"),
                    "Deadline": task.get("deadline", "none")
                })
            st.dataframe(task_data, use_container_width=True, hide_index=True)
        else:
            st.info("No tasks identified.")
        
        # Decisions
        st.markdown("### 🎯 Decisions Made")
        decisions = extracted_data.get("decisions", [])
        if decisions:
            for decision in decisions:
                st.markdown(f'<div class="decision-box">✓ {decision}</div>', unsafe_allow_html=True)
        else:
            st.info("No decisions identified.")
        
        # Pending Approvals
        st.markdown("### ⏳ Pending Approvals")
        approvals = extracted_data.get("pending_approvals", [])
        if approvals:
            for approval in approvals:
                st.markdown(f'<div class="approval-box">⚠️ {approval}</div>', unsafe_allow_html=True)
        else:
            st.info("No pending approvals.")
        
        # Save to database
        if st.button("💾 Save to Project Memory", use_container_width=True):
            try:
                save_extraction(conversation_text, extracted_data)
                st.success("✅ Saved! You can now search and view this in Project Memory.")
                st.session_state.last_extraction = None
                st.session_state.conversation_text = ""
            except Exception as e:
                st.error(f"Failed to save: {str(e)}")

# PAGE 2: Task Board
elif page == "Task Board":
    st.header("📊 Task Board")
    st.markdown("View all extracted tasks across conversations, grouped by owner.")
    
    # Get unique owners
    owners = get_all_owners()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_owner = st.selectbox(
            "Filter by owner:",
            ["All Owners"] + owners,
            key="owner_filter"
        )
    with col2:
        st.empty()
    
    # Fetch tasks
    if selected_owner == "All Owners":
        all_tasks = get_all_tasks()
    else:
        all_tasks = get_tasks_by_owner(selected_owner)
    
    if all_tasks:
        st.markdown(f"**Found {len(all_tasks)} tasks**")
        
        # Create expandable task list
        for task_id, task_text, owner, deadline, status, created_at in all_tasks:
            with st.expander(f"📌 {task_text[:60]}... | {owner} | {deadline}"):
                st.markdown(f"**Task:** {task_text}")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Owner:** {owner}")
                with col2:
                    st.markdown(f"**Deadline:** {deadline}")
                with col3:
                    st.markdown(f"**Status:** {status}")
                
                st.markdown(f"**Added:** {created_at}")
                
                # Status update button
                new_status = st.radio(
                    "Update status:",
                    ["pending", "in-progress", "complete"],
                    key=f"status_{task_id}",
                    index=["pending", "in-progress", "complete"].index(status)
                )
                
                if new_status != status:
                    update_task_status(task_id, new_status)
                    st.success(f"✅ Status updated to '{new_status}'")
                    st.rerun()
    else:
        st.info("No tasks found. Process a conversation first!")

# PAGE 3: Project Memory / Search
elif page == "Project Memory":
    st.header("🔍 Project Memory")
    st.markdown("Search across all conversations, decisions, and tasks.")
    
    search_query = st.text_input(
        "Search keyword:",
        placeholder="e.g., 'deadline', 'approval', 'budget'...",
        key="search_input"
    )
    
    if search_query.strip():
        results = search(search_query)
        
        # Display results grouped by type
        result_count = (
            len(results['summaries']) + len(results['tasks']) + 
            len(results['decisions']) + len(results['approvals'])
        )
        st.markdown(f'**Found {result_count} results for "{search_query}"**')
        
        # Summaries
        if results['summaries']:
            st.markdown("### 📋 Matching Summaries")
            for conv_id, summary, created_at in results['summaries']:
                with st.expander(f"📅 {created_at}"):
                    st.markdown(summary)
        
        # Tasks
        if results['tasks']:
            st.markdown("### ✅ Matching Tasks")
            task_data = []
            for task, owner, deadline, created_at in results['tasks']:
                task_data.append({
                    "Task": task,
                    "Owner": owner,
                    "Deadline": deadline,
                    "Date": created_at
                })
            st.dataframe(task_data, use_container_width=True, hide_index=True)
        
        # Decisions
        if results['decisions']:
            st.markdown("### 🎯 Matching Decisions")
            for decision, created_at in results['decisions']:
                st.markdown(f'<div class="decision-box">**{created_at}:** {decision}</div>', unsafe_allow_html=True)
        
        # Approvals
        if results['approvals']:
            st.markdown("### ⏳ Matching Pending Approvals")
            for approval, created_at in results['approvals']:
                st.markdown(f'<div class="approval-box">**{created_at}:** {approval}</div>', unsafe_allow_html=True)
    else:
        # Show general stats if no search
        all_tasks = get_all_tasks()
        all_decisions = get_all_decisions()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(all_tasks))
        with col2:
            st.metric("Total Decisions", len(all_decisions))
        with col3:
            pending_tasks = len([t for t in all_tasks if t[4] == 'pending'])
            st.metric("Pending Tasks", pending_tasks)
        
        st.markdown("---")
        st.info("💡 Enter a keyword above to search across all project data!")
