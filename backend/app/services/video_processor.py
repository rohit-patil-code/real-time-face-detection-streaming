import imageio
import numpy as np
from typing import Generator
from app.services.face_detection import detect_faces
from app.services.image_utils import draw_boxes

def extract_frames(video_path: str) -> Generator[np.ndarray, None, None]:
    """
    Read a video file frame by frame using imageio (ffmpeg), without OpenCV.
    """
    reader = imageio.get_reader(video_path, 'ffmpeg')
    for frame in reader:
        yield frame
    reader.close()

def process_video(video_path: str) -> Generator[np.ndarray, None, None]:
    """
    Pipeline to process a video file frame by frame:
    - extracts frames
    - detects faces
    - draws bounding box using Pillow
    
    Yields the processed frames as numpy arrays.
    """
    for frame in extract_frames(video_path):
        # 1. Detect faces
        boxes = detect_faces(frame)
        
        # 2. Draw bounding boxes
        if boxes:
            # We assume one face per frame as per the requirement
            processed_frame = draw_boxes(frame, boxes[:1])
        else:
            processed_frame = frame
            
        # 3. Yield the processed frame
        yield processed_frame
