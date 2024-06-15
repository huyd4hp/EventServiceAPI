from pydantic import BaseModel
from datetime import date
from typing import Optional

class FeedbackView(BaseModel):
    id: int
    content: str
    created_at: date
    star: float
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