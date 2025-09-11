
# utils/noise_utils.py
# ===============================

import cv2
import numpy as np
from scipy import ndimage

class NoiseAnalyzer:
    """Noise and compression artifact analysis"""
    
    @staticmethod
    def analyze_noise(image_path):
        """Analyze noise patterns and compression artifacts"""
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Analyze noise characteristics
            noise_level = NoiseAnalyzer._estimate_noise_level(gray)
            compression_artifacts = NoiseAnalyzer._detect_compression_artifacts(gray)
            noise_consistency = NoiseAnalyzer._analyze_noise_consistency(gray)
            
            # Calculate suspicious score
            suspicious_score = 0.0
            if noise_level > 0.15:  # High noise
                suspicious_score += 0.3
            if compression_artifacts > 0.2:  # High artifacts
                suspicious_score += 0.4
            if noise_consistency < 0.6:  # Inconsistent noise
                suspicious_score += 0.3
            
            return {
                "noise_level": round(noise_level, 4),
                "compression_artifacts": round(compression_artifacts, 4),
                "noise_consistency": round(noise_consistency, 4),
                "suspicious_score": min(suspicious_score, 1.0)
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "suspicious_score": 0.5
            }
    
    @staticmethod
    def _estimate_noise_level(image):
        """Estimate noise level using wavelet transform"""
        # Apply Gaussian filter and calculate difference
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        noise = cv2.absdiff(image.astype(np.float32), blurred.astype(np.float32))
        return np.mean(noise) / 255.0
    
    @staticmethod
    def _detect_compression_artifacts(image):
        """Detect JPEG compression artifacts"""
        # Apply high-pass filter to detect artifacts
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        filtered = cv2.filter2D(image.astype(np.float32), -1, kernel)
        artifact_score = np.mean(np.abs(filtered)) / 255.0
        return min(artifact_score, 1.0)
    
    @staticmethod
    def _analyze_noise_consistency(image):
        """Analyze consistency of noise across image regions"""
        h, w = image.shape
        noise_levels = []
        
        # Analyze 2x2 grid of regions
        for i in range(2):
            for j in range(2):
                start_h, end_h = i * h // 2, (i + 1) * h // 2
                start_w, end_w = j * w // 2, (j + 1) * w // 2
                region = image[start_h:end_h, start_w:end_w]
                
                # Calculate noise in this region
                blurred = cv2.GaussianBlur(region, (3, 3), 0)
                noise = cv2.absdiff(region.astype(np.float32), blurred.astype(np.float32))
                noise_levels.append(np.mean(noise))
        
        # Calculate consistency (inverse of standard deviation)
        if len(noise_levels) > 1:
            consistency = 1.0 - min(np.std(noise_levels) / (np.mean(noise_levels) + 1e-6), 1.0)
        else:
            consistency = 1.0
        
        return consistency