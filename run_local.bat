@echo off
REM Nexora AI - Local Startup Script (No Docker)
REM This script starts both backend and frontend automatically

echo.
echo 🚀 Nexora AI: Local Execution Mode
echo ===================================
echo.

REM Check if Ollama is running
echo [*] Checking if Ollama is running...
curl -s http://127.0.0.1:11434/api/tags >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [!] WARNING: Ollama is not running!
    echo [*] Please start Ollama in another terminal:
    echo.
    echo     ollama serve
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)
echo [+] Ollama is running on http://localhost:11434

REM Check if venv exists, if not create it
if not exist "venv\" (
    echo.
    echo [*] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to create virtual environment
        echo [*] Make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
    
    echo [*] Installing Python dependencies...
    call venv\Scripts\activate.bat
    pip install -q -r backend\requirements.txt
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo [+] Python dependencies installed
)

REM Check if node_modules exists, if not install
if not exist "frontend\node_modules\" (
    echo.
    echo [*] Installing Node.js dependencies...
    cd frontend
    call npm install >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to install Node dependencies
        echo [*] Make sure Node.js is installed from https://nodejs.org/
        cd ..
        pause
        exit /b 1
    )
    echo [+] Node.js dependencies installed
    cd ..
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo ========================================
echo   Starting Services...
echo ========================================
echo.

REM Start backend in new window
echo [+] Starting Backend API on http://localhost:8000
start cmd /k "cd backend && python main.py"

REM Wait for backend to start
echo [*] Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo [+] Starting Frontend on http://localhost:3000
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo [+] Frontend: http://localhost:3000
echo [+] Backend API: http://localhost:8000
echo [+] API Docs: http://localhost:8000/docs
echo.
echo Close this window or press Ctrl+C to stop.
echo.
pause
