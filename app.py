import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger
import httpx
import time
import json
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import Optional, List, Dict, Any

# --- Konfigurasi dan Inisialisasi (Sama seperti sebelumnya) ---
load_dotenv()
LLM_API_URL = os.getenv('LLM_API_URL')
DB_FILE = 'tasks.db'
SQL_INIT_FILE = 'database_task.sql'

logger.add('app.log', rotation='1 MB')
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
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_history(session_id: str) -> List[tuple]:
    # (Fungsi ini sama seperti sebelumnya)
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


def save_history(session_id: str, user_message: str, ai_response: str):
    conn = get_db_conn()
    cur = conn.cursor()
    # Buat tabel chat_history jika belum ada
    cur.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_message TEXT,
        ai_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    cur.execute('''INSERT INTO chat_history (session_id, user_message, ai_response) VALUES (?, ?, ?)''',
                (session_id, user_message, ai_response))
    conn.commit()
    conn.close()

# --- Definisi Fungsi "Alat" (Sama seperti sebelumnya) ---

def search_activities(user_name: Optional[str] = None, status: Optional[str] = None, task_name: Optional[str] = None, bulan: Optional[str] = None) -> List[Dict[str, Any]]:
    """Mencari aktivitas dalam database berdasarkan nama user, status, nama proyek, dan/atau bulan."""
    logger.info(f"Executing search_activities(user_name={user_name}, status={status}, task_name={task_name}, bulan={bulan})")
    conn = get_db_conn()
    query = """
        SELECT a.activity, t.task, u.nama, a.start_date, a.end_date, a.status
        FROM activity a
        JOIN task t ON a.task_id = t.id
        JOIN user_task ut ON t.id = ut.task_id
        JOIN user u ON ut.user_id = u.id
        WHERE 1=1
    """
    params = []
    if user_name:
        query += " AND u.nama LIKE ?"
        params.append(f"%{user_name}%")
    if status:
        query += " AND a.status = ?"
        params.append(status)
    if task_name:
        query += " AND t.task LIKE ?"
        params.append(f"%{task_name}%")
    if bulan:
        query += " AND (strftime('%m', a.start_date) = ? OR strftime('%m', a.end_date) = ?)"
        params.extend([bulan, bulan])
    cur = conn.cursor()
    cur.execute(query, tuple(params))
    activities = [dict(row) for row in cur.fetchall()]
    conn.close()
    return activities

def get_user_list() -> List[str]:
    """Mengambil daftar semua nama user yang tercatat di dalam sistem."""
    logger.info("Executing get_user_list()")
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT nama FROM user")
    users = [row['nama'] for row in cur.fetchall()]
    conn.close()
    return users

# --- Mapping Nama Fungsi ke Fungsi Python ---
AVAILABLE_TOOLS = {
    "search_activities": search_activities,
    "get_user_list": get_user_list,
}

