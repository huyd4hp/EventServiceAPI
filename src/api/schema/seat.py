from pydantic import BaseModel
from typing import Optional,Literal
class SeatDelete(BaseModel):
    ids: list
    class Config:
        from_attributes = True
        
class SeatCreate(BaseModel):
    event:int
    count: Optional[int] = 1
    class Config:
        from_attributes = True

class SeatView(BaseModel):
    id: int
    event:int 
    price: float
    status: str
    owner: Optional[str] = None
    class Config:
        from_attributes = True


class SeatUpdate(BaseModel):
    status: Optional[Literal["NotOrdered", "Ordered", "Pending","Cancelled"]] = None
    owner: Optional[str] = None

    class Config:
        from_attributes = True

