#!/usr/bin/env pwsh
# Autonomous Coding Agent - Local Startup Script (PowerShell)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Autonomous Coding Agent - Local Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "[*] Checking if Ollama is running..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -ErrorAction Stop
    Write-Host "[+] Ollama is running on http://localhost:11434" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "[!] ERROR: Ollama is not running!" -ForegroundColor Red
    Write-Host "[*] Please start Ollama in another terminal:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    ollama serve" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Create venv if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "[*] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] ERROR: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "[*] Make sure Python is installed and added to PATH" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[+] Virtual environment created" -ForegroundColor Green
    
    Write-Host "[*] Installing Python dependencies..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    pip install -q -r backend\requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] ERROR: Failed to install Python dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[+] Python dependencies installed" -ForegroundColor Green
}

# Install Node dependencies if needed
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host ""
    Write-Host "[*] Installing Node.js dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] ERROR: Failed to install Node dependencies" -ForegroundColor Red
        Write-Host "[*] Make sure Node.js is installed from https://nodejs.org/" -ForegroundColor Yellow
        Pop-Location
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[+] Node.js dependencies installed" -ForegroundColor Green
    Pop-Location
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Services..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start backend
Write-Host "[+] Starting Backend API on http://localhost:8000" -ForegroundColor Green
Start-Process pwsh -ArgumentList "-Command", "cd backend; python main.py" -WindowStyle Normal

# Wait for backend
Write-Host "[*] Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend
Write-Host "[+] Starting Frontend on http://localhost:3000" -ForegroundColor Green
Start-Process pwsh -ArgumentList "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Services Started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[+] Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "[+] Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "[+] API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Close the service windows to stop them." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"
