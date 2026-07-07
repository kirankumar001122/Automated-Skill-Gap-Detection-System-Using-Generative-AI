# 🚀 Quick Start - Local Setup

Get the Autonomous Coding Agent running in 5 minutes (no Docker required).

---

## 🎯 Quick Start (30 seconds)

```bash
# Terminal 1: Start Ollama (required)
ollama serve

# Terminal 2: Run the startup script
cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
.\run_local.bat
```

Open browser → http://localhost:3000

**Done!** 🎉

---

## ⚙️ Prerequisites

Verify you have these installed:

```bash
python --version        # Should be 3.10+
node --version         # Should be 18+
ollama --version       # Should be installed
```

If not installed:
- **Python**: Download from [python.org](https://www.python.org/downloads/)
- **Node.js**: Download from [nodejs.org](https://nodejs.org/)
- **Ollama**: Download from [ollama.ai](https://ollama.ai/)

---

## 📦 Installation

1. **Install Ollama models:**
   ```bash
   ollama pull codellama
   ```

2. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

---

## ▶️ Running

### Easy Way (Recommended):
```bash
.\run_local.bat
```
This automatically:
- Checks Ollama is running
- Creates virtual environment
- Installs dependencies
- Starts backend and frontend

### Manual Way:
```bash
# Terminal 1
ollama serve

# Terminal 2
cd backend
python main.py

# Terminal 3
cd frontend
npm run dev
```

---

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434

---

## 📋 What Changed from Docker Version

✅ **Removed:**
- Docker Desktop requirement
- Dockerfile & docker-compose.yml usage
- Docker dependency

✅ **Added:**
- Local code execution via subprocess
- `run_local.bat` & `run_local.ps1` scripts
- `LOCAL_SETUP_GUIDE.md`
- `MIGRATION_GUIDE.md`

✅ **Kept Same:**
- All agent functionality
- API endpoints
- Frontend interface
- Performance

---

## 🧪 Test It

1. **Backend health check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Generate code:**
   - Open http://localhost:3000
   - Enter: "Create a function to calculate factorial"
   - Click "Generate Code"

3. **API documentation:**
   - Visit http://localhost:8000/docs
   - Try the endpoints interactively

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| "Ollama is not running" | Run `ollama serve` in a terminal |
| "Port 8000 already in use" | Close other apps or change port in `backend/main.py` |
| "ModuleNotFoundError" | Run `pip install -r backend/requirements.txt` |
| "npm command not found" | Install Node.js from nodejs.org |

---

## 📚 Full Guides

- **Detailed Setup**: See [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)
- **All Changes**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **API Reference**: Visit http://localhost:8000/docs

---

## ✨ Features

- 🤖 6 specialized AI agents
- 💻 Multi-language code execution (Python, JS, Java, C/C++)
- 🧪 Automatic test generation
- 🔧 Code debugging and optimization
- 📝 Code explanation
- ⚡ No Docker needed
- 🏠 Fully local execution

---

## 🎓 Next Steps

1. Explore the agent system
2. Try different programming languages
3. Check out the API documentation
4. Build features on top of this!

---

**Questions?** Check [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) for detailed troubleshooting.
