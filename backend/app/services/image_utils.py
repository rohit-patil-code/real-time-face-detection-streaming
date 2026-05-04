import numpy as np
from PIL import Image, ImageDraw

def draw_boxes(frame: np.ndarray, boxes: list[tuple[int, int, int, int]]) -> np.ndarray:
    """
    Draw bounding boxes on a frame.
    
    Args:
        frame: A numpy array representing the image (in RGB format).
        boxes: List of bounding boxes in (top, right, bottom, left) format.
        
    Returns:
        A new numpy array with boxes drawn.
    """
    # Convert numpy array to a Pillow Image to draw
    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    
    for box in boxes:
        top, right, bottom, left = box
        # Pillow's draw.rectangle expects [x0, y0, x1, y1] -> [left, top, right, bottom]
        draw.rectangle([left, top, right, bottom], outline="red", width=3)
        
    # Convert back to numpy array
    return np.array(image)
