from pydantic import BaseModel
from typing import Optional,List
class SeatTypeView(BaseModel):
    id: int
    type : str
    price : float
    event : int
    class Config:
        from_attributes = True

class SeatTypeUpdate(BaseModel):
    type: str
    price: float

class SeatDelete(BaseModel):
    ids: list
    class Config:
        from_attributes = True
        
class SeatCreate(BaseModel):
    code: str
    count: Optional[int] = 1
    class Config:
        from_attributes = True

class SeatView(BaseModel):
    id: int
    code: str
    type: int
    status: str
    owner: Optional[str] = None
    class Config:
        from_attributes = True

class SeatTypeDetail(BaseModel):
    id: int
    type : str
    price : float
    event : int
    seats: Optional[List[SeatView]] = []
    class Config:
        from_attributes = True

class SeatTypeCreate(BaseModel):
    type: str
    price: float
    event: int
    class Config:
        from_attributes = True