
# utils/blur_utils.py
# ===============================

import cv2
import numpy as np

class BlurAnalyzer:
    """Image sharpness and blur analysis"""
    
    @staticmethod
    def analyze_blur(image_path):
        """Analyze image for blur artifacts and sharpness inconsistencies"""
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate overall sharpness using Laplacian variance
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Analyze regional sharpness variations
            regions = BlurAnalyzer._get_image_regions(gray)
            regional_sharpness = []
            
            for region in regions:
                region_var = cv2.Laplacian(region, cv2.CV_64F).var()
                regional_sharpness.append(region_var)
            
            # Calculate sharpness consistency with anti-false-positive measures
            sharpness_std = np.std(regional_sharpness)
            avg_sharpness = np.mean(regional_sharpness)
            consistency_score = 1.0 - min(sharpness_std / (avg_sharpness + 1e-6), 1.0)
            
            # 🔧 ANTI-FALSE-POSITIVE: More conservative suspicious scoring
            # Only flag if consistency is very poor AND overall sharpness is reasonable
            suspicious_score = 0.0
            if consistency_score < 0.5 and avg_sharpness > 50:  # More conservative threshold
                suspicious_score = (1.0 - consistency_score) * 0.7  # Reduced impact
            
            return {
                "overall_sharpness": round(laplacian_var, 2),
                "is_blurry": laplacian_var < 100.0,
                "regional_sharpness": [round(x, 2) for x in regional_sharpness],
                "sharpness_consistency": round(consistency_score, 3),
                "suspicious_score": round(suspicious_score, 3)
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "suspicious_score": 0.5
            }
    
    @staticmethod
    def _get_image_regions(image):
        """Split image into regions for analysis"""
        h, w = image.shape
        regions = []
        
        # Split into 3x3 grid
        for i in range(3):
            for j in range(3):
                start_h, end_h = i * h // 3, (i + 1) * h // 3
                start_w, end_w = j * w // 3, (j + 1) * w // 3
                region = image[start_h:end_h, start_w:end_w]
                regions.append(region)
        
        return regions

# Legacy function for backward compatibility
def analyze_blur(image_path):
    """Legacy function - use BlurAnalyzer.analyze_blur() instead"""
    return BlurAnalyzer.analyze_blur(image_path)