import io
import time
from typing import Generator
from PIL import Image
import numpy as np
import imageio
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
    # Dynamically extract original video FPS to match native playback speed
    try:
        reader = imageio.get_reader(video_path, 'ffmpeg')
        target_fps = reader.get_meta_data().get('fps', 30)
        reader.close()
    except Exception:
        target_fps = 30

    frame_duration = 1.0 / target_fps
    next_frame_time = time.time()
    
    try:
        for processed_frame in process_video(video_path):
            jpeg_bytes = encode_frame_to_jpeg(processed_frame)
            
            # Yield in multipart/x-mixed-replace format for MJPEG streaming
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n"
            )
            
            # Advance the target time for the next frame
            next_frame_time += frame_duration
            
            # Sleep only if we are ahead of schedule (this accounts for ALL processing time, 
            # including the time taken inside process_video)
            sleep_time = next_frame_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # If processing was too slow, reset the clock to prevent fast-forward "catch-up" bursts
                next_frame_time = time.time()
                
    except Exception as e:
        # Logging standard streaming errors
        print(f"Error during video streaming: {e}")
