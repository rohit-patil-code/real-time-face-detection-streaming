import imageio
import numpy as np
from typing import Generator
from app.services.face_detection import detect_faces
from app.services.image_utils import draw_boxes
from app.db.session import SessionLocal
from app.schemas.roi import ROICreate
from app.services.roi_service import create_roi

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
    - saves ROI to database
    - draws bounding box using Pillow
    
    Yields the processed frames as numpy arrays.
    """
    # Create an independent DB session for this streaming process
    db = SessionLocal()
    try:
        for frame in extract_frames(video_path):
            # 1. Detect faces
            boxes = detect_faces(frame)
            
            # 2. Store ROI and Draw bounding boxes
            if boxes:
                # We assume one face per frame as per the requirement
                box = boxes[0]
                top, right, bottom, left = box
                
                # Convert (top, right, bottom, left) to (x, y, width, height)
                x = left
                y = top
                width = right - left
                height = bottom - top
                
                # Save ROI data to DB
                roi_data = ROICreate(x=x, y=y, width=width, height=height)
                create_roi(db, roi_data)
                
                # Draw box
                processed_frame = draw_boxes(frame, [box])
            else:
                processed_frame = frame
                
            # 3. Yield the processed frame
            yield processed_frame
    finally:
        # Ensure DB connection is closed when the generator is consumed or stops
        db.close()
