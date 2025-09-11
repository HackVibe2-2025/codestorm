# services/operations.py

from PIL import Image
import os

# Import utilities that should always work
from utils.exif_utils import ExifAnalyzer
from utils.blur_utils import BlurAnalyzer
from utils.color_utils import analyze_color_distribution
from utils.noise_utils import NoiseAnalyzer
from utils.shadow_utils import ShadowAnalyzer
from utils.texture_utils import TextureAnalyzer

# Try to import AI model, but handle gracefully if not available
try:
    from models.hf_deepfake import HuggingFaceDeepfakeDetector
    HF_MODEL_AVAILABLE = True
    print("✅ AI model import successful")
except ImportError as e:
    print(f"⚠️ AI model not available - {e}")
    HF_MODEL_AVAILABLE = False
except Exception as e:
    print(f"⚠️ AI model failed to load - {e}")
    HF_MODEL_AVAILABLE = False

class DeepfakeAnalyzer:
    """Main deepfake analysis orchestrator"""
    
    def __init__(self):
        # Initialize AI model if available
        if HF_MODEL_AVAILABLE:
            try:
                print("🔄 Loading AI model...")
                self.hf_detector = HuggingFaceDeepfakeDetector()
                print("✅ AI model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to initialize AI model - {e}")
                self.hf_detector = None
        else:
            print("ℹ️ AI model not available - running without AI detection")
            self.hf_detector = None
            
        self.exif_analyzer = ExifAnalyzer()
        self.blur_analyzer = BlurAnalyzer()
        self.noise_analyzer = NoiseAnalyzer()
        self.shadow_analyzer = ShadowAnalyzer()
        self.texture_analyzer = TextureAnalyzer()
    
    def analyze_image(self, image_path):
        """
        Comprehensive image analysis for deepfake detection
        Returns: dict with all analysis results
        """
        try:
            # Load image
            pil_image = Image.open(image_path).convert('RGB')
            
            # Run all analyses
            results = {
                "file_path": image_path,
                "status": "success",
                "analyses": {}
            }
            
            # 1. Hugging Face deepfake detection
            if self.hf_detector:
                try:
                    hf_result = self.hf_detector.predict(image_path)
                    results["analyses"]["deepfake_detection"] = {
                        "operation": "AI Deepfake Detection",
                        "result": hf_result,
                        "flag": "Suspicious" if hf_result.get("label") == "fake" else "Passed",
                        "description": f"AI model predicts: {hf_result.get('label', 'unknown')} with {hf_result.get('score', 0)*100:.1f}% confidence"
                    }
                except Exception as e:
                    results["analyses"]["deepfake_detection"] = {
                        "operation": "AI Deepfake Detection",
                        "flag": "Error",
                        "description": f"AI analysis failed: {str(e)}"
                    }
            else:
                results["analyses"]["deepfake_detection"] = {
                    "operation": "AI Deepfake Detection",
                    "flag": "Skipped",
                    "description": "AI model not available - install transformers package for AI analysis"
                }
            
            # 2. EXIF metadata analysis
            try:
                exif_result = self.exif_analyzer.analyze_exif(image_path)
                results["analyses"]["exif_analysis"] = {
                    "operation": "EXIF Metadata Analysis",
                    "result": exif_result,
                    "flag": "Suspicious" if exif_result.get("suspicious_score", 0) > 0.5 else "Passed",
                    "description": f"EXIF data analysis - {len(exif_result.get('anomalies', []))} anomalies detected"
                }
            except Exception as e:
                results["analyses"]["exif_analysis"] = {
                    "operation": "EXIF Metadata Analysis",
                    "flag": "Error",
                    "description": f"EXIF analysis failed: {str(e)}"
                }
            
            # 3. Blur analysis
            try:
                blur_result = self.blur_analyzer.analyze_blur(image_path)
                results["analyses"]["blur_analysis"] = {
                    "operation": "Blur/Sharpness Analysis",
                    "result": blur_result,
                    "flag": "Suspicious" if blur_result.get("suspicious_score", 0) > 0.5 else "Passed",
                    "description": f"Sharpness consistency: {blur_result.get('sharpness_consistency', 0)*100:.1f}%"
                }
            except Exception as e:
                results["analyses"]["blur_analysis"] = {
                    "operation": "Blur/Sharpness Analysis",
                    "flag": "Error",
                    "description": f"Blur analysis failed: {str(e)}"
                }
            
            # 4. Color distribution analysis
            try:
                color_result = analyze_color_distribution(pil_image)
                results["analyses"]["color_analysis"] = color_result
            except Exception as e:
                results["analyses"]["color_analysis"] = {
                    "operation": "Color Distribution Analysis",
                    "flag": "Error",
                    "description": f"Color analysis failed: {str(e)}"
                }
            
            # 5. Noise analysis
            try:
                noise_result = self.noise_analyzer.analyze_noise(image_path)
                results["analyses"]["noise_analysis"] = {
                    "operation": "Noise Pattern Analysis",
                    "result": noise_result,
                    "flag": "Suspicious" if noise_result.get("suspicious_score", 0) > 0.5 else "Passed",
                    "description": f"Noise consistency: {noise_result.get('noise_consistency', 0)*100:.1f}%"
                }
            except Exception as e:
                results["analyses"]["noise_analysis"] = {
                    "operation": "Noise Pattern Analysis",
                    "flag": "Error",
                    "description": f"Noise analysis failed: {str(e)}"
                }
            
            # 6. Shadow/lighting analysis
            try:
                shadow_result = self.shadow_analyzer.analyze_shadows(image_path)
                results["analyses"]["shadow_analysis"] = {
                    "operation": "Lighting/Shadow Analysis",
                    "result": shadow_result,
                    "flag": "Suspicious" if shadow_result.get("suspicious_score", 0) > 0.5 else "Passed",
                    "description": f"Lighting consistency: {shadow_result.get('overall_consistency', 0)*100:.1f}%"
                }
            except Exception as e:
                results["analyses"]["shadow_analysis"] = {
                    "operation": "Lighting/Shadow Analysis",
                    "flag": "Error",
                    "description": f"Shadow analysis failed: {str(e)}"
                }
            
            # 7. Texture analysis
            try:
                texture_result = self.texture_analyzer.analyze_texture(image_path)
                results["analyses"]["texture_analysis"] = {
                    "operation": "Texture Consistency Analysis",
                    "result": texture_result,
                    "flag": "Suspicious" if texture_result.get("suspicious_score", 0) > 0.5 else "Passed",
                    "description": f"Texture consistency: {texture_result.get('texture_consistency', 0)*100:.1f}%"
                }
            except Exception as e:
                results["analyses"]["texture_analysis"] = {
                    "operation": "Texture Consistency Analysis",
                    "flag": "Error",
                    "description": f"Texture analysis failed: {str(e)}"
                }
            
            # Calculate overall confidence score
            results["overall_assessment"] = self._calculate_overall_score(results["analyses"])
            
            return results
            
        except Exception as e:
            return {
                "file_path": image_path,
                "status": "error",
                "error": str(e),
                "overall_assessment": {
                    "confidence_score": 0.0,
                    "is_likely_deepfake": False,
                    "recommendation": "Analysis failed - unable to determine authenticity"
                }
            }
    
    def _calculate_overall_score(self, analyses):
        """Calculate overall confidence and assessment"""
        suspicious_count = 0
        total_analyses = 0
        confidence_scores = []
        
        for analysis in analyses.values():
            if analysis.get("flag") == "Suspicious":
                suspicious_count += 1
            if analysis.get("flag") in ["Passed", "Suspicious"]:
                total_analyses += 1
            
            # Extract confidence scores where available
            result = analysis.get("result", {})
            if isinstance(result, dict):
                if "score" in result:
                    confidence_scores.append(result["score"])
                elif "suspicious_score" in result:
                    confidence_scores.append(1.0 - result["suspicious_score"])
        
        # Calculate overall confidence
        if total_analyses > 0:
            suspicion_ratio = suspicious_count / total_analyses
            base_confidence = 1.0 - suspicion_ratio
        else:
            base_confidence = 0.5
        
        # Adjust based on AI model confidence if available
        ai_result = analyses.get("deepfake_detection", {}).get("result", {})
        ai_flag = analyses.get("deepfake_detection", {}).get("flag", "Skipped")
        
        if ai_flag in ["Suspicious", "Passed"] and ai_result.get("raw_probabilities"):
            # Use raw probabilities for more accurate confidence calculation
            raw_probs = ai_result.get("raw_probabilities", {})
            real_prob = raw_probs.get("real", 0.5)
            fake_prob = raw_probs.get("fake", 0.5)
            
            # Authenticity confidence is the probability that image is real
            ai_authenticity_confidence = real_prob
            
            # Weight the AI model heavily since it's trained specifically for this task
            base_confidence = (base_confidence * 0.3) + (ai_authenticity_confidence * 0.7)
        elif ai_flag == "Suspicious" and ai_result.get("label") == "fake":
            # Fallback: If AI says "fake" with high confidence, lower our authenticity confidence
            fake_confidence = ai_result.get("score", 0.5)
            authentic_confidence = 1.0 - fake_confidence
            base_confidence = min(base_confidence, authentic_confidence)
        elif ai_flag == "Passed" and ai_result.get("label") == "real":
            # Fallback: If AI says "real" with high confidence, increase our authenticity confidence
            real_confidence = ai_result.get("score", 0.5)
            base_confidence = max(base_confidence, real_confidence)
        
        is_likely_deepfake = base_confidence < 0.5
        
        # 🔍 DEBUG: Add comprehensive logging for confidence calculation
        print(f"🔍 CONFIDENCE CALCULATION DEBUG:")
        print(f"  - Suspicious count: {suspicious_count}/{total_analyses}")
        print(f"  - Suspicion ratio: {suspicious_count / total_analyses if total_analyses > 0 else 'N/A'}")
        print(f"  - Base confidence (before AI): {1.0 - (suspicious_count / total_analyses) if total_analyses > 0 else 0.5}")
        print(f"  - AI result: {ai_result}")
        print(f"  - AI flag: {ai_flag}")
        print(f"  - Final base_confidence: {base_confidence}")
        print(f"  - is_likely_deepfake: {is_likely_deepfake}")
        print(f"  - Authenticity confidence: {base_confidence * 100:.1f}%")
        
        # Generate recommendation
        if base_confidence > 0.8:
            recommendation = "Image appears authentic with high confidence"
        elif base_confidence > 0.6:
            recommendation = "Image likely authentic but some minor inconsistencies detected"
        elif base_confidence > 0.4:
            recommendation = "Inconclusive - mixed indicators detected"
        elif base_confidence > 0.2:
            recommendation = "Image likely manipulated - multiple suspicious indicators"
        else:
            recommendation = "Image very likely deepfake - strong suspicious indicators"
        
        return {
            "confidence_score": round(base_confidence, 3),
            "is_likely_deepfake": is_likely_deepfake,
            "suspicious_analyses": suspicious_count,
            "total_analyses": total_analyses,
            "recommendation": recommendation
        }

