import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings

ALLOWED_EXTENSIONS = {".mp4", ".avi"}

async def save_video_file(file: UploadFile) -> str:
    """
    Validates the file extension and saves the file to the temporary upload directory.
    """
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: '{file_ext}'. Only {', '.join(ALLOWED_EXTENSIONS)} are allowed."
        )

    file_path = settings.UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        file.file.close()

    return str(file_path.absolute())
