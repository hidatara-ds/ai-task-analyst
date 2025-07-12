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
    # (Fungsi ini sama seperti sebelumnya)
    conn = get_db_conn()
    cur = conn.cursor()
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

    # === LANGKAH 1: ROUTING ===
    # Definisikan semua kemungkinan tindakan sebagai "tools" untuk router.
    routing_tools = [
        {
            "name": "search_activities",
            "description": "Gunakan untuk pencarian dan filter data aktivitas/task berdasarkan kriteria spesifik. Contoh: 'cari task yang dikerjakan Budi', 'tampilkan pekerjaan dengan status done', 'aktivitas bulan Januari', 'task proyek website'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {"type": "string", "description": "Nama user/karyawan yang mengerjakan task"},
                    "status": {"type": "string", "description": "Status pekerjaan: 'todo', 'in-progress', atau 'done'"},
                    "task_name": {"type": "string", "description": "Nama proyek atau task yang dicari"},
                    "bulan": {"type": "string", "description": "Bulan dalam format 2 digit ('01'-'12'), contoh: '01' untuk Januari"}
                }
            }
        },
        {
            "name": "get_user_list",
            "description": "Gunakan saat user meminta daftar semua user/karyawan/anggota tim. Contoh: 'siapa saja anggota tim?', 'tampilkan semua karyawan', 'daftar user'.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "analyze_full_data",
            "description": "Gunakan untuk analisis kompleks, perbandingan, statistik, atau ringkasan data. Contoh: 'siapa yang paling produktif?', 'berapa total task selesai bulan ini?', 'bandingkan performa tim', 'buat laporan bulanan', 'statistik pekerjaan'.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "general_conversation",
            "description": "Gunakan untuk percakapan umum, sapaan, pertanyaan tentang AI, atau permintaan di luar konteks data task. Contoh: 'halo', 'siapa kamu?', 'apa kabar?', 'terima kasih'.",
            "parameters": {"type": "object", "properties": {}}
        }
    ]

    router_prompt_system = """Anda adalah AI router yang cerdas untuk sistem manajemen task dan aktivitas.

TUGAS ANDA:
- Analisis permintaan user dengan teliti
- Pilih fungsi yang paling tepat untuk menjawab permintaan
- JANGAN menjawab pertanyaan user, cukup pilih fungsi yang benar

PANDUAN PEMILIHAN:
1. search_activities: Untuk pencarian/filter data berdasarkan kriteria spesifik
2. get_user_list: Untuk daftar user/karyawan
3. analyze_full_data: Untuk analisis kompleks, statistik, perbandingan
4. general_conversation: Untuk percakapan umum di luar konteks data

Pilih fungsi yang paling sesuai dengan maksud user."""
    
    llm_router_response = await call_llm_api(router_prompt_system, user_message, tools=routing_tools)
    
    # Ekstrak keputusan fungsi dari respons. Format ini mungkin berbeda tergantung API Anda.
    # Asumsi: response memiliki 'candidates'[0]['content']['parts'][0]['functionCall']
    try:
        function_call = llm_router_response['candidates'][0]['content']['parts'][0].get('functionCall')
        chosen_function = function_call['name']
        arguments = function_call.get('args', {})
        logger.info(f"Router decided to use function: '{chosen_function}' with args: {arguments}")
    except (KeyError, IndexError, TypeError):
        chosen_function = "general_conversation" # Fallback jika LLM tidak memilih fungsi
        arguments = {}
        logger.warning("Router failed to choose a function, falling back to general_conversation.")

    ai_response = "Maaf, terjadi kesalahan." # Default response

    # === LANGKAH 2: EKSEKUSI BERDASARKAN KEPUTUSAN ROUTER ===

    # --- PATH A: FUNCTION CALLING (untuk pencarian spesifik) ---
    if chosen_function in AVAILABLE_TOOLS:
        logger.info("Executing Path A: Function Calling")
        function_to_call = AVAILABLE_TOOLS[chosen_function]
        tool_result = function_to_call(**arguments)
        tool_result_str = json.dumps(tool_result, indent=2, ensure_ascii=False)
        
        summary_prompt_system = """Anda adalah asisten AI yang ahli dalam menyajikan data dengan jelas dan informatif.

TUGAS ANDA:
- Analisis data hasil dari database
- Sajikan informasi dalam format yang mudah dibaca dan dipahami
- Gunakan tabel HTML untuk data yang terstruktur
- Berikan konteks dan insight yang berguna

PANDUAN FORMAT:
- Jika data kosong: "Tidak ditemukan data yang sesuai dengan kriteria pencarian Anda."
- Jika ada data: Sajikan dalam tabel HTML dengan header yang jelas
- Tambahkan ringkasan singkat di awal jika relevan
- Gunakan bahasa yang ramah dan profesional

Jawab dalam bahasa Indonesia yang natural dan mudah dipahami."""
        
        final_response_json = await call_llm_api(summary_prompt_system, f"Data dari database:\n{tool_result_str}\n\nPertanyaan user: '{user_message}'\n\nSajikan data ini dengan baik dan jawab pertanyaan user.")
        ai_response = final_response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Saya mendapat data, tapi gagal merangkumnya.")

    # --- PATH B: CONTEXT STUFFING (untuk analisis kompleks) ---
    elif chosen_function == "analyze_full_data":
        logger.info("Executing Path B: Context Stuffing")
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.activity, t.task, u.nama, a.start_date, a.end_date, a.status
            FROM activity a JOIN task t ON a.task_id = t.id JOIN user_task ut ON t.id = ut.task_id JOIN user u ON ut.user_id = u.id
        """)
        activities = [dict(row) for row in cur.fetchall()]
        conn.close()
        
        activity_data_text = "\n".join([f"- Aktivitas: {row['activity']}, Proyek: {row['task']}, Oleh: {row['nama']}, Mulai: {row['start_date']}, Selesai: {row['end_date']}, Status: {row['status']}" for row in activities])
        
        analysis_prompt_system = f"""Anda adalah analis data AI yang ahli dalam menganalisis dan menyajikan informasi manajemen task dan aktivitas.

