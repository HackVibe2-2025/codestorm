# models/hf_deepfake.py
# ===============================

from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

class HuggingFaceDeepfakeDetector:
    """Hugging Face deepfake detection model wrapper"""
    
    def __init__(self, model_name="prithivMLmods/deepfake-detector-model-v1"):
        self.model_name = model_name
        self.processor = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model and processor"""
        try:
            self.processor = AutoImageProcessor.from_pretrained(self.model_name)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
            print(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    
    def predict(self, image_path):
        """
        Predict if image is real or fake
        Returns: dict with label and confidence score
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            inputs = self.processor(image, return_tensors="pt")
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get predicted class and confidence
            predicted_class_id = outputs.logits.argmax().item()
            confidence = probabilities[0][predicted_class_id].item()
            
            # Map to human readable labels
            label_mapping = {0: "real", 1: "fake"}
            predicted_label = label_mapping.get(predicted_class_id, "unknown")
            
            return {
                "label": predicted_label,
                "score": round(confidence, 4),
                "raw_probabilities": {
                    "real": round(probabilities[0][0].item(), 4),
                    "fake": round(probabilities[0][1].item(), 4)
                }
            }
        
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "label": "unknown",
                "score": 0.0
            }