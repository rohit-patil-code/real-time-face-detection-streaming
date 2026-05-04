from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Face Detection Video Streaming API"
    API_V1_STR: str = "/api/v1"
    
    UPLOAD_DIR: Path = Path("temp_uploads")

    class Config:
        env_file = ".env"

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
