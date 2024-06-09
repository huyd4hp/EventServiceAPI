from pydantic import BaseModel
from datetime import date as Date
from datetime import time
from typing import Optional


class ShowView(BaseModel):
    id: int
    name: str
    date: Date
    start: time
    end: time
    event: int
    class Config:
        from_attributes = True

class ShowCreate(BaseModel):
    name: str
    date: Date
    start: time
    end: time
    event: int

class ShowUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[Date] = None
    start: Optional[time] = None
    end: Optional[time] = None
    