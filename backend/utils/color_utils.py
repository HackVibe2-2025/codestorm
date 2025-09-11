# utils/color_utils.py

import cv2
import numpy as np
from PIL import Image

def analyze_color_distribution(pil_image: Image.Image):
    """
    Analyzes color distribution of the image.
    Returns JSON with flag + description.
    """

    # Convert to OpenCV format (BGR)
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Compute histogram for each channel
    hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

    # Normalize histograms
    hist_b /= hist_b.sum()
    hist_g /= hist_g.sum()
    hist_r /= hist_r.sum()

    # Calculate mean intensity of each channel
    mean_b, mean_g, mean_r = hist_b.mean(), hist_g.mean(), hist_r.mean()

    # Simple heuristic: check if one channel dominates
    max_mean = max(mean_b, mean_g, mean_r)
    min_mean = min(mean_b, mean_g, mean_r)
    color_balance = max_mean - min_mean

    if color_balance > 0.05:
        flag = "Anomaly"
        description = "Unnatural color balance detected (one channel dominates)."
    else:
        flag = "Passed"
        description = "Color distribution looks natural."

    return {
        "operation": "Color/Histogram Analysis",
        "flag": flag,
        "description": description
    }
