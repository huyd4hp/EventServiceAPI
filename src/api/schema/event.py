from datetime import date
from pydantic import BaseModel,model_validator
from fastapi import Query
from typing import Optional

class EventView(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
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
    price: Optional[float] = 0.0
    seatCount: Optional[int] = 1

class EventQuery(BaseModel):
    page: Optional[int] = Query(1, alias='page')
    limit: Optional[int] = Query(10, alias='limit')
    offset: Optional[int] = Query(0, alias='offset')
