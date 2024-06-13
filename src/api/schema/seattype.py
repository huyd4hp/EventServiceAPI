from pydantic import BaseModel
from typing import Optional

class SeatTypeView(BaseModel):
    id: int
    type : str
    price : float
    event : int
    class Config:
        from_attributes = True

class SeatTypeUpdate(BaseModel):
    type: Optional[str] = None
    price: Optional[float] = None
    class Config:
        from_attributes = True

class SeatTypeCreate(BaseModel):
    type: str
    price: float
    event: int
    class Config:
        from_attributes = True