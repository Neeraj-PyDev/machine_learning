@echo off
cd /d "%~dp0"

for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /PID %%p /F >nul 2>&1
)

"%~dp0venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000
