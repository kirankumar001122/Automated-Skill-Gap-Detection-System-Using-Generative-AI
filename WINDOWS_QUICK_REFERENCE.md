# 🚀 Windows Quick Reference

Quick commands for getting Autonomous Coding Agent running locally on Windows.

---

## ⚡ Ultra-Quick Start (2 minutes)

```batch
# Assuming you already have Python, Node.js, and Ollama installed

# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Navigate and run
cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
.\run_local.bat
```

**Done!** Open: http://localhost:3000

---

## 🔧 First-Time Setup (10 minutes)

### Step 1: Install Prerequisites
```batch
# Check Python is installed
python --version

# Check Node.js is installed  
node --version

# Check Ollama is installed
ollama --version
```

If any are missing, install from:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Ollama: https://ollama.ai/

### Step 2: Navigate to Project
```batch
cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
```

### Step 3: Start Services
```batch
# Terminal 1
ollama serve

# Terminal 2
.\run_local.bat
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main dashboard |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/api/v1/health | System status |
| Ollama | http://localhost:11434 | LLM service |

---

## 📋 Common Commands

### Start Everything
```batch
# One-line startup (Terminal 1)
ollama serve

# One-line startup (Terminal 2)
.\run_local.bat
```

### Manual Startup (If needed)
```batch
# Terminal 1: Ollama
ollama serve

# Terminal 2: Backend
cd backend
python main.py

# Terminal 3: Frontend
cd frontend
npm run dev
```

### Test Backend
```batch
curl http://localhost:8000/api/v1/health
```

### Install/Update Dependencies
```batch
pip install -r backend\requirements.txt
cd frontend && npm install
```

### Stop Everything
```batch
# Close the terminal windows or press Ctrl+C in each
```

---

## 🐛 Quick Troubleshooting

### "Ollama not running"
```batch
ollama serve
```
Keep this running in background.

### "Port 8000 already in use"
```batch
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number shown)
taskkill /PID <PID> /F
```

### "Module not found"
```batch
pip install -r backend\requirements.txt
```

### "npm command not found"
Download Node.js from https://nodejs.org/ and restart terminal.

### "Cannot connect to backend"
Check that backend is running:
```batch
python backend\main.py
```

---

## 🎯 Typical Workflow

1. **Open 2 terminals**

2. **Terminal 1: Start Ollama**
   ```batch
   ollama serve
   ```

3. **Terminal 2: Start Project**
   ```batch
   .\run_local.bat
   ```

4. **Open Browser**
   ```
   http://localhost:3000
   ```

5. **Generate Code**
   - Enter prompt
   - Click "Generate Code"
   - See results!

6. **Stop Everything**
   - Close terminal windows

---

## 📊 What's Running

```
http://localhost:3000  ← Frontend (React/Next.js)
                          ↓ (Sends requests to)
http://localhost:8000  ← Backend API (FastAPI)
                          ↓ (Uses)
http://localhost:11434 ← Ollama LLM Service
```

---

## 📖 Detailed Guides

- **5-minute quick start**: [README_LOCAL.md](README_LOCAL.md)
- **Complete setup guide**: [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)
- **Technical details**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Main documentation**: [README.md](README.md)

---

## ✨ Features

- 🤖 6 AI agents for code generation, debugging, testing, optimization
- 💻 Multi-language support (Python, JavaScript, Java, C/C++)
- 🧪 Automatic test generation
- 🔧 Code debugging and optimization
- 📝 Code explanation
- ⚡ Local execution (no Docker required!)

---

## 🎓 Example Usage

### Generate Code
```
Prompt: "Create a function to calculate factorial"
Language: Python
Click: "Generate Code"
```

### Run Code
```
Click: "Run Code"
View output in console
```

### Debug
```
Paste buggy code
Click: "Debug Code"
See fixed version
```

### Get Explanation
```
View generated code
Click: "Explain Code"
Read explanation
```

---

## 💡 Tips

- Keep Ollama running in the background
- Use `.bat` script for easy one-click startup
- API documentation is at http://localhost:8000/docs
- Check browser console for frontend errors
- Check backend terminal for backend errors
- Models available: codellama, deepseek-coder, llama3

---

## 🆘 Getting Help

1. Check [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) troubleshooting section
2. Verify all prerequisites are installed
3. Ensure Ollama is running
4. Check ports 3000, 8000, 11434 are available
5. Reinstall dependencies: `pip install --upgrade -r backend\requirements.txt`

---

## 🎉 Ready to Go!

You're all set up! Start with:
```batch
ollama serve
.\run_local.bat
```

Then open: http://localhost:3000

**Enjoy coding with AI! 🚀**