# --- Panggilan LLM yang disederhanakan ---
async def call_llm_api(system_prompt: str, user_prompt: str, tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """Fungsi generik untuk memanggil API LLM."""
    # Di sini, Anda akan menggunakan format yang dibutuhkan oleh API LLM Anda
    # Contoh ini menggunakan format umum seperti Gemini API
    full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAI:"
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }
    # Jika ada tools, tambahkan ke payload
    if tools:
        # Sesuaikan format ini dengan API Anda (misal: Gemini, OpenAI)
        payload["tools"] = [{"function_declarations": tools}]

    headers = {'Content-Type': 'application/json'}
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(LLM_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        return {"error": "Maaf, terjadi kesalahan pada AI."}

# --- Endpoint Chat dengan Logika Hibrida ---
@app.post('/chat')
async def chat(request: Request):
    t0 = time.time()
    data = await request.json()
    user_message = data.get('message')
    session_id = data.get('session_id')

    if not user_message or not session_id:
        raise HTTPException(400, 'message and session_id required')

    logger.info(f"[CHAT] session={session_id} user_message='{user_message}'")

    # === LANGKAH 1: AMBIL HISTORY UNTUK CONTEXT ===
    chat_history = get_history(session_id)
    context_messages = []
    
    # Ambil 3 pesan terakhir untuk context
    for user_msg, ai_msg in chat_history[-3:]:
        context_messages.append(f"User: {user_msg}")
        context_messages.append(f"AI: {ai_msg}")
    
    context_text = "\n".join(context_messages) if context_messages else ""

    # === LANGKAH 2: SMART ROUTING DENGAN CONTEXT ===
    routing_prompt = f"""Anda adalah AI router yang cerdas. Analisis permintaan user dan context percakapan sebelumnya.

CONTEXT PERCAKAPAN SEBELUMNYA:
{context_text}

PERTANYAAN USER SAAT INI: {user_message}

TUGAS ANDA:
Pilih fungsi yang paling tepat berdasarkan pertanyaan user dan context.

FUNGSI YANG TERSEDIA:
1. search_activities - Untuk pencarian task/aktivitas berdasarkan nama user, status, proyek, bulan
2. get_user_list - Untuk daftar semua user/karyawan
3. analyze_full_data - Untuk analisis kompleks, statistik, perbandingan performa
4. general_conversation - Untuk percakapan umum, sapaan, bantuan

PANDUAN PEMILIHAN:
- Jika user minta data user/task → pilih fungsi yang sesuai
- Jika user minta analisis/perbandingan → analyze_full_data
- Jika user hanya sapaan/pertanyaan umum → general_conversation
- Perhatikan context! Jika user melanjutkan percakapan sebelumnya, gunakan fungsi yang sesuai

JAWAB HANYA: nama_fungsi (tanpa tanda kutip atau penjelasan lain)"""

    # Panggil LLM untuk routing
    routing_response = await call_llm_api(routing_prompt, user_message)
    
    try:
        chosen_function = routing_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip().lower()
        logger.info(f"Router chose: '{chosen_function}'")
    except:
        chosen_function = "general_conversation"
        logger.warning("Router failed, using general_conversation")

    # === LANGKAH 3: EKSEKUSI BERDASARKAN FUNGSI ===
    ai_response = "Maaf, terjadi kesalahan."

    if "search_activities" in chosen_function:
        logger.info("Executing search_activities")
        
        # Extract parameters from user message
        search_prompt = f"""Extract search parameters from user message.

USER MESSAGE: {user_message}
CONTEXT: {context_text}

Extract these parameters (if mentioned):
- user_name: nama user/karyawan
- status: status task (todo, in-progress, done, selesai)
- task_name: nama proyek/task
- bulan: bulan (01-12)

Return as JSON only, example: {{"user_name": "andi", "status": "done"}}
If not found, use null."""

        param_response = await call_llm_api(search_prompt, "")
        try:
            import re
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', param_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}'))
            if json_match:
                params = json.loads(json_match.group())
            else:
                params = {}
        except:
            params = {}
        
        # Execute search
        result = search_activities(
            user_name=params.get('user_name'),
            status=params.get('status'),
            task_name=params.get('task_name'),
            bulan=params.get('bulan')
        )
        
        # Format response
        if result:
            response_prompt = f"""Sajikan hasil pencarian dengan format yang baik.

DATA HASIL PENCARIAN:
{json.dumps(result, indent=2, ensure_ascii=False)}

PERTANYAAN USER: {user_message}
CONTEXT: {context_text}

Sajikan dalam format tabel HTML yang rapi dengan kolom: Aktivitas, Proyek, Oleh, Mulai, Selesai, Status.
Tambahkan ringkasan singkat di awal."""
        else:
            response_prompt = f"""User tidak menemukan data yang sesuai.

PERTANYAAN USER: {user_message}
CONTEXT: {context_text}

Berikan jawaban yang ramah dan sarankan format pencarian yang lebih spesifik."""

        final_response = await call_llm_api(response_prompt, "")
        ai_response = final_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Tidak ditemukan data yang sesuai.")

    elif "get_user_list" in chosen_function:
        logger.info("Executing get_user_list")
        users = get_user_list()
        
        response_prompt = f"""Sajikan daftar user dengan format yang baik.

DAFTAR USER: {json.dumps(users, ensure_ascii=False)}

PERTANYAAN USER: {user_message}
CONTEXT: {context_text}

Sajikan dalam format tabel HTML dengan kolom: No, Nama User.
Tambahkan ringkasan jumlah user di awal."""

        final_response = await call_llm_api(response_prompt, "")
        ai_response = final_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Berikut daftar user yang tersedia.")

    elif "analyze_full_data" in chosen_function:
        logger.info("Executing analyze_full_data")
        
        # Get all data
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.activity, t.task, u.nama, a.start_date, a.end_date, a.status
            FROM activity a JOIN task t ON a.task_id = t.id JOIN user_task ut ON t.id = ut.task_id JOIN user u ON ut.user_id = u.id
        """)
        activities = [dict(row) for row in cur.fetchall()]
        conn.close()
        
        analysis_prompt = f"""Analisis data dan jawab pertanyaan user dengan insight yang berguna.

