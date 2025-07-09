import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger
import httpx
import time
from fastapi.staticfiles import StaticFiles

# Load env
load_dotenv()
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_URL = os.getenv('LLM_API_URL')
DB_FILE = 'tasks.db'
SQL_INIT_FILE = 'database_task.sql'

# Logging setup
logger.add('app.log', rotation='1 MB')

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def init_db():
    if not os.path.exists(DB_FILE):
        logger.info('Database not found, initializing from SQL...')
        conn = sqlite3.connect(DB_FILE)
        with open(SQL_INIT_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()
        logger.info('Database initialized.')
    else:
        logger.info('Database found, skipping init.')

init_db()

def get_db_conn():
    return sqlite3.connect(DB_FILE)

def get_history(session_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_message TEXT,
        ai_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    cur.execute('SELECT user_message, ai_response FROM chat_history WHERE session_id = ? ORDER BY id', (session_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def save_history(session_id, user_message, ai_response):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''INSERT INTO chat_history (session_id, user_message, ai_response) VALUES (?, ?, ?)''',
                (session_id, user_message, ai_response))
    conn.commit()
    conn.close()

async def ask_llm(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(LLM_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Gemini response structure
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logger.error(f'LLM API error: {e}')
            return 'Maaf, terjadi kesalahan pada AI.'

def get_all_data_as_text():
    conn = get_db_conn()
    cur = conn.cursor()
    # Users
    cur.execute("SELECT id, nama FROM user")
    users = "\n".join([f"- {row[0]}, {row[1]}" for row in cur.fetchall()])
    # Tasks
    cur.execute("SELECT id, task, start_date, end_date FROM task")
    tasks = "\n".join([f"- {row[0]}, {row[1]}, {row[2]}, {row[3]}" for row in cur.fetchall()])
    # Activities
    cur.execute("SELECT id, activity, task_id, start_date, end_date, status FROM activity")
    activities = "\n".join([f"- {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}" for row in cur.fetchall()])
    conn.close()
    return f"Users:\n{users}\n\nTasks:\n{tasks}\n\nActivities:\n{activities}"

@app.post('/chat')
async def chat(request: Request):
    t0 = time.time()
    data = await request.json()
    user_message = data.get('message')
    session_id = data.get('session_id')
    logger.info(f"[CHAT] session={session_id} user_message={user_message}")
    if not user_message or not session_id:
        raise HTTPException(400, 'message and session_id required')
    # Ambil history
    history = get_history(session_id)
    # Compose prompt
    context = "".join([f"User: {h[0]}\nAI: {h[1]}\n" for h in history])
    data_text = get_all_data_as_text()
    prompt = f"""
Gunakan data berikut untuk menjawab pertanyaan user secara spesifik dan ringkas.

{data_text}

User: {user_message}
AI:
"""
    # Kirim ke LLM
    ai_response = await ask_llm(prompt)
    # Simpan history
    save_history(session_id, user_message, ai_response)
    logger.info(f"[RESPONSE] session={session_id} ai_response={ai_response}")
    t1 = time.time()
    logger.info(f"[LATENCY] {t1-t0:.2f}s")
    return JSONResponse({
        'answer': ai_response,
        'history': get_history(session_id)
    })

@app.get('/history/{session_id}')
def history(session_id: str):
    logger.info(f"[HISTORY] session={session_id}")
    return {'history': get_history(session_id)}
