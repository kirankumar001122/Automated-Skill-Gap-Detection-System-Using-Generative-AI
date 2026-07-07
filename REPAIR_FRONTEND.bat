@echo off
setlocal

echo ======================================================
echo 🛠️  NEXT.JS REPAIR: ANTIGRAVITY
echo ======================================================

cd frontend

echo [CLEANUP] Removing node_modules and locks...
if exist "node_modules" rmdir /s /q node_modules
if exist ".next" rmdir /s /q .next
if exist "package-lock.json" del /f /q package-lock.json

echo [INSTALL] Running fresh npm install...
echo (This will also fix the SWC binary issue)
call npm install

echo [START] Starting Next.js Dev Server...
echo [INFO] Dashboard will be at http://localhost:3000
call npm run dev

echo ======================================================
echo ✅ Frontend process finished.
echo ======================================================
pause
