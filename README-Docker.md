# 🐳 Docker Setup untuk AI Task Analyst

Panduan lengkap untuk menjalankan aplikasi AI Task Analyst menggunakan Docker.

## 📋 Prerequisites

- Docker Desktop atau Docker Engine
- Docker Compose
- File `.env` yang sudah dikonfigurasi

## 🚀 Quick Start

### 1. **Development Mode (Hot Reload)**
```bash
# Build dan jalankan dengan hot reload
docker-compose -f docker-compose.dev.yml up --build

# Atau jalankan di background
docker-compose -f docker-compose.dev.yml up -d --build
```

### 2. **Production Mode**
```bash
# Build dan jalankan untuk production
docker-compose up --build

# Atau dengan nginx reverse proxy
docker-compose --profile production up --build
```

## 🔧 Konfigurasi

### Environment Variables
Pastikan file `.env` sudah ada dengan konfigurasi:
```env
LLM_API_KEY=your_api_key_here
LLM_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=your_api_key_here
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama2
```

### Volume Mounts
- `./tasks.db:/app/tasks.db` - Database persistence
- `./logs:/app/logs` - Log files
- `./.env:/app/.env` - Environment variables

## 📁 File Structure

```
ai-task-analyst/
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Production compose
├── docker-compose.dev.yml     # Development compose
├── .dockerignore             # Files to ignore in build
├── nginx.conf                # Nginx configuration
└── README-Docker.md          # This file
```

## 🛠️ Commands

### Build Image
```bash
# Build image saja
docker build -t ai-task-analyst .

# Build tanpa cache
docker build --no-cache -t ai-task-analyst .
```

### Run Container
```bash
# Run container langsung
docker run -p 8000:8000 --env-file .env ai-task-analyst

# Run dengan volume mounts
docker run -p 8000:8000 \
  -v $(pwd)/tasks.db:/app/tasks.db \
  -v $(pwd)/.env:/app/.env \
  ai-task-analyst
```

### Docker Compose Commands
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build

# Remove everything (containers, networks, volumes)
docker-compose down -v --remove-orphans
```

## 🔍 Troubleshooting

### 1. **Port Already in Use**
```bash
# Check what's using port 8000
netstat -tulpn | grep :8000

# Kill process using port 8000
sudo kill -9 $(lsof -t -i:8000)

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### 2. **Database Issues**
```bash
# Remove existing database
rm tasks.db

# Restart container (will recreate database)
docker-compose restart
```

### 3. **Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with user permissions
docker-compose run --user $(id -u):$(id -g) ai-task-analyst
```

### 4. **Build Cache Issues**
```bash
# Clean build without cache
docker-compose build --no-cache

# Remove all unused images
docker image prune -a
```

## 📊 Monitoring

### Health Check
```bash
# Check container health
docker-compose ps

# View health check logs
docker inspect ai-task-analyst-app | grep -A 10 Health
```

### Logs
```bash
# View application logs
docker-compose logs -f ai-task-analyst

# View nginx logs (if using production profile)
docker-compose logs -f nginx
```

## 🌐 Access Application

- **Development**: http://localhost:8000/static/index.html
- **Production (with nginx)**: http://localhost/static/index.html

## 🔒 Security Notes

1. **Environment Variables**: Jangan commit file `.env` ke repository
2. **Database**: File `tasks.db` akan dibuat otomatis jika belum ada
3. **Logs**: Log files disimpan di folder `./logs/`
4. **Network**: Aplikasi berjalan di network terisolasi `ai-task-network`

## 🚀 Production Deployment

### 1. **Environment Setup**
```bash
# Copy environment template
cp env.example .env

# Edit dengan konfigurasi production
nano .env
```

### 2. **Deploy with Nginx**
```bash
# Deploy dengan nginx reverse proxy
docker-compose --profile production up -d

# Check status
docker-compose ps
```

### 3. **SSL/HTTPS (Optional)**
Untuk production, pertimbangkan menambahkan SSL certificate di nginx configuration.

## 📝 Notes

- Database akan otomatis dibuat dari `database_task.sql` saat pertama kali run
- Log files akan tersimpan di folder `./logs/`
- Untuk development, gunakan `docker-compose.dev.yml` untuk hot reload
- Untuk production, gunakan `docker-compose.yml` dengan atau tanpa nginx
