import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

class TextureAnalyzer:
    """Texture analysis for deepfake detection, focusing on skin regions"""
    
    @staticmethod
    def analyze_texture(image_path):
        """Analyze texture patterns for inconsistencies"""
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect potential skin regions (simplified)
            skin_mask = TextureAnalyzer._detect_skin_regions(image)
            
            # Analyze texture in skin regions
            texture_features = TextureAnalyzer._extract_texture_features(gray, skin_mask)
            consistency_score = TextureAnalyzer._calculate_texture_consistency(gray, skin_mask)
            
            # Calculate suspicious score with more conservative thresholds
            suspicious_score = 0.0
            
            # 🔧 ANTI-FALSE-POSITIVE: More conservative texture analysis
            if consistency_score < 0.5:  # Lowered from 0.7 - only flag very inconsistent textures
                suspicious_score += 0.4  # Reduced impact
            if texture_features.get('uniformity', 0) > 0.85:  # Only flag extremely uniform textures
                suspicious_score += 0.2  # Reduced impact
            
            # Additional check: if skin regions are very small, reduce suspicion
            skin_pixel_count = np.sum(skin_mask > 0)
            if skin_pixel_count < 500:  # Very small skin regions
                suspicious_score *= 0.5  # Reduce suspicion for non-face images
            
            return {
                "skin_regions_detected": np.sum(skin_mask > 0) > 100,
                "texture_features": texture_features,
                "texture_consistency": round(consistency_score, 3),
                "suspicious_score": min(suspicious_score, 1.0)
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "suspicious_score": 0.5
            }
    
    @staticmethod
    def _detect_skin_regions(image):
        """Simple skin detection using color ranges"""
        # Convert to HSV for better skin detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create mask
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        return mask
    
    @staticmethod
    def _extract_texture_features(gray_image, mask):
        """Extract GLCM texture features"""
        try:
            # Apply mask to focus on skin regions
            masked_image = np.where(mask > 0, gray_image, 0)
            
            # Calculate GLCM
            glcm = graycomatrix(masked_image, distances=[1], angles=[0, 45, 90, 135], 
                             levels=256, symmetric=True, normed=True)
            
            # Extract features
            contrast = graycoprops(glcm, 'contrast')[0, 0]
            dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
            homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
            energy = graycoprops(glcm, 'energy')[0, 0]
            
            return {
                "contrast": round(float(contrast), 4),
                "dissimilarity": round(float(dissimilarity), 4),
                "homogeneity": round(float(homogeneity), 4),
                "uniformity": round(float(energy), 4)
            }
        
        except Exception:
            return {"error": "Could not extract texture features"}
    
    @staticmethod
    def _calculate_texture_consistency(gray_image, mask):
        """Calculate texture consistency across different regions"""
        # Find regions with skin
        if np.sum(mask) < 100:  # Not enough skin regions
            return 1.0
        
        # Extract texture from different patches
        patches = TextureAnalyzer._extract_patches(gray_image, mask)
        if len(patches) < 2:
            return 1.0
        
        # Calculate texture variance across patches
        variances = [np.var(patch) for patch in patches]
        consistency = 1.0 - min(np.std(variances) / (np.mean(variances) + 1e-6), 1.0)
        
        return consistency
    
    @staticmethod
    def _extract_patches(image, mask, patch_size=32):
        """Extract patches from masked regions"""
        patches = []
        h, w = image.shape
        
        for i in range(0, h - patch_size, patch_size // 2):
            for j in range(0, w - patch_size, patch_size // 2):
                patch_mask = mask[i:i+patch_size, j:j+patch_size]
                if np.sum(patch_mask) > (patch_size * patch_size) * 0.5:  # At least 50% skin
                    patch = image[i:i+patch_size, j:j+patch_size]
                    patches.append(patch)
        
        return patches