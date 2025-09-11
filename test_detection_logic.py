#!/usr/bin/env python3
"""
Test script to verify deepfake detection logic is working correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.operations import DeepfakeAnalyzer
import json

def test_analysis_logic():
    """Test the analysis logic with mock data"""
    
    print("🧪 Testing DeepfakeAnalyzer confidence calculation logic")
    print("=" * 60)
    
    analyzer = DeepfakeAnalyzer()
    
    # Test Case 1: Mock analysis where AI predicts REAL with high confidence
    print("\n📋 TEST CASE 1: AI predicts REAL with high confidence")
    mock_analyses_real = {
        "deepfake_detection": {
            "flag": "Passed",
            "result": {
                "label": "real",
                "score": 0.92,
                "raw_probabilities": {
                    "real": 0.92,
                    "fake": 0.08
                }
            }
        },
        "texture_analysis": {"flag": "Passed"},
        "shadow_analysis": {"flag": "Passed"},
        "blur_analysis": {"flag": "Passed"}
    }
    
    result_real = analyzer._calculate_overall_score(mock_analyses_real)
    print(f"  ✅ Result: {result_real}")
    print(f"  ✅ is_likely_deepfake: {result_real['is_likely_deepfake']} (should be False)")
    print(f"  ✅ confidence_score: {result_real['confidence_score']:.3f} (should be high, >0.8)")
    
    # Test Case 2: Mock analysis where AI predicts FAKE with high confidence
    print("\n📋 TEST CASE 2: AI predicts FAKE with high confidence")
    mock_analyses_fake = {
        "deepfake_detection": {
            "flag": "Suspicious",
            "result": {
                "label": "fake",
                "score": 0.89,
                "raw_probabilities": {
                    "real": 0.11,
                    "fake": 0.89
                }
            }
        },
        "texture_analysis": {"flag": "Suspicious"},
        "shadow_analysis": {"flag": "Suspicious"},
        "blur_analysis": {"flag": "Passed"}
    }
    
    result_fake = analyzer._calculate_overall_score(mock_analyses_fake)
    print(f"  ⚠️ Result: {result_fake}")
    print(f"  ⚠️ is_likely_deepfake: {result_fake['is_likely_deepfake']} (should be True)")
    print(f"  ⚠️ confidence_score: {result_fake['confidence_score']:.3f} (should be low, <0.5)")
    
    # Test Case 3: Mixed signals
    print("\n📋 TEST CASE 3: Mixed signals (AI says real, but other analyses suspicious)")
    mock_analyses_mixed = {
        "deepfake_detection": {
            "flag": "Passed",
            "result": {
                "label": "real",
                "score": 0.75,
                "raw_probabilities": {
                    "real": 0.75,
                    "fake": 0.25
                }
            }
        },
        "texture_analysis": {"flag": "Suspicious"},
        "shadow_analysis": {"flag": "Suspicious"},
        "blur_analysis": {"flag": "Suspicious"},
        "noise_analysis": {"flag": "Passed"}
    }
    
    result_mixed = analyzer._calculate_overall_score(mock_analyses_mixed)
    print(f"  🤔 Result: {result_mixed}")
    print(f"  🤔 is_likely_deepfake: {result_mixed['is_likely_deepfake']}")
    print(f"  🤔 confidence_score: {result_mixed['confidence_score']:.3f}")
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    print(f"  📊 Test 1 (Real Image): confidence={result_real['confidence_score']:.3f}, deepfake={result_real['is_likely_deepfake']}")
    print(f"  📊 Test 2 (Fake Image): confidence={result_fake['confidence_score']:.3f}, deepfake={result_fake['is_likely_deepfake']}")
    print(f"  📊 Test 3 (Mixed): confidence={result_mixed['confidence_score']:.3f}, deepfake={result_mixed['is_likely_deepfake']}")
    
    # Validate expectations
    success = True
    if result_real['is_likely_deepfake'] != False:
        print("  ❌ FAILED: Real image test should have is_likely_deepfake=False")
        success = False
    if result_fake['is_likely_deepfake'] != True:
        print("  ❌ FAILED: Fake image test should have is_likely_deepfake=True")
        success = False
    if result_real['confidence_score'] < 0.6:
        print("  ❌ FAILED: Real image should have high confidence (>0.6)")
        success = False
    if result_fake['confidence_score'] > 0.4:
        print("  ❌ FAILED: Fake image should have low confidence (<0.4)")
        success = False
    
    if success:
        print("  ✅ ALL TESTS PASSED! Logic is working correctly.")
    else:
        print("  ❌ SOME TESTS FAILED! Check the logic.")
    
    return success

if __name__ == "__main__":
    test_analysis_logic()
