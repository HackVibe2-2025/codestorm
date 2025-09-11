import base64
from PIL import Image
import io

# Create a simple test image
img = Image.new('RGB', (100, 100), color='red')
buffer = io.BytesIO()
img.save(buffer, format='JPEG')
buffer.seek(0)

# Save the image to the frontend folder for easy testing
with open(r'c:\Users\BHANU TEJA GUPTA V\Downloads\DeepScan\frontend\test_image.jpg', 'wb') as f:
    f.write(buffer.getvalue())

print("Test image created at: c:\\Users\\BHANU TEJA GUPTA V\\Downloads\\DeepScan\\frontend\\test_image.jpg")
