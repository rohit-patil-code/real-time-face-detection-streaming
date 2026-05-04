import os
import urllib.request
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Define the model path and URL
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "blaze_face_short_range.tflite")

# Download the model automatically if it doesn't exist
if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# Initialize the face detection model once at the module level for efficiency.
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceDetectorOptions(base_options=base_options, min_detection_confidence=0.5)
face_detection_model = vision.FaceDetector.create_from_options(options)

def detect_faces(frame: np.ndarray) -> list[tuple[int, int, int, int]]:
    """
    Detect faces in a given frame/image using MediaPipe Tasks API.
    
    Args:
        frame: A numpy array representing the image (in RGB format).
        
    Returns:
        A list of bounding boxes for each face found. 
        Format: (top, right, bottom, left).
    """
    bounding_boxes = []
    
    # Ensure the frame is a contiguous array, as MediaPipe requires it
    if not frame.flags['C_CONTIGUOUS']:
        frame = np.ascontiguousarray(frame)
        
    # MediaPipe Tasks API requires a MediaPipe Image object
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    
    # Process the frame
    results = face_detection_model.detect(mp_image)
    
    if results.detections:
        frame_height, frame_width = frame.shape[:2]
        
        for detection in results.detections:
            bbox = detection.bounding_box
            
            # The Tasks API returns absolute coordinates directly via origin_x, origin_y, width, and height.
            # We ensure the bounding boxes don't fall outside the frame dimensions.
            top = max(0, bbox.origin_y)
            left = max(0, bbox.origin_x)
            bottom = min(frame_height, bbox.origin_y + bbox.height)
            right = min(frame_width, bbox.origin_x + bbox.width)
            
            # Append in the requested format
            bounding_boxes.append((top, right, bottom, left))
            
    return bounding_boxes
