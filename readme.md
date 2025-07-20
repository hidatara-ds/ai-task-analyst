# 🚀 AI Task Analyst Web

A smart AI-powered web app for analyzing and managing project/task data, featuring advanced function calling and data analysis. Enjoy an AI chat that remembers previous conversations and delivers actionable insights.

---

## 📊 **Flow Diagram Example**

![Diagram Flow](diagram-flow.png)

---

## 🌟 **Key Features**
- 🤖 **Intelligent AI Chat** with session-based memory
- 🔍 **Function Calling** for precise data search and filtering
- 📈 **Advanced Data Analysis** with statistics and insights
- 💬 **Automatic Conversation Routing** based on question type
- 📱 **Responsive Frontend** built with Vue.js
- 📝 **Comprehensive Logging** for monitoring and debugging
- 🎯 **Optimized Prompt Engineering** for best results

---

## 🧠 **AI Capabilities**

### 1. **Data Search & Filtering**
- Search tasks by user/employee name
- Filter by status (todo, in-progress, done)
- Search by project/task name
- Filter by specific month

### 2. **Complex Analysis**
- Team and individual performance statistics
- Productivity comparison between users
- Monthly work trend analysis
- Identify bottlenecks and improvement areas
- Executive reports with actionable insights

### 3. **User Management**
- Complete team member list
- Detailed user and task assignment info

### 4. **Conversational AI**
- Natural conversation in English (and Indonesian)
- Explains system features and capabilities
- General help and usage guidance

---

## 🗂️ **Project Structure**
```text
ai-task-analyst/
│
├── app.py                # FastAPI backend with function calling
├── requirements.txt      # Python dependencies
├── .env                  # LLM API key
├── database_task.sql     # SQL schema + sample data
├── static/
│   └── index.html        # Responsive chat frontend
├── tasks.db              # (auto-generated) SQLite DB
└── app.log               # Log file for monitoring
```

---

## 🏗️ **System Architecture**

### 🤖 **Routing Intelligence**
The system uses a smart AI router to select the right function:

1. **search_activities** - Search and filter data
2. **get_user_list** - List users/employees
3. **analyze_full_data** - Complex analysis and statistics
4. **general_conversation** - General chat

### 🔗 **Function Calling**
- `search_activities(user_name, status, task_name, month)`
- `get_user_list()`
- Context stuffing for complex analysis
- General conversation for common questions

---

## ⚡ **Installation & Setup**

### 1. **Clone the repo & enter the folder**
```bash
git clone <repo-url>
cd ai-task-analyst
```

### 2. **Create & activate environment (optional but recommended)**
```bash
# Using conda
conda create -n ai-task python=3.10
conda activate ai-task

# Or with venv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Prepare the `.env` file**
Create a `.env` file in the root directory:
```env
LLM_API_KEY=your_google_ai_studio_api_key
LLM_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=your_google_ai_studio_api_key
```
Replace with your actual API key and endpoint as needed.

### 5. **Ensure `database_task.sql` contains CREATE TABLE + INSERT**
Already included in the repo, but make sure the top of the file looks like:
```sql
CREATE TABLE IF NOT EXISTS user (...);
CREATE TABLE IF NOT EXISTS task (...);
CREATE TABLE IF NOT EXISTS activity (...);
-- then INSERT ...
```

---

## 🚦 **Running the Application**

### 1. **Start the backend**
```bash
uvicorn app:app --reload
```
- The server will auto-create `tasks.db` from `database_task.sql` if it doesn't exist.
- Logs are written to `app.log` for monitoring.

### 2. **Access the frontend**
Open in your browser:
```
http://127.0.0.1:8000/static/index.html
```

---

## 💡 **Usage Examples**

### **Data Search**
- "Find tasks assigned to Budi"
- "Show tasks with status done"
- "Activities in January"
- "Website project tasks"

### **Complex Analysis**
- "Who is the most productive?"
- "How many tasks were completed this month?"
- "Compare team performance"
- "Generate monthly report"
- "Work statistics"

### **User Management**
- "Who are the team members?"
- "Show all employees"
- "User list"

### **General Conversation**
- "Hello, how are you?"
- "What can you do?"
- "Thank you"

---

## 🛠️ **Troubleshooting & Error Handling**

### **Error: `sqlite3.OperationalError: no such table: user`**
**Cause:**
The `tasks.db` file exists but is empty or has the wrong schema.

**Solution:**
1. **Delete the `tasks.db`** file in the project folder.
2. **Restart the server** (`uvicorn app:app --reload`).
   - The server will automatically recreate the database from `database_task.sql`.

### **Error: `Import "fastapi" could not be resolved`**
- Make sure your environment is active.
- Run: `pip install fastapi uvicorn`

### **Error: `uvicorn` not found**
- Run: `pip install uvicorn`

### **Error: LLM not responding/API error**
- Ensure `.env` is correct and API key is active.
- Check `app.log` for error details.
- Make sure the API response format matches expectations.

### **Error: 404 Not Found for endpoint**
- Use the `/chat` endpoint (not `/chat_stream`).
- Make sure the frontend is updated to use the correct endpoint.

---

## 🧑‍💻 **Technical Features**

### **Enhanced Prompts**
- **Router Prompt:** Smart AI for function selection
- **Summary Prompt:** Informative and structured data presentation
- **Analysis Prompt:** Deep analysis with actionable insights
- **General Prompt:** Friendly, natural conversation

### **Response Format**
- HTML tables for structured data
- Markdown support for formatting
- Code blocks for technical output
- Responsive design for mobile

### **Performance**
- 45-second timeout for API calls
- Detailed logging for monitoring
- Robust error handling
- Efficient session management

---

## 📚 **Usage Notes**
- All data is sourced from the SQLite database (`tasks.db`).
- To update data, edit `database_task.sql`, delete `tasks.db`, and restart the server.
- Chat history per session is stored in the database.
- Detailed logs are available in `app.log` for debugging.

---

## 🚀 **Further Development**
- For large datasets, limit data sent to the LLM.
- Switch LLM to OpenAI, Ollama, etc. by updating `.env`.
- For deployment, use a production server (e.g., `uvicorn app:app --host 0.0.0.0 --port 80`).
- Add authentication and authorization as needed.
- Implement streaming responses for better UX.

---

## 📝 **License**
Free to use for learning and development purposes.

---

**If you encounter other errors, check `app.log` or ask here!**