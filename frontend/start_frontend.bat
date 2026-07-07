@echo off
echo ========================================
echo   Autonomous Agent - Frontend
echo ========================================
echo [*] Checking dependencies...

if not exist "node_modules\" (
    echo [*] node_modules not found. Installing...
    call npm install
)

echo [+] Starting Frontend on http://localhost:3000
npm run dev
