from pydantic import BaseModel
from datetime import datetime

class ROIBase(BaseModel):
    x: int
    y: int
    width: int
    height: int

class ROICreate(ROIBase):
    pass

class ROIResponse(ROIBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
