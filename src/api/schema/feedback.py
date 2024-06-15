from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackView(BaseModel):
    id: int
    content: str
    created_at: datetime
    star: Optional[float] = None
    owner: Optional[str] = None
    event: int
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    content: str
    star: float
    event: int 

class FeedbackUpdate(BaseModel):
    content: Optional[str] = None
    star: Optional[float] = None