#!/bin/bash

echo "🚀 Starting DeepScan Development Environment..."
echo

echo "📂 Navigating to project directory..."
cd "$(dirname "$0")"

echo "🐍 Starting Backend Server (Flask)..."
gnome-terminal --title="DeepScan Backend" -- bash -c "cd backend && python app.py; exec bash" 2>/dev/null || \
xterm -title "DeepScan Backend" -e "cd backend && python app.py; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/backend && python app.py"' 2>/dev/null || \
echo "⚠️  Please manually start: cd backend && python app.py"

echo "⏳ Waiting for backend to initialize..."
sleep 3

echo "🌐 Starting Frontend Server..."
gnome-terminal --title="DeepScan Frontend" -- bash -c "cd frontend && python -m http.server 8000; exec bash" 2>/dev/null || \
xterm -title "DeepScan Frontend" -e "cd frontend && python -m http.server 8000; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && python -m http.server 8000"' 2>/dev/null || \
echo "⚠️  Please manually start: cd frontend && python -m http.server 8000"

echo "⏳ Waiting for frontend to initialize..."
sleep 2

echo "✅ DeepScan is starting up!"
echo
echo "📋 Access URLs:"
echo "   🔗 Frontend: http://localhost:8000"
echo "   🔗 Backend API: http://localhost:5000"
echo
echo "💡 Both servers should be running in separate terminals."
echo
