@echo off
setlocal

:: Autonomous Coding Agent Startup Script
echo ======================================================
echo 🤖 Starting Autonomous Coding Agent (Localhost)
echo ======================================================

:: Check for backend virtual environment
if not exist "backend\venv" (
    echo [BACKEND] Creating virtual environment...
    python -m venv backend\venv
)

:: Install backend dependencies
echo [BACKEND] Installing/Updating dependencies...
call backend\venv\Scripts\activate
pip install -r backend\requirements.txt

:: Start Backend in a new window
echo [BACKEND] Starting server on http://localhost:8000...
start "Backend API" cmd /k "call backend\venv\Scripts\activate && cd backend && python main.py"

:: Wait for backend to initialize
timeout /t 5 /nobreak > nul

:: Check for frontend dependencies
if not exist "frontend\node_modules" (
    echo [FRONTEND] Installing dependencies - npm install...
    cd frontend && npm install && cd ..
)

:: Start Frontend in a new window
echo [FRONTEND] Starting dashboard on http://localhost:3000...
start "Frontend Dashboard" cmd /k "cd frontend && npm run dev"

:: Wait for frontend to start
echo [WAIT] Waiting for Next.js to initialize...
timeout /t 10 /nobreak > nul

:: Open browser automatically
echo [BROWSER] Opening dashboard...
start http://localhost:3000

echo ======================================================
echo ✅ All systems operational!
echo Backend: http://localhost:8000
echo Dashboard: http://localhost:3000
echo ======================================================
pause