DATA LENGKAP:
{json.dumps(activities, indent=2, ensure_ascii=False)}

PERTANYAAN USER: {user_message}
CONTEXT: {context_text}
TANGGAL HARI INI: {datetime.now().strftime('%Y-%m-%d')}

Lakukan analisis mendalam:
1. Hitung statistik yang relevan
2. Bandingkan performa jika diminta
3. Identifikasi tren dan insight
4. Sajikan dalam format tabel HTML jika ada data terstruktur
5. Berikan rekomendasi jika relevan

Jawab dengan bahasa Indonesia yang natural dan informatif."""

        final_response = await call_llm_api(analysis_prompt, "")
        ai_response = final_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Saya mendapat data untuk analisis, tapi gagal memprosesnya.")

    else:  # general_conversation
        logger.info("Executing general_conversation")
        
        general_prompt = f"""Anda adalah Task Analyst AI yang ramah dan membantu.

CONTEXT PERCAKAPAN SEBELUMNYA:
{context_text}

PERTANYAAN USER SAAT INI: {user_message}

IDENTITAS ANDA:
- Nama: Task Analyst AI
- Peran: Asisten untuk manajemen task dan aktivitas
- Kepribadian: Ramah, profesional, dan selalu siap membantu

KEMAMPUAN ANDA:
- Mencari dan memfilter data aktivitas/task
- Menganalisis performa tim dan proyek
- Memberikan insight dan rekomendasi
- Menjawab pertanyaan umum dengan sopan

PANDUAN JAWABAN:
- Gunakan bahasa Indonesia yang natural dan ramah
- Perhatikan context percakapan sebelumnya
- Jika user menanyakan tentang data, arahkan ke format yang tepat
- JANGAN bilang "saya perlu akses data"
- Berikan contoh pertanyaan yang tepat jika diperlukan

Contoh format pertanyaan yang bisa Anda sarankan:
- "Cari task yang dikerjakan [nama]"
- "Sebutkan semua user"
- "Siapa yang paling produktif?"
- "Tampilkan statistik pekerjaan bulan ini"

Jawab dengan ramah dan bermanfaat."""

        final_response = await call_llm_api(general_prompt, "")
        ai_response = final_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Maaf, saya tidak bisa menjawab itu saat ini.")

    # Simpan histori dan kirim respons
    save_history(session_id, user_message, ai_response)
    logger.info(f"[RESPONSE] session={session_id} ai_response='{ai_response[:200]}...'")
    logger.info(f"[LATENCY] {time.time() - t0:.2f}s")
    
    updated_history = get_history(session_id)
    return JSONResponse({'answer': ai_response, 'history': updated_history})

@app.get('/history/{session_id}')
def history(session_id: str):
    logger.info(f"[HISTORY] session={session_id}")
    return JSONResponse({'history': get_history(session_id)})