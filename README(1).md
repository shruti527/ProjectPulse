# 🚀 ProjectPulse

## AI-Powered Project Communication Intelligence

> Turn scattered project conversations into structured, searchable project intelligence.

ProjectPulse is a hackathon prototype that uses **Google Gemini AI**, **Streamlit**, and **SQLite** to convert unstructured project communication into actionable information.

It extracts:
- 📝 Conversation summaries
- ✅ Tasks and action items
- 👤 Task owners
- 📅 Deadlines
- 🎯 Decisions made
- ⏳ Pending approvals and blockers

## 🎯 Problem

Project teams communicate through chats, meetings, and emails. Important tasks and decisions often get buried, resulting in missed deadlines, unclear ownership, and delayed approvals.

## 💡 Solution

```text
Raw Conversation
       ↓
Google Gemini AI
       ↓
Structured Extraction
       ↓
Summary | Tasks | Decisions | Approvals
       ↓
SQLite Project Memory
       ↓
Task Board + Search
```

## ✨ Features

### 📝 Process Conversation
Paste chat messages, meeting notes, or email-style discussions. Gemini extracts structured project information.

### 📊 Task Board
- View extracted tasks
- See owners and deadlines
- Filter tasks by owner
- Update task status: Pending, In Progress, Complete

### 🔍 Project Memory
Search stored information across summaries, tasks, decisions, and pending approvals.

### 🧠 Structured AI Extraction
Gemini returns structured JSON containing summary, tasks, decisions, and pending approvals.

### 🛡️ Error Handling
The application handles missing configuration, API failures, invalid responses, and database errors with user-friendly messages.

> AI-generated results should be reviewed by a human before being treated as confirmed commitments.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Google Gemini API | AI extraction |
| Google GenAI SDK | Gemini integration |
| SQLite | Local database |
| python-dotenv | Environment configuration |
| Git/GitHub | Version control |

## 📁 Project Structure

```text
ProjectPulse/
├── app.py                 # Main Streamlit interface
├── extraction.py          # Gemini integration and AI extraction
├── db.py                  # SQLite database operations
├── sample_data.py         # Sample project conversations
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

## ⚙️ Installation

### Prerequisites

- Python 3.9+
- Git
- Google Gemini API key

Get an API key from: https://aistudio.google.com/apikey

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ProjectPulse
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit your real `.env` file or API key.

### 5. Run the application

```bash
streamlit run app.py
```

Open: `http://localhost:8501`

## 🧪 How to Use

1. Open **Process Conversation**.
2. Paste a project conversation or load a sample.
3. Click **Process**.
4. Review the summary, tasks, decisions, and pending approvals.
5. Save the results to Project Memory.
6. Use Task Board to manage tasks.
7. Use Project Memory to search stored information.

## 🎬 Hackathon Demo Flow

1. Explain the problem of scattered project communication.
2. Load a sample conversation.
3. Process it with Gemini.
4. Show the extracted summary, tasks, decisions, and approvals.
5. Open the Task Board.
6. Search for `deadline`, `approval`, or `budget`.

### Project Pitch

> ProjectPulse turns scattered project communication into a structured, searchable source of truth—helping teams understand what was discussed, what was decided, and what needs to happen next.

## 🏗️ Data Model

The application stores:

- Conversations and summaries
- Tasks with owners, deadlines, and statuses
- Decisions linked to conversations
- Pending approvals linked to conversations

SQLite is used for simple local storage without requiring a separate database server.

## 🔐 Security and Privacy

- Store API keys in environment variables.
- Keep `.env` excluded through `.gitignore`.
- Do not upload confidential conversations.
- Review AI-generated outputs.
- Do not commit local databases or virtual environments.

## 🚧 Current Limitations

- Results depend on the quality of the input text.
- AI outputs require human verification.
- Local SQLite storage is designed for a prototype.
- Search currently uses keyword matching.
- Gemini API limits depend on the selected model and account.

## 🔮 Future Scope

- Slack, Teams, and email integration
- Semantic search with embeddings
- Automatic deadline reminders
- Multi-project workspaces
- Authentication and role-based access
- Cloud database support
- Analytics and risk detection
- Calendar and project-management integrations

## 📌 Project Status

**Status:** Hackathon Prototype

The current version demonstrates AI extraction, task management, decision tracking, pending approval detection, local project memory, and keyword search.

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application.
5. Submit a pull request.

## 📄 License

Add a license appropriate for your project. The MIT License may be used if you want to allow broad reuse.

## 👩‍💻 Author

**Shruti Chedge**

Built as a hackathon project exploring practical Generative AI applications for project productivity.
