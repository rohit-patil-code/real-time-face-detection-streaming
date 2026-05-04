import os
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from app.services.streaming import generate_video_stream
from app.core.config import settings

router = APIRouter()

@router.get("/stream")
def stream_video(
    filename: str = Query(..., description="Name of the ingested video file"),
    t: str = Query(None, description="Cache-busting timestamp")
):
    """
    Stream a processed video using MJPEG.
    Browser compatible endpoint: <img src="/api/v1/stream?filename=video.mp4&t=123" />
    """
    video_path = settings.UPLOAD_DIR / filename
    
    # Simple validation to prevent path traversal
    if ".." in filename or filename.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid filename format")
        
    if not video_path.exists() or not video_path.is_file():
        raise HTTPException(status_code=404, detail=f"Video file '{filename}' not found. Please /ingest it first.")
        
    # StreamingResponse with a synchronous generator automatically runs in a threadpool in FastAPI,
    # ensuring the main async loop is not blocked by the CPU-intensive video processing.
    return StreamingResponse(
        generate_video_stream(str(video_path)),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
