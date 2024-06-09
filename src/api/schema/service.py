from pydantic import BaseModel

class ServiceView(BaseModel):
    name:str
    description:str
    available:int
    price:float
    event:int
    class Config:
        from_attributes = True