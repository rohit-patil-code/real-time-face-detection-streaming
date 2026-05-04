from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from app.db.base import Base

class ROI(Base):
    __tablename__ = "rois"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    x = Column(Integer)
    y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
