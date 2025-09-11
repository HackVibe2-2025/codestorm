from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import json
import numpy as np
from werkzeug.utils import secure_filename
from services.operations import DeepfakeAnalyzer
from services.summarizer import ResultSummarizer
from config.settings import Config

def convert_for_json(obj):
    """Convert numpy types and other non-serializable objects to JSON-serializable types"""
    if isinstance(obj, dict):
        return {key: convert_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_json(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    else:
        return obj

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

analyzer = DeepfakeAnalyzer()
summarizer = ResultSummarizer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Deepfake Detection API is running"})

@app.route('/detect', methods=['POST'])
def detect_deepfake():
    """Main endpoint for deepfake detection"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only jpg, jpeg, png allowed"}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Run analysis
            results = analyzer.analyze_image(filepath)
            
            # Get summary format if requested
            format_type = request.args.get('format', 'json')
            if format_type == 'summary':
                summary = summarizer.generate_summary(results)
                response = {
                    "status": "success",
                    "results": convert_for_json(results),  # Always include full analysis
                    "summary": convert_for_json(summary)   # Also include summary if requested
                }
            else:
                response = {
                    "status": "success",
                    "results": convert_for_json(results)
                }
            
            return jsonify(response)
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)