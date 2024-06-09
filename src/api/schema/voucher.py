from pydantic import BaseModel
from typing import Optional
class VoucherView(BaseModel):
    id: int
    name: str
    discount_percent: float
    discount_max: float
    remaining: int
    event: int
    class Config:
        from_attributes = True

class VoucherCreate(BaseModel):
    name: str
    discount_percent: float
    discount_max: float
    quantity: int
    event: int
    class Config:
        from_attributes = True

class VoucherUpdate(BaseModel):
    name: Optional[str] = None
    discount_percent: Optional[float] = None
    discount_max: Optional[float] = None
    remaining: Optional[int] = None
    class Config:
        from_attributes = True

