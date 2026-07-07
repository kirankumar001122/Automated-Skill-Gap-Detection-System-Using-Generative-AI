@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo   Autonomous Agent - Backend API
echo ========================================

REM Set environment variables if needed
set PORT=8000
set HOST=127.0.0.1

REM Use the virtual environment if it exists
if exist "venv\Scripts\python.exe" (
    set PYTHON_EXE=venv\Scripts\python.exe
) else if exist "..\venv\Scripts\python.exe" (
    set PYTHON_EXE=..\venv\Scripts\python.exe
) else if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXE=.venv\Scripts\python.exe
) else (
    set PYTHON_EXE=python
)

echo [*] Using Python: %PYTHON_EXE%
echo [*] Installing dependencies...
%PYTHON_EXE% -m pip install -r requirements.txt

echo [+] Starting Backend API on http://%HOST%:%PORT%
echo [INFO] Press Ctrl+C to stop
%PYTHON_EXE% -m uvicorn main:app --host %HOST% --port %PORT% --reload

pause
