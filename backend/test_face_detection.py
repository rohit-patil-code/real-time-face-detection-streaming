import sys
import os
import numpy as np
from PIL import Image

# Add the parent directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.face_detection import detect_faces

def run_test():
    # You can place any test image named 'test_image.jpg' in the backend folder
    test_image_path = "test_image.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Error: Please place an image named '{test_image_path}' in the backend directory to test.")
        return

    print(f"Loading image '{test_image_path}'...")
    try:
        # Load the image using PIL (to avoid OpenCV entirely) and convert to RGB numpy array
        image = Image.open(test_image_path).convert("RGB")
        frame = np.array(image)
        
        print("Detecting faces...")
        # Get bounding boxes
        bounding_boxes = detect_faces(frame)
        
        print(f"✅ Found {len(bounding_boxes)} face(s) in the image!")
        for i, box in enumerate(bounding_boxes):
            print(f"   Face {i+1} bounding box: {box} (top, right, bottom, left)")
            
    except Exception as e:
        print(f"❌ An error occurred during face detection: {e}")

if __name__ == "__main__":
    run_test()
