import requests

# Test the exact API call that the frontend makes
def test_frontend_backend_integration():
    # Open the test image
    with open(r'c:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\frontend\test_image.jpg', 'rb') as f:
        files = {'image': ('test_image.jpg', f, 'image/jpeg')}
        
        try:
            print("Making API call to backend (same as frontend)...")
            response = requests.post('http://localhost:5000/detect?format=summary', files=files)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success! Backend returned:")
                print(f"  - Status: {result.get('status')}")
                print(f"  - Is Deepfake: {result.get('summary', {}).get('is_deepfake')}")
                print(f"  - Score: {result.get('summary', {}).get('score')}")
                print("✅ Frontend-Backend integration working!")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error calling backend: {e}")
            return False

if __name__ == "__main__":
    test_frontend_backend_integration()
