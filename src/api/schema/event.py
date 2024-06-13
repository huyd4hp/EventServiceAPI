from datetime import date
from pydantic import BaseModel
from typing import Optional,List

class EventView(BaseModel):
    id: int
    name: str
    about: Optional[str]
    location: str
    start_date: Optional[date] 
    end_date: Optional[date] 
    owner: str
    owner_name: Optional[str] = None
    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    name: Optional[str] = None
    about: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: str
    about: Optional[str] = None
    location: str





