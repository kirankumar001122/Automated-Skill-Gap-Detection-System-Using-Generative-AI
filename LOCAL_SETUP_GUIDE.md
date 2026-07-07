# 🚀 Local Setup Guide (No Docker)

This guide will help you run the Autonomous Coding Agent locally on Windows without Docker.

---

## 📋 System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.10+** [Download](https://www.python.org/downloads/)
- **Node.js 18+** [Download](https://nodejs.org/) (Optional, for JavaScript execution)
- **Ollama** [Download](https://ollama.ai/) (For local LLM)
- **G++ Compiler** (For C/C++ execution - Optional)
- **Java JDK** (For Java execution - Optional)
- **At least 4GB RAM available**
- **At least 5GB disk space**

---

## ✅ Pre-Installation Checklist

Before starting, verify you have these installed:

```bash
# Check Python
python --version         # Should be 3.10 or higher

# Check Node.js (optional)
node --version          # Should be 18 or higher

# Check Ollama
ollama --version        # Should be installed
```

---

## 🛠️ Step-by-Step Installation

### Step 1: Install Ollama and Models

1. **Download and Install Ollama**
   - Visit [ollama.ai](https://ollama.ai)
   - Download and run the installer
   - Follow the installation wizard

2. **Start Ollama Service**
   - Open PowerShell or Command Prompt
   - Run: `ollama serve`
   - You should see: `Listening on 127.0.0.1:11434`

3. **Install Models** (in another terminal)
   ```bash
   # Install a coding model (choose one)
   ollama pull codellama        # ~4GB - Recommended
   
   # OR
   ollama pull deepseek-coder   # ~6GB - Excellent for coding
   
   # OR
   ollama pull llama3           # ~4GB - Good general purpose
   
   # Verify installation
   ollama list
   ```

   > ⏱️ Model download may take 5-10 minutes depending on your internet speed

### Step 2: Navigate to Project Directory

```bash
cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
```

### Step 3: Set Up Python Backend

1. **Create Python Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import fastapi; print('✓ FastAPI installed')"
   python -c "import requests; print('✓ Requests installed')"
   ```

### Step 4: Set Up Frontend (Next.js)

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Return to Project Root**
   ```bash
   cd ..
   ```

---

## 🚀 Running the Project (Local)

### Method 1: Using Batch Scripts (Windows - Easy!)

1. **Make sure Ollama is running**
   - Open a terminal and run: `ollama serve`

2. **Open PowerShell and run the startup script**
   ```bash
   cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
   .\run_local.bat
   ```

   This will automatically:
   - Start the backend API on http://localhost:8000
   - Start the frontend dev server on http://localhost:3000

3. **Open your browser**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

### Method 2: Manual Setup (Full Control)

**Terminal 1 - Start Ollama:**
```bash
ollama serve
# Keep this running in the background
```

**Terminal 2 - Start Backend:**
```bash
cd backend
python main.py
# Should see: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 3 - Start Frontend:**
```bash
cd frontend
npm run dev
# Should see: "- Local: http://localhost:3000"
```

---

## 🧪 Testing the Installation

### Test 1: Backend Health Check

Open PowerShell and run:
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "models": ["codellama:latest"]
}
```

### Test 2: Frontend Access

Open browser:
```
http://localhost:3000
```

You should see the Autonomous Coding Agent dashboard.

### Test 3: Code Generation

In the frontend dashboard:
1. Enter a prompt like: "Create a function to calculate factorial"
2. Click "Generate Code"
3. You should see generated Python code

---

## 🔧 Configuration

### Change Backend Port

Edit `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Change this to different port
        reload=True,
        log_level="info"
    )
```

### Change Frontend Port

Edit `frontend/package.json`:
```json
"scripts": {
  "dev": "next dev -p 3001"  // Change port to 3001
}
```

### Change Ollama Model

Edit `backend/services/ollama_service.py`:
```python
class OllamaConfig(BaseModel):
    base_url: str = "http://localhost:11434"
    model: str = "deepseek-coder"  # Change model here
    timeout: int = 30
```

---

## 🔌 Optional: Install Language Compilers

To support more languages, install:

### JavaScript/Node.js
```bash
# Already required for frontend setup
```

### Java
```bash
# Download JDK from oracle.com
# Add Java bin folder to PATH
```

### C/C++
```bash
# For Windows: Install MinGW or MSVC
# Add g++.exe to PATH
```

---

## ⚠️ Troubleshooting

### Issue: "Ollama is not running"
**Solution:**
```bash
ollama serve
```
Keep this terminal open in the background.

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
# Make sure you activated venv
venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt
```

### Issue: "Cannot connect to backend at localhost:8000"
**Solution:**
1. Check backend is running: `curl http://localhost:8000`
2. If not running, start it: `python backend/main.py`
3. Check port 8000 is not in use: `netstat -ano | findstr :8000`

### Issue: "npm command not found"
**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

### Issue: "Code execution timeout"
**Solution:**
- The default timeout is 10 seconds
- Edit `backend/services/local_executor.py`:
  ```python
  self.timeout = 30  # Increase to 30 seconds
  ```

### Issue: "g++ not found" for C/C++ code
**Solution:**
- Install MinGW: https://www.mingw-w64.org/
- Or install Visual Studio Build Tools
- Add g++ to your PATH

---

## 📊 Project Structure

```
ProjectStu/
├── backend/
│   ├── main.py                 # Backend entry point
│   ├── requirements.txt         # Python dependencies
│   ├── services/
│   │   ├── ollama_service.py   # LLM interface
│   │   ├── local_executor.py   # Code execution (local)
│   │   └── code_runner.py      # Code runner wrapper
│   ├── agents/                  # AI agents
│   └── routes/                  # API routes
│
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── app/
│   │   ├── page.tsx            # Main dashboard
│   │   └── components/         # React components
│   └── services/
│       └── api.ts              # API client
│
├── run_local.bat               # Easy startup script
└── LOCAL_SETUP_GUIDE.md        # This file
```

---

## 🎯 Next Steps

1. ✅ Install all prerequisites
2. ✅ Run `ollama serve` in one terminal
3. ✅ Run `.\run_local.bat` in another terminal
4. ✅ Open http://localhost:3000 in browser
5. ✅ Start generating code!

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs**: Look at backend terminal output for error messages
2. **Verify Ollama**: Ensure `ollama serve` is running
3. **Check ports**: Make sure ports 3000 and 8000 are available
4. **Reinstall packages**: `pip install --upgrade -r backend/requirements.txt`

---

## 🎉 You're All Set!

Your Autonomous Coding Agent is now running locally without Docker!

**Access points:**
- 🌐 Frontend: http://localhost:3000
- 📚 API Docs: http://localhost:8000/docs
- 🤖 Backend: http://localhost:8000

**Happy coding!** 🚀