def run_all_ops(pil_image: Image.Image):
    """
    Legacy function - runs all available operations on the image
    and returns a list of JSON results.
    """
    # This function is kept for backward compatibility
    # In practice, use DeepfakeAnalyzer.analyze_image() instead
    
    results = []

    # 1. Hugging Face deepfake detection
    if HF_MODEL_AVAILABLE:
        try:
            detector = HuggingFaceDeepfakeDetector()
            # Save temp file for analysis
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                pil_image.save(tmp.name)
                hf_result = detector.predict(tmp.name)
                os.unlink(tmp.name)
            
            results.append({
                "operation": "Deepfake Detection",
                "flag": "Suspicious" if hf_result.get("label") == "fake" else "Passed",
                "description": f"AI predicts: {hf_result.get('label')} ({hf_result.get('score', 0)*100:.1f}% confidence)"
            })
        except Exception as e:
            results.append({
                "operation": "Deepfake Detection",
                "flag": "Error",
                "description": f"Failed to run: {str(e)}"
            })
    else:
        results.append({
            "operation": "Deepfake Detection",
            "flag": "Skipped",
            "description": "AI model not available - install transformers package"
        })

    # 2. Color distribution analysis
    try:
        color_result = analyze_color_distribution(pil_image)
        results.append(color_result)
    except Exception as e:
        results.append({
            "operation": "Color Analysis",
            "flag": "Error",
            "description": f"Failed to run: {str(e)}"
        })

    return results
