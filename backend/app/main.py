import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

def get_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

app = get_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