TANGGAL HARI INI: {datetime.now().strftime('%Y-%m-%d')}

TUGAS ANDA:
- Analisis data aktivitas dan task secara mendalam
- Berikan insight yang berguna dan actionable
- Sajikan perbandingan dan statistik dalam format yang jelas
- Gunakan tabel HTML untuk data terstruktur
- Berikan rekomendasi jika relevan

PANDUAN ANALISIS:
1. Hitung statistik: total task, task per status, task per user
2. Analisis performa: user paling produktif, task terlama/tercepat
3. Identifikasi tren: task per bulan, progress tim
4. Berikan insight: bottleneck, area improvement, pencapaian

FORMAT OUTPUT:
- Mulai dengan ringkasan eksekutif
- Sajikan data dalam tabel HTML yang rapi
- Berikan analisis mendalam
- Akhiri dengan insight atau rekomendasi

DATA LENGKAP DARI DATABASE:
{activity_data_text}

Analisis data ini dengan teliti dan berikan jawaban yang informatif dan berguna."""
        
        final_response_json = await call_llm_api(analysis_prompt_system, user_message)
        ai_response = final_response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Saya mendapat data untuk analisis, tapi gagal memprosesnya.")
        
    # --- PATH C: GENERAL CONVERSATION (untuk obrolan biasa) ---
    else: # Termasuk chosen_function == "general_conversation" atau fallback
        logger.info("Executing Path C: General Conversation")
        general_prompt_system = """Anda adalah asisten AI yang ramah dan membantu untuk sistem manajemen task dan aktivitas.

IDENTITAS ANDA:
- Nama: Task Analyst AI
- Peran: Asisten untuk membantu mengelola dan menganalisis data task/aktivitas
- Kepribadian: Ramah, profesional, dan selalu siap membantu

KEMAMPUAN ANDA:
- Mencari dan memfilter data aktivitas/task
- Menganalisis performa tim dan proyek
- Memberikan insight dan rekomendasi
- Menjawab pertanyaan umum dengan sopan

PANDUAN JAWABAN:
- Gunakan bahasa Indonesia yang natural dan ramah
- Berikan jawaban yang informatif dan bermanfaat
- Jika ditanya tentang kemampuan, jelaskan fitur-fitur yang tersedia
- Tunjukkan antusiasme untuk membantu

Contoh pertanyaan yang bisa Anda bantu:
- "Cari task yang dikerjakan Budi"
- "Siapa yang paling produktif?"
- "Tampilkan statistik pekerjaan bulan ini"
- "Halo, apa kabar?"""
        
        final_response_json = await call_llm_api(general_prompt_system, user_message)
        ai_response = final_response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Maaf, saya tidak bisa menjawab itu saat ini.")

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