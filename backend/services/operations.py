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
        """Calculate overall confidence and assessment with false positive reduction"""
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
        
        # Calculate base confidence from traditional analyses
        if total_analyses > 0:
            suspicion_ratio = suspicious_count / total_analyses
            base_confidence = 1.0 - suspicion_ratio
        else:
            base_confidence = 0.5
        
        # Get AI analysis results
        ai_result = analyses.get("deepfake_detection", {}).get("result", {})
        ai_flag = analyses.get("deepfake_detection", {}).get("flag", "Skipped")
        
        # 🔧 ENHANCED FALSE POSITIVE REDUCTION
        # Check if this might be a non-photographic image (drawing, artwork, etc.)
        is_likely_synthetic_art = self._detect_synthetic_artwork(analyses)
        
        if ai_flag in ["Suspicious", "Passed"] and ai_result.get("raw_probabilities"):
            # Use raw probabilities for more accurate confidence calculation
            raw_probs = ai_result.get("raw_probabilities", {})
            real_prob = raw_probs.get("real", 0.5)
            fake_prob = raw_probs.get("fake", 0.5)
            
            # 🎯 ANTI-FALSE-POSITIVE LOGIC
            if is_likely_synthetic_art:
                print("🎨 Detected synthetic artwork - applying false positive reduction")
                # For synthetic art, be much more conservative with AI predictions
                if ai_flag == "Suspicious" and fake_prob < 0.85:  # Only flag if AI is very confident
                    print(f"   📝 AI confidence {fake_prob:.3f} too low for artwork - treating as authentic")
                    real_prob = max(real_prob, 0.7)  # Boost authenticity for artwork
                elif ai_flag == "Passed":
                    real_prob = max(real_prob, 0.8)  # Strongly favor authentic for artwork
            
            # Weight AI model based on confidence and image type
            if is_likely_synthetic_art:
                # Reduce AI weight for synthetic artwork
                ai_weight = 0.4  # Reduced from 0.7
                traditional_weight = 0.6
            else:
                # Normal weighting for photographic images
                ai_weight = 0.7
                traditional_weight = 0.3
            
            # Calculate weighted confidence
            ai_authenticity_confidence = real_prob
            base_confidence = (base_confidence * traditional_weight) + (ai_authenticity_confidence * ai_weight)
            
        elif ai_flag == "Suspicious" and ai_result.get("label") == "fake":
            # Fallback handling for non-raw probability results
            fake_confidence = ai_result.get("score", 0.5)
            
            if is_likely_synthetic_art and fake_confidence < 0.85:
                print(f"🎨 Artwork with low AI confidence ({fake_confidence:.3f}) - treating as authentic")
                base_confidence = max(base_confidence, 0.7)
            else:
                authentic_confidence = 1.0 - fake_confidence
                base_confidence = min(base_confidence, authentic_confidence)
                
        elif ai_flag == "Passed" and ai_result.get("label") == "real":
            # Boost confidence for AI-verified real images
            real_confidence = ai_result.get("score", 0.5)
            if is_likely_synthetic_art:
                real_confidence = max(real_confidence, 0.8)  # Extra boost for artwork
            base_confidence = max(base_confidence, real_confidence)
        
        # 🛡️ FINAL ANTI-FALSE-POSITIVE SAFEGUARDS
        # If only AI flagged as suspicious and it's likely artwork, be lenient
        if (suspicious_count == 1 and ai_flag == "Suspicious" and 
            is_likely_synthetic_art and base_confidence > 0.4):
            print("🛡️ Final safeguard: Only AI suspicious on artwork - boosting confidence")
            base_confidence = max(base_confidence, 0.6)
        
        is_likely_deepfake = base_confidence < 0.5
        
        # 🔍 DEBUG: Add comprehensive logging for confidence calculation
        print(f"🔍 CONFIDENCE CALCULATION DEBUG:")
        print(f"  - Suspicious count: {suspicious_count}/{total_analyses}")
        print(f"  - Suspicion ratio: {suspicious_count / total_analyses if total_analyses > 0 else 'N/A'}")
        print(f"  - Base confidence (before AI): {1.0 - (suspicious_count / total_analyses) if total_analyses > 0 else 0.5}")
        print(f"  - AI result: {ai_result}")
        print(f"  - AI flag: {ai_flag}")
        print(f"  - Is likely synthetic art: {is_likely_synthetic_art}")
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
            "recommendation": recommendation,
            "is_synthetic_artwork": is_likely_synthetic_art
        }
    
    def _detect_synthetic_artwork(self, analyses):
        """Detect if image is likely synthetic artwork/drawing rather than photography"""
        indicators = 0
        
        # Check texture analysis - artwork often has more uniform textures
        texture_result = analyses.get("texture_analysis", {}).get("result", {})
        if texture_result.get("texture_features", {}).get("uniformity", 0) > 0.7:
            indicators += 1
        
        # Check color analysis - digital art often has different color distributions
        color_result = analyses.get("color_analysis", {}).get("result", {})
        if color_result and isinstance(color_result, dict):
            # Simple heuristic: digital art often has very even color distributions
            color_variance = color_result.get("color_variance", 0.5)
            if color_variance < 0.3:  # Very low variance suggests artificial colors
                indicators += 1
        
        # Check EXIF data - digital artwork often lacks camera metadata
        exif_result = analyses.get("exif_analysis", {}).get("result", {})
        has_camera_info = bool(exif_result.get("camera_info"))
        if not has_camera_info:
            indicators += 1
        
        # Check blur analysis - drawings often have consistent sharpness
        blur_result = analyses.get("blur_analysis", {}).get("result", {})
        sharpness_consistency = blur_result.get("sharpness_consistency", 0)
        if sharpness_consistency > 0.9:  # Very consistent sharpness
            indicators += 1
        
        # Consider it synthetic artwork if multiple indicators present
        is_artwork = indicators >= 2
        
        if is_artwork:
            print(f"🎨 Synthetic artwork detected - indicators: {indicators}/4")
        
        return is_artwork

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
