# exif_utils.py - EXIF Metadata Analysis for Deepfake Detection
# ===============================

from PIL import Image
from PIL.ExifTags import TAGS
import json

class ExifAnalyzer:
    """EXIF metadata analysis for deepfake detection"""
    
    @staticmethod
    def analyze_exif(image_path):
        """Analyze EXIF data for anomalies"""
        try:
            image = Image.open(image_path)
            exif_dict = {}
            
            # Extract EXIF data
            exif_data = image.getexif()
            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_dict[tag] = str(value)
            
            # Analyze for suspicious patterns
            anomalies = ExifAnalyzer._detect_anomalies(exif_dict)
            
            return {
                "has_exif": len(exif_dict) > 0,
                "exif_count": len(exif_dict),
                "anomalies": anomalies,
                "suspicious_score": len(anomalies) / 10.0,  # Normalize to 0-1
                "metadata": exif_dict
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "has_exif": False,
                "suspicious_score": 0.5  # Unknown, moderate suspicion
            }
    
    @staticmethod
    def _detect_anomalies(exif_dict):
        """Detect common anomalies in EXIF data"""
        anomalies = []
        
        # Check for missing common fields
        common_fields = ['DateTime', 'Software', 'Make', 'Model']
        missing_fields = [field for field in common_fields if field not in exif_dict]
        if len(missing_fields) > 2:
            anomalies.append(f"Missing common EXIF fields: {missing_fields}")
        
        # Check for suspicious software signatures
        if 'Software' in exif_dict:
            software = exif_dict['Software'].lower()
            suspicious_software = ['photoshop', 'gimp', 'deepfake', 'faceswap', 'ai']
            if any(sus in software for sus in suspicious_software):
                anomalies.append(f"Suspicious software detected: {exif_dict['Software']}")
        
        # Check for inconsistent timestamps
        if 'DateTime' in exif_dict and 'DateTimeOriginal' in exif_dict:
            if exif_dict['DateTime'] != exif_dict['DateTimeOriginal']:
                anomalies.append("Timestamp inconsistency detected")
        
        return anomalies

# Legacy function for backward compatibility
def analyze_exif(image_path):
    """Legacy function - use ExifAnalyzer.analyze_exif() instead"""
    return ExifAnalyzer.analyze_exif(image_path)