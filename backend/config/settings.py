
import os

class Config:
    """Application configuration"""
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model configurations
    DEEPFAKE_MODEL_NAME = "prithivMLmods/deepfake-detector-model-v1"
    CONFIDENCE_THRESHOLD = 0.5
    
    # Analysis thresholds
    BLUR_THRESHOLD = 100.0
    NOISE_THRESHOLD = 0.15
    TEXTURE_CONSISTENCY_THRESHOLD = 0.7
    SHADOW_CONSISTENCY_THRESHOLD = 0.6