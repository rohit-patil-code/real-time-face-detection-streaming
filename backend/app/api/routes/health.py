from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=dict)
def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "ok", "message": "Service is healthy"}
