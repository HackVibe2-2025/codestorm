@echo off
echo 🚀 Starting DeepScan Development Environment...
echo.

echo 📂 Navigating to project directory...
cd /d "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan"

echo 🐍 Starting Backend Server (Flask)...
start "DeepScan Backend" cmd /k "cd backend && python app.py"

echo ⏳ Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "DeepScan Frontend" cmd /k "cd frontend && python -m http.server 8000"

echo ⏳ Waiting for frontend to initialize...
timeout /t 2 /nobreak > nul

echo ✅ DeepScan is starting up!
echo.
echo 📋 Access URLs:
echo    🔗 Frontend: http://localhost:8000
echo    🔗 Backend API: http://localhost:5000
echo.
echo 💡 Both servers are running in separate windows.
echo    Close this window or press Ctrl+C to continue.
echo.
pause
