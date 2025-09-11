import requests
import os

# Test the detect endpoint with a simple test
def test_detect_endpoint():
    # Create a small test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    files = {'image': ('test.png', test_image_data, 'image/png')}
    
    try:
        response = requests.post('http://localhost:5000/detect?format=summary', files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Backend API is working!")
        else:
            print("❌ Backend API returned error")
            
    except Exception as e:
        print(f"❌ Error calling backend: {e}")

if __name__ == "__main__":
    test_detect_endpoint()
