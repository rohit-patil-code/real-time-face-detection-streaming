from fastapi import APIRouter, File, UploadFile
from app.services import video_service

router = APIRouter()

@router.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    """
    Endpoint to ingest a video file, validate its type, and save it temporarily to disk.
    """
    file_path = await video_service.save_video_file(file)
    return {
        "status": "success",
        "message": "Video uploaded successfully",
        "file_path": file_path
    }
