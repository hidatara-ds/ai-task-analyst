import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger
import httpx
import time
from fastapi.staticfiles import StaticFiles
import re
from datetime import datetime

# Load env
load_dotenv()
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
    # Menggunakan row_factory agar bisa akses kolom via nama
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

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
    return [(row['user_message'], row['ai_response']) for row in rows]

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
    # Timeout dinaikkan untuk antisipasi LLM yang mungkin butuh waktu lebih lama
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(LLM_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Membersihkan ```html atau ``` dari jawaban AI
            response_text = data['candidates'][0]['content']['parts'][0]['text']
            return re.sub(r"```[a-zA-Z]*\s*([\s\S]*?)```", r"\1", response_text).strip()
        except Exception as e:
            logger.error(f'LLM API error: {e}')
            return 'Maaf, terjadi kesalahan pada AI.'

@app.post('/chat')
async def chat(request: Request):
    t0 = time.time()
    data = await request.json()
    user_message = data.get('message')
    session_id = data.get('session_id')

    if not user_message or not session_id:
        raise HTTPException(400, 'message and session_id required')

    logger.info(f"[CHAT] session={session_id} user_message={user_message}")

    history = get_history(session_id)
    context = "\n".join([f"User: {h[0]}\nAI: {h[1]}" for h in history])

    # --- PERUBAHAN UTAMA ---
    # Alih-alih mengandalkan function calling, kita ambil semua data relevan
    # dan memasukkannya langsung ke dalam prompt.
    conn = get_db_conn()
    cur = conn.cursor()

    # 1. Ambil semua data aktivitas dari database
    cur.execute("""
        SELECT a.activity, t.task, u.nama, a.start_date, a.end_date, a.status
        FROM activity a
        JOIN task t ON a.task_id = t.id
        JOIN user_task ut ON t.id = ut.task_id
        JOIN user u ON ut.user_id = u.id
        ORDER BY a.start_date
    """)
    activities = cur.fetchall()
    conn.close()

    # 2. Format data aktivitas menjadi teks yang mudah dibaca oleh AI
    activity_data_text = "\nBerikut adalah daftar semua aktivitas yang tercatat di database:\n"
    if activities:
        for row in activities:
            activity_data_text += f"- Aktivitas: {row['activity']}, Proyek: {row['task']}, Dikerjakan oleh: {row['nama']}, Mulai: {row['start_date']}, Selesai: {row['end_date']}, Status: {row['status']}\n"
    else:
        activity_data_text = "Tidak ada data aktivitas di dalam database."

    # 3. Buat prompt baru yang lebih sederhana
    # Prompt ini memberikan semua data ke AI dan memintanya untuk menjawab berdasarkan itu.
    prompt = f"""
Kamu adalah asisten AI yang cerdas dan membantu. Jawab pertanyaan user berdasarkan histori percakapan dan data yang diberikan di bawah ini.
Saat ini adalah tanggal: {datetime.now().strftime('%Y-%m-%d')}

Histori Percakapan:
{context}

Data dari Database:
{activity_data_text}

ATURAN:
1. Analisis pertanyaan user dan jawab menggunakan data yang telah disediakan.
2. Jika user meminta ringkasan (summary) atau daftar, selalu sajikan dalam format tabel HTML yang rapi dan mudah dibaca (gunakan tag <table>, <thead>, <tbody>, <tr>, <th>, <td>).
3. Jangan pernah menyertakan ```html dalam jawabanmu. Langsung berikan kode HTML-nya.
4. Jika data yang diminta user tidak ada, informasikan dengan sopan.

User: {user_message}
AI:
"""

    ai_response = await ask_llm(prompt)

    save_history(session_id, user_message, ai_response)
    logger.info(f"[RESPONSE] session={session_id} ai_response={ai_response[:200]}...")
    logger.info(f"[LATENCY] {time.time() - t0:.2f}s")

    updated_history = get_history(session_id)

    return JSONResponse({
        'answer': ai_response,
        'history': updated_history
    })

@app.get('/history/{session_id}')
def history(session_id: str):
    logger.info(f"[HISTORY] session={session_id}")
    return {'history': get_history(session_id)}