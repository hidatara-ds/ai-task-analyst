# AI Task Analyst Web

Web AI cerdas untuk menganalisis dan mengelola data tugas/proyek dengan kemampuan function calling dan analisis data yang advanced. Chat AI yang mengingat percakapan sebelumnya dan memberikan insight yang berguna.

---

## **Contoh Diagram Flow**

![Diagram Flow](diagram-flow.png)

---

## **Fitur Utama**
- 🤖 **AI Chat Cerdas** dengan session-based memory
- 🔍 **Function Calling** untuk pencarian dan filter data yang presisi
- 📊 **Analisis Data Kompleks** dengan statistik dan insight
- 💬 **Conversation Routing** otomatis berdasarkan jenis pertanyaan
- 📱 **Frontend Responsive** dengan Vue.js
- 📝 **Logging Lengkap** untuk monitoring dan debugging
- 🎯 **Prompt Engineering** yang dioptimalkan untuk hasil terbaik

---

## **Kemampuan AI**

### **1. Pencarian & Filter Data**
- Mencari task berdasarkan nama user/karyawan
- Filter berdasarkan status (todo, in-progress, done)
- Pencarian berdasarkan nama proyek/task
- Filter berdasarkan bulan tertentu

### **2. Analisis Kompleks**
- Statistik performa tim dan individu
- Perbandingan produktivitas antar user
- Analisis tren pekerjaan per bulan
- Identifikasi bottleneck dan area improvement
- Laporan eksekutif dengan insight actionable

### **3. Manajemen User**
- Daftar lengkap anggota tim
- Informasi detail user dan task assignment

### **4. Conversational AI**
- Percakapan natural dalam bahasa Indonesia
- Penjelasan kemampuan dan fitur sistem
- Bantuan umum dan panduan penggunaan

---

## **Struktur Project**
```
ai-task-analyst/
│
├── app.py                # Backend FastAPI dengan function calling
├── requirements.txt      # Python dependencies
├── .env                  # API key LLM
├── database_task.sql     # SQL schema + sample data
├── static/
│   └── index.html        # Frontend chat responsive
├── tasks.db              # (auto-generated) SQLite DB
└── app.log               # Log file untuk monitoring
```

---

## **Arsitektur Sistem**

### **Routing Intelligence**
Sistem menggunakan AI router yang cerdas untuk memilih fungsi yang tepat:

1. **search_activities** - Pencarian dan filter data
2. **get_user_list** - Daftar user/karyawan  
3. **analyze_full_data** - Analisis kompleks dan statistik
4. **general_conversation** - Percakapan umum

### **Function Calling**
- **search_activities(user_name, status, task_name, bulan)**
- **get_user_list()**
- Context stuffing untuk analisis kompleks
- General conversation untuk pertanyaan umum

---

## **Instalasi & Setup**

### 1. **Clone repo & masuk ke folder**
```bash
git clone <repo-url>
cd ai-task-analyst
```

### 2. **Buat & aktifkan environment (opsional, tapi disarankan)**
```bash
# Contoh dengan conda
conda create -n ai-task python=3.10
conda activate ai-task

# Atau dengan venv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Siapkan file `.env`**
Buat file `.env` di root, isi:
```env
LLM_API_KEY=your_google_ai_studio_api_key
LLM_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=your_google_ai_studio_api_key
```
Ganti dengan API key dan endpoint sesuai LLM yang digunakan.

### 5. **Pastikan file `database_task.sql` berisi CREATE TABLE + INSERT**
Sudah ada di repo, tapi pastikan bagian atas file seperti:
```sql
CREATE TABLE IF NOT EXISTS user (...);
CREATE TABLE IF NOT EXISTS task (...);
CREATE TABLE IF NOT EXISTS activity (...);
-- lalu INSERT ...
```

---

## **Menjalankan Aplikasi**

### 1. **Jalankan backend**
```bash
uvicorn app:app --reload
```
- Server akan otomatis membuat file `tasks.db` dari `database_task.sql` jika belum ada.
- Log akan ditulis ke `app.log` untuk monitoring.

### 2. **Akses frontend**
Buka di browser:
```
http://127.0.0.1:8000/static/index.html
```

---

## **Contoh Penggunaan**

### **Pencarian Data**
- "Cari task yang dikerjakan Budi"
- "Tampilkan pekerjaan dengan status done"
- "Aktivitas bulan Januari"
- "Task proyek website"

### **Analisis Kompleks**
- "Siapa yang paling produktif?"
- "Berapa total task selesai bulan ini?"
- "Bandingkan performa tim"
- "Buat laporan bulanan"
- "Statistik pekerjaan"

### **Manajemen User**
- "Siapa saja anggota tim?"
- "Tampilkan semua karyawan"
- "Daftar user"

### **Percakapan Umum**
- "Halo, apa kabar?"
- "Apa saja yang bisa kamu lakukan?"
- "Terima kasih"

---

## **Troubleshooting & Error Handling**

### **Error: `sqlite3.OperationalError: no such table: user`**
**Penyebab:**
File `tasks.db` sudah ada, tapi kosong/tidak sesuai schema.

**Solusi:**
1. **Hapus file `tasks.db`** di folder project.
2. **Restart server** (`uvicorn app:app --reload`).
   - Server akan otomatis membuat ulang database dari `database_task.sql`.

### **Error: `Import "fastapi" could not be resolved`**
- Pastikan environment sudah aktif.
- Jalankan: `pip install fastapi uvicorn`

### **Error: `uvicorn` not found**
- Jalankan: `pip install uvicorn`

### **Error: LLM tidak menjawab/muncul error API**
- Pastikan `.env` sudah benar dan API key aktif.
- Cek log di `app.log` untuk detail error.
- Pastikan format API response sesuai dengan yang diharapkan.

### **Error: 404 Not Found untuk endpoint**
- Pastikan menggunakan endpoint `/chat` (bukan `/chat_stream`)
- Frontend sudah diupdate untuk menggunakan endpoint yang benar.

---

## **Fitur Teknis**

### **Enhanced Prompts**
- **Router Prompt**: AI cerdas untuk memilih fungsi yang tepat
- **Summary Prompt**: Penyajian data yang informatif dan terstruktur
- **Analysis Prompt**: Analisis mendalam dengan insight actionable
- **General Prompt**: Percakapan natural dan ramah

### **Response Format**
- Tabel HTML untuk data terstruktur
- Markdown support untuk formatting
- Code blocks untuk output teknis
- Responsive design untuk mobile

### **Performance**
- Timeout 45 detik untuk API calls
- Logging detail untuk monitoring
- Error handling yang robust
- Session management yang efisien

---

## **Catatan Penggunaan**
- Semua data diambil dari database SQLite (`tasks.db`).
- Untuk update data, edit `database_task.sql` lalu hapus `tasks.db` dan restart server.
- Chat history per session disimpan di database.
- Log detail tersedia di `app.log` untuk debugging.

---

## **Pengembangan Lanjutan**
- Untuk data besar, bisa batasi data yang dikirim ke LLM.
- Bisa ganti LLM ke OpenAI, Ollama, dsb, cukup ganti `.env`.
- Untuk deployment, gunakan server production (misal: `uvicorn app:app --host 0.0.0.0 --port 80`).
- Bisa tambahkan authentication dan authorization.
- Implementasi streaming response untuk UX yang lebih baik.

---

## **Lisensi**
Bebas digunakan untuk pembelajaran dan pengembangan.

---

**Jika ada error lain, cek log `app.log` atau tanyakan di sini!**