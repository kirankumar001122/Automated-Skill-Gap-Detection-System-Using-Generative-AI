@echo off
setlocal
cd /d "%~dp0"

echo ======================================================
echo   🚀 Autonomous Coding Agent - ULTIMATE LOCAL LAUNCH
echo ======================================================
echo.

REM 1. Setup Backend
echo [*] Initializing Backend...
if not exist "venv\" (
    if not exist "backend\venv\" (
        echo [*] Creating virtual environment...
        python -m venv venv
    )
)

REM 2. Start Backend in a new terminal
echo [*] Launching Backend API (Port 8000)...
start "BACKEND_API" cmd /c "cd backend && start_backend.bat"

REM 3. Wait for backend to warm up
echo [*] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM 4. Start Frontend in a new terminal
echo [*] Launching Frontend Dashboard (Port 3000)...
start "FRONTEND_UI" cmd /c "cd frontend && start_frontend.bat"

echo.
echo ======================================================
echo   ✅ ALL SERVICES ARE STARTING!
echo ======================================================
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3000
echo   - API Docs: http://localhost:8000/docs
echo.
echo   Check the new terminal windows for any errors.
echo   If you see "Ollama" errors, ensure your .env has an API key.
echo ======================================================
pause
