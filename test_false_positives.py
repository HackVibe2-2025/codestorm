#!/usr/bin/env python3
"""
Real-world test for false positive detection
Tests with actual image files to identify false positive issues
"""

import os
import sys
import requests
from PIL import Image, ImageDraw
import tempfile
import time

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.operations import DeepfakeAnalyzer

def create_test_real_image():
    """Create a simple, obviously real image"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face-like pattern
    # Face outline
    draw.ellipse([50, 50, 250, 250], outline='black', width=3)
    # Eyes
    draw.ellipse([80, 100, 120, 140], fill='black')
    draw.ellipse([180, 100, 220, 140], fill='black')
    # Nose
    draw.line([150, 140, 150, 180], fill='black', width=3)
    # Mouth
    draw.arc([100, 180, 200, 220], start=0, end=180, fill='black', width=3)
    
    return img

def create_test_photo_like_image():
    """Create a more photo-like image"""
    img = Image.new('RGB', (400, 400), color=(240, 220, 200))  # Skin-like color
    draw = ImageDraw.Draw(img)
    
    # Add some texture/noise to make it more realistic
    import random
    for _ in range(1000):
        x = random.randint(0, 399)
        y = random.randint(0, 399)
        color_var = random.randint(-20, 20)
        new_color = (
            max(0, min(255, 240 + color_var)),
            max(0, min(255, 220 + color_var)),
            max(0, min(255, 200 + color_var))
        )
        draw.point((x, y), fill=new_color)
    
    return img

def test_real_world_images():
    """Test with various types of images to identify false positive patterns"""
    print("🧪 REAL-WORLD FALSE POSITIVE ANALYSIS")
    print("=" * 60)
    
    analyzer = DeepfakeAnalyzer()
    
    test_cases = [
        {
            "name": "Simple Drawn Image",
            "image": create_test_real_image(),
            "expected": "Should be authentic (simple drawing)"
        },
        {
            "name": "Photo-like Synthetic",
            "image": create_test_photo_like_image(),
            "expected": "Might trigger some alerts but should lean authentic"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 TEST CASE {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected']}")
        print("-" * 40)
        
        # Save test image temporarily
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            test_case['image'].save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Analyze the image
            result = analyzer.analyze_image(tmp_path)
            
            overall = result.get('overall_assessment', {})
            confidence = overall.get('confidence_score', 0)
            is_deepfake = overall.get('is_likely_deepfake', False)
            recommendation = overall.get('recommendation', 'Unknown')
            
            print(f"🎯 RESULT:")
            print(f"  Confidence: {confidence*100:.1f}%")
            print(f"  Is Deepfake: {is_deepfake}")
            print(f"  Recommendation: {recommendation}")
            
            # Analyze which specific tests flagged as suspicious
            analyses = result.get('analyses', {})
            suspicious_tests = []
            for test_name, test_result in analyses.items():
                if test_result.get('flag') == 'Suspicious':
                    suspicious_tests.append({
                        'test': test_name,
                        'description': test_result.get('description', 'No description')
                    })
            
            if suspicious_tests:
                print(f"⚠️  SUSPICIOUS FLAGS ({len(suspicious_tests)}):")
                for flag in suspicious_tests:
                    print(f"    - {flag['test']}: {flag['description']}")
            else:
                print("✅ No suspicious flags")
            
            # Check for potential false positive
            if is_deepfake and test_case['name'] in ['Simple Drawn Image']:
                print("🚨 POTENTIAL FALSE POSITIVE DETECTED!")
                print("   This simple drawing should not be flagged as deepfake")
            
            results.append({
                'name': test_case['name'],
                'confidence': confidence,
                'is_deepfake': is_deepfake,
                'suspicious_count': len(suspicious_tests),
                'suspicious_tests': suspicious_tests
            })
            
        except Exception as e:
            print(f"❌ Error analyzing {test_case['name']}: {e}")
            results.append({
                'name': test_case['name'],
                'error': str(e)
            })
        
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    # Summary analysis
    print(f"\n📊 SUMMARY ANALYSIS")
    print("=" * 60)
    
    false_positives = [r for r in results if r.get('is_deepfake') and 'Simple' in r.get('name', '')]
    high_suspicious_count = [r for r in results if r.get('suspicious_count', 0) > 2]
    
    if false_positives:
        print(f"🚨 FALSE POSITIVES DETECTED: {len(false_positives)}")
        for fp in false_positives:
            print(f"   - {fp['name']}: {fp['confidence']*100:.1f}% confidence")
    else:
        print("✅ No clear false positives detected")
    
    if high_suspicious_count:
        print(f"\n⚠️  HIGH SUSPICIOUS FLAG COUNT:")
        for case in high_suspicious_count:
            print(f"   - {case['name']}: {case['suspicious_count']} suspicious flags")
            if case.get('suspicious_tests'):
                for test in case['suspicious_tests'][:3]:  # Show first 3
                    print(f"     * {test['test']}")
    
    # Recommendations for fixing false positives
    print(f"\n💡 RECOMMENDATIONS:")
    print("1. Adjust thresholds for synthetic/drawn images")
    print("2. Add metadata-based filtering (check for digital art indicators)")
    print("3. Implement confidence weighting based on image characteristics")
    print("4. Consider excluding obviously non-photographic images")
    
    return results

if __name__ == "__main__":
    try:
        results = test_real_world_images()
        print(f"\n✅ Test completed successfully")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
