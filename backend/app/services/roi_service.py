from sqlalchemy.orm import Session
from app.models.roi import ROI
from app.schemas.roi import ROICreate

def create_roi(db: Session, roi: ROICreate) -> ROI:
    """
    Save a new ROI into the database.
    """
    db_roi = ROI(**roi.model_dump())
    db.add(db_roi)
    db.commit()
    db.refresh(db_roi)
    return db_roi

def get_latest_rois(db: Session, limit: int = 10) -> list[ROI]:
    """
    Retrieve the latest ROIs from the database.
    """
    return db.query(ROI).order_by(ROI.timestamp.desc()).limit(limit).all()
