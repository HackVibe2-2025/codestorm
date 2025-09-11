# 🔍 DeepScan - AI-Powered Deepfake Detection Platform

> Advanced deepfake detection system combining multiple AI algorithms with natural language summaries powered by Google's Gemini AI.

## 🌟 Features

### 🧠 **Multi-Algorithm Detection**
- **AI Deepfake Detection**: Hugging Face transformer models for state-of-the-art detection
- **Computer Vision Analysis**: OpenCV-based pixel-level examination
- **Metadata Analysis**: EXIF data inspection for manipulation traces
- **Texture Consistency**: Facial region texture analysis
- **Lighting & Shadow Analysis**: Inconsistency detection in illumination
- **Noise Pattern Analysis**: Compression artifact examination
- **Blur & Sharpness Analysis**: Regional sharpness consistency checks

### 🤖 **AI-Powered Summaries**
- **Natural Language Reports**: Technical analysis converted to human-readable summaries
- **Google Gemini Integration**: Advanced AI explanations of detection results
- **Confidence Scoring**: Percentage-based authenticity confidence levels
- **Detailed Recommendations**: Actionable insights for each analysis

### 🎨 **Modern Web Interface**
- **Drag & Drop Upload**: Intuitive image upload system
- **Real-time Analysis**: Live progress tracking with animated metrics
- **Interactive Dashboard**: Comprehensive results visualization
- **Responsive Design**: Works seamlessly across devices
- **Error Handling**: Robust fallback mechanisms for reliability

### 🔧 **Technical Excellence**
- **Flask Backend**: RESTful API with comprehensive error handling
- **Modular Architecture**: Easily extensible analysis modules
- **Production Ready**: Enterprise-level logging and debugging
- **Performance Optimized**: Efficient processing with caching
- **Cross-Platform**: Compatible with Windows, macOS, and Linux
   http://localhost:8000/
   ```

4. To specifically test the frontend handling of backend results, open:
   ```
   http://localhost:8000/test_frontend.html
   ```
   This test page will verify that the frontend correctly processes and displays backend results.

## End-to-End Testing

1. Make sure both backend and frontend servers are running
2. Go to the main page: `http://localhost:8000/`
3. Upload an image using the upload button or drag-drop
4. The analysis should be performed, and you should be redirected to the analysis page
5. The AI-generated summary should be displayed in the "Technical Analysis" section of the results

## Troubleshooting

If you encounter issues:

1. **Backend not responding**: Check if Flask is running on port 5000 and that CORS is properly configured
2. **No AI summary**: Verify your Gemini API key is valid and that you have proper internet connectivity
3. **Frontend not displaying results**: Open browser console to check for any JavaScript errors

## Mock Data for Testing

You can use the test files created by `test_manual.py` to simulate backend responses:
- `test_deepfake_summary.json` - Contains a mock deepfake detection result
- `test_authentic_summary.json` - Contains a mock authentic image detection result
