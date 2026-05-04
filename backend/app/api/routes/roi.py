from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.roi import ROIResponse
from app.services.roi_service import get_latest_rois

router = APIRouter()

@router.get("/roi", response_model=list[ROIResponse])
def get_roi_data(limit: int = Query(10, description="Number of latest ROIs to return"), db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the latest Region of Interest (ROI) data.
    """
    return get_latest_rois(db, limit=limit)
