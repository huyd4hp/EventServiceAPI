from pydantic import BaseModel
from typing import Optional,Literal
class SeatDelete(BaseModel):
    ids: list
    class Config:
        from_attributes = True
        
class SeatCreate(BaseModel):
    code: str
    type: int
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


class SeatUpdate(BaseModel):
    status: Optional[Literal["NOT_ORDERED", "ORDERED", "PENDING","CANCELLED"]] = None
    owner: Optional[str] = None

    class Config:
        from_attributes = True

