from pydantic import BaseModel
from typing import Optional
class AddonView(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float 
    available: int
    event: int
        
    class Config:
        from_attributes = True

class AddonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[int] = None
    class Config:   
        from_attributes = True

class AddonCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = 0
    available: int
    event: int
    

