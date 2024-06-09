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
    class Config:
        from_attributes = True

class EventDetail(BaseModel):
    id: int
    name: str
    about: Optional[str]
    location: str
    start_date: Optional[date] 
    end_date: Optional[date] 
    seat: Optional[List] = []
    addon: Optional[List] = []
    agenda: Optional[List] = []
    voucher: Optional[List] = []
    rating: Optional[float] = 0
    owner: str
    
    class Config:
        from_attributes = True

class EventPut(BaseModel):
    name: str
    about: str
    location: str

    class Config:
        from_attributes = True

class EventPatch(BaseModel):
    name: Optional[str] = None
    about: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: str
    about: Optional[str] = None
    location: str
    class Config:
        from_attributes = True



