@echo off
REM Nexora AI - Startup Script for Windows
REM This script helps you start the application quickly

echo 🚀 Nexora AI - AI Autonomous Coding Workspace
echo ==============================================

REM Function to check if command exists
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docker.com
    pause
    exit /b 1
)

echo [INFO] Docker is installed ✓

REM Check if Docker is running
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [INFO] Docker is running ✓

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Ollama is not installed.
    echo Install with: curl -fsSL https://ollama.ai/install.sh | sh
    pause
    exit /b 1
)

echo [INFO] Ollama is installed ✓

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARN] Ollama is not running. Starting it...
    start /B ollama serve
    timeout /t 10 /nobreak >nul
    
    REM Check again
    curl -s http://localhost:11434/api/tags >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to start Ollama. Please start it manually with: ollama serve
        pause
        exit /b 1
    )
)

echo [INFO] Ollama is running ✓

REM Check if models are installed
ollama list | findstr /C:"NAME" >nul
if %errorlevel% neq 0 (
    echo [WARN] No models found. Installing recommended models...
    
    echo [INFO] Pulling codellama:7b (this may take a while)...
    ollama pull codellama:7b
    
    echo [INFO] Pulling deepseek-coder:6.7b (this may take a while)...
    ollama pull deepseek-coder:6.7b
    
    echo [INFO] Models installed successfully ✓
) else (
    echo [INFO] Found Ollama models ✓
    ollama list
)

REM Check environment file
if not exist ".env" (
    echo [WARN] .env file not found. Creating from template...
    copy .env.example .env >nul
    echo [INFO] Created .env file from template ✓
    echo [WARN] You may want to edit .env file for custom configuration
) else (
    echo [INFO] .env file exists ✓
)

REM Stop existing containers
echo [INFO] Stopping existing containers...
docker-compose down 2>nul

REM Build and start services
echo [INFO] Building and starting services...
docker-compose up --build

echo.
echo [INFO] Application stopped.
pause
