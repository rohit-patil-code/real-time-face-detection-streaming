import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from app.api.router import api_router
from app.core.config import settings

# Initialize Database tables
from app.db.session import engine
from app.db.base import Base
from app.models.roi import ROI
Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    @application.get("/", response_class=HTMLResponse, tags=["frontend"])
    def serve_frontend():
        """Serve the minimal HTML frontend for testing."""
        html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
        with open(html_path, "r") as f:
            return f.read()
            
    return application

app = get_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
