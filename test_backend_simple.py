import requests
import time

def test_backend():
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get('http://localhost:5000/health')
        print(f"Health status: {response.status_code}")
        print(f"Health response: {response.text}")

        # Test detect endpoint with a simple image
        print("\nTesting detect endpoint...")
        with open(r'c:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\frontend\test_image.jpg', 'rb') as f:
            files = {'image': ('test.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:5000/detect?format=summary', files=files)
            print(f"Detect status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Backend is working correctly!")
            else:
                print(f"❌ Backend error: {response.text}")

    except Exception as e:
        print(f"❌ Error testing backend: {e}")

if __name__ == "__main__":
    test_backend()
