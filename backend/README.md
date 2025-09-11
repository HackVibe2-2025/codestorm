# DeepScan Backend Setup Guide

## Quick Start (Basic Functionality)

The backend is now working with basic computer vision analysis. To start immediately:

```bash
cd backend
python app.py
```

The server will start on http://localhost:5000

## Available Endpoints

- `GET /health` - Health check
- `POST /detect` - Upload image for deepfake analysis

## API Usage Example

```bash
# Health check
curl http://localhost:5000/health

# Upload image for analysis
curl -X POST -F "image=@your_image.jpg" http://localhost:5000/detect

# Get summary format
curl -X POST -F "image=@your_image.jpg" "http://localhost:5000/detect?format=summary"
```

## Current Analysis Features ✅

1. **EXIF Metadata Analysis** - Detects suspicious software signatures and timestamp inconsistencies
2. **Blur/Sharpness Analysis** - Analyzes sharpness consistency across image regions  
3. **Color Distribution Analysis** - Detects unnatural color balance
4. **Noise Pattern Analysis** - Analyzes noise consistency and compression artifacts
5. **Lighting/Shadow Analysis** - Detects lighting direction inconsistencies
6. **Texture Analysis** - Analyzes texture patterns in skin regions

## Enhanced Setup (With AI Model)

For full AI-powered deepfake detection, install additional dependencies:

```bash
pip install -r requirements.txt
```

This will enable:
- **🤖 Hugging Face AI Model** - Advanced deepfake detection using pre-trained models

## File Structure

```
backend/
├── app.py                 # Flask web server
├── requirements.txt       # Python dependencies  
├── test_backend.py       # Test script
├── config/
│   └── settings.py       # Configuration
├── models/
│   └── hf_deepfake.py    # AI model wrapper
├── services/
│   ├── operations.py     # Main analysis orchestrator
│   └── summarizer.py     # Result summarization
├── utils/                # Computer vision utilities
│   ├── blur_utils.py
│   ├── color_utils.py
│   ├── exif_utils.py
│   ├── noise_utils.py
│   ├── shadow_utils.py
│   └── texture_utils.py
├── tests/
│   └── tests_ops.py      # Unit tests
└── uploads/              # Temporary upload directory
```

## Testing

Run the test suite:

```bash
python test_backend.py
```

Run unit tests:

```bash
python -m pytest tests/
```

## Configuration

Edit `config/settings.py` to customize:
- Upload file size limits
- Analysis thresholds  
- Model configurations
- Allowed file types

## Integration with Frontend

The backend API is designed to work with the DeepScan frontend. When both are running:

1. Frontend: http://localhost:8000
2. Backend: http://localhost:5000

To integrate, update the frontend JavaScript to call the backend API instead of using mock data.

## Troubleshooting

**Import Errors**: Install missing packages with `pip install <package_name>`

**Memory Issues**: The AI model requires ~2GB RAM. Disable it by setting `HF_MODEL_AVAILABLE = False` in operations.py

**File Upload Issues**: Check that the `uploads/` directory exists and has write permissions

## Production Deployment

For production:
1. Set `debug=False` in app.py
2. Use a production WSGI server like Gunicorn
3. Configure proper file upload limits
4. Set up proper logging
5. Use environment variables for sensitive config
