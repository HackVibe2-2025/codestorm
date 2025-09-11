# 🚀 DeepScan Backend Startup Guide

## Quick Start Commands

### Option 1: Start from project root
```bash
cd "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan"
python backend/app.py
```

### Option 2: Start from backend directory
```bash
cd "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\backend"
python app.py
```

### Option 3: Using Python module syntax
```bash
cd "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\backend"
python -c "from app import app; app.run(debug=True, port=5000)"
```

### Option 4: With specific configuration
```bash
cd "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\backend"
python -c "from app import app; app.run(host='127.0.0.1', port=5000, debug=True)"
```

## 🔍 How to Check if Backend is Running

### Method 1: Check Health Endpoint
Open browser and go to: `http://127.0.0.1:5000/health`
Should return: `{"status": "healthy", "message": "Deepfake Detection API is running"}`

### Method 2: Check Terminal Output
Look for these messages:
```
✅ AI model import successful
🔄 Loading AI model...
✅ AI model loaded successfully
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Method 3: Test with curl (if available)
```bash
curl http://127.0.0.1:5000/health
```

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Kill existing process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Module not found"
```bash
# Install dependencies
cd "C:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\backend"
pip install -r requirements.txt
```

### Issue: "AI model fails to load"
```bash
# Install specific AI packages
pip install transformers torch pillow
```

## ✅ Expected Startup Sequence

1. **AI Model Loading**: Takes 10-30 seconds first time
2. **Flask Server Start**: Listens on port 5000
3. **Debug Mode**: Enables auto-reload on code changes
4. **Health Check**: Endpoint becomes available
5. **Ready for Requests**: Can accept image uploads

## 🔧 Configuration Options

- **Port**: Default 5000, can be changed in `config/settings.py`
- **Debug**: Enabled by default for development
- **Upload Folder**: `uploads/` directory (auto-created)
- **AI Model**: `prithivMLmods/deepfake-detector-model-v1`

## 📊 What Running Looks Like

When working correctly, you'll see:
- Image analysis requests with confidence scores
- AI summary generation with Gemini API
- HTTP request logs (POST /detect)
- Debug information for troubleshooting
