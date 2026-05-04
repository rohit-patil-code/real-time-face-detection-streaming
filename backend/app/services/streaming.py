import io
import time
from typing import Generator
from PIL import Image
import numpy as np
from app.services.video_processor import process_video

def encode_frame_to_jpeg(frame: np.ndarray) -> bytes:
    """
    Convert a numpy array frame to JPEG bytes using Pillow.
    """
    image = Image.fromarray(frame)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()

def generate_video_stream(video_path: str) -> Generator[bytes, None, None]:
    """
    Generator that processes the video frame-by-frame and yields 
    MJPEG formatted frames with framerate control.
    """
    target_fps = 24
    frame_duration = 1.0 / target_fps
    
    try:
        for processed_frame in process_video(video_path):
            start_time = time.time()
            
            jpeg_bytes = encode_frame_to_jpeg(processed_frame)
            
            # Yield in multipart/x-mixed-replace format for MJPEG streaming
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n"
            )
            
            # Control playback speed by sleeping the remainder of the frame duration
            elapsed_time = time.time() - start_time
            sleep_time = frame_duration - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except Exception as e:
        # Logging standard streaming errors
        print(f"Error during video streaming: {e}")
