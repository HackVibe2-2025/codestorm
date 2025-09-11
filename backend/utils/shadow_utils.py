import cv2
import numpy as np

class ShadowAnalyzer:
    """Lighting and shadow consistency analysis"""
    
    @staticmethod
    def analyze_shadows(image_path):
        """Analyze lighting consistency and shadow patterns"""
        try:
            # Load image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Analyze lighting direction consistency
            lighting_consistency = ShadowAnalyzer._analyze_lighting_direction(gray)
            
            # Detect shadow regions
            shadow_regions = ShadowAnalyzer._detect_shadows(image)
            
            # Analyze shadow consistency
            shadow_consistency = ShadowAnalyzer._analyze_shadow_consistency(shadow_regions, gray)
            
            # Calculate overall consistency
            overall_consistency = (lighting_consistency + shadow_consistency) / 2.0
            
            # Calculate suspicious score
            suspicious_score = 0.0
            if overall_consistency < 0.6:
                suspicious_score += 0.6
            if lighting_consistency < 0.5:
                suspicious_score += 0.4
            
            return {
                "lighting_consistency": round(lighting_consistency, 3),
                "shadow_consistency": round(shadow_consistency, 3),
                "overall_consistency": round(overall_consistency, 3),
                "suspicious_score": min(suspicious_score, 1.0)
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "suspicious_score": 0.5
            }
    
    @staticmethod
    def _analyze_lighting_direction(gray_image):
        """Analyze consistency of lighting direction across the image"""
        # Calculate gradients
        grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate gradient magnitude and direction
        magnitude = np.sqrt(grad_x*2 + grad_y*2)
        direction = np.arctan2(grad_y, grad_x)
        
        # Focus on strong gradients (likely lighting boundaries)
        strong_gradients = magnitude > np.percentile(magnitude, 80)
        
        if np.sum(strong_gradients) < 100:  # Not enough gradients
            return 1.0
        
        # Analyze direction consistency
        directions = direction[strong_gradients]
        
        # Calculate circular variance (for angular data)
        mean_direction = np.arctan2(np.mean(np.sin(directions)), np.mean(np.cos(directions)))
        angular_variance = 1 - np.abs(np.mean(np.exp(1j * (directions - mean_direction))))
        
        consistency = 1.0 - angular_variance
        return max(0.0, min(1.0, consistency))
    
    @staticmethod
    def _detect_shadows(image):
        """Detect shadow regions in the image"""
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Shadow regions typically have low value (brightness)
        v_channel = hsv[:, :, 2]
        
        # Threshold to detect dark regions
        shadow_threshold = np.percentile(v_channel, 25)  # Bottom 25% as potential shadows
        shadow_mask = v_channel < shadow_threshold
        
        # Apply morphological operations to clean up
        kernel = np.ones((5, 5), np.uint8)
        shadow_mask = cv2.morphologyEx(shadow_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
        
        return shadow_mask
    
    @staticmethod
    def _analyze_shadow_consistency(shadow_mask, gray_image):
        """Analyze consistency of shadows"""
        if np.sum(shadow_mask) < 100:  # Not enough shadow regions
            return 1.0
        
        # Extract shadow regions
        shadow_regions = ShadowAnalyzer._extract_shadow_patches(shadow_mask, gray_image)
        
        if len(shadow_regions) < 2:
            return 1.0
        
        # Calculate intensity consistency in shadow regions
        intensities = [np.mean(region) for region in shadow_regions]
        intensity_std = np.std(intensities)
        intensity_mean = np.mean(intensities)
        
        # Normalize consistency score
        consistency = 1.0 - min(intensity_std / (intensity_mean + 1e-6), 1.0)
        
        return max(0.0, min(1.0, consistency))
    
    @staticmethod
    def _extract_shadow_patches(shadow_mask, gray_image, patch_size=32):
        """Extract patches from shadow regions"""
        patches = []
        h, w = shadow_mask.shape
        
        for i in range(0, h - patch_size, patch_size):
            for j in range(0, w - patch_size, patch_size):
                patch_mask = shadow_mask[i:i+patch_size, j:j+patch_size]
                if np.sum(patch_mask) > (patch_size * patch_size) * 0.3:  # At least 30% shadow
                    patch = gray_image[i:i+patch_size, j:j+patch_size]
                    patches.append(patch)
        
        return patches