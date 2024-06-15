from sqlalchemy.orm import Session
from core.database.mysql import Seat,SeatType,Event
from fastapi.encoders import jsonable_encoder
from api.schema import SeatTypeCreate,SeatTypeUpdate,SeatTypeView
from typing import List

class SeatTypeService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,Manager_ID:str=None,Event_ID:int=None) -> List[SeatTypeView]: 
        ''' Danh sách SeatType thuộc quản lí của User '''
        query = self.db.query(SeatType).join(Event,SeatType.event == Event.id)
        if Event_ID:
            query = query.filter(SeatType.event == Event_ID)
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        metadata = [SeatTypeView.model_validate(obj) for obj in query.all()]
        return jsonable_encoder(metadata)
    
    
    def find(self,ID:int) -> SeatTypeView | None:
        data = self.db.query(SeatType).filter_by(id = ID).first()
        if data is None:
            return None
        return jsonable_encoder(SeatTypeView.model_validate(data)) 

    def add(self,SeatTypeInfo:SeatTypeCreate) -> SeatTypeView:
        '''Thêm SeatType'''
        NewST = SeatType(**SeatTypeInfo.model_dump())
        self.db.add(NewST)
        self.db.commit()
        return jsonable_encoder(SeatTypeView.model_validate(NewST))
    
    
    def delete(self,SeatType_ID:int):
        '''Xoá SeatType bằng ID'''
        obj =self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        self.db.delete(obj)
        self.db.commit()
        
    def update(self,SeatType_ID:int,SeatTypeInfo:SeatTypeUpdate) -> SeatTypeView:
        STObj = self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        if SeatTypeInfo.type is not None:
            STObj.type = SeatTypeInfo.type
        if SeatTypeInfo.price is not None or SeatTypeInfo.price == 0:
            STObj.price = SeatTypeInfo.price
        self.db.commit()
        return jsonable_encoder(SeatTypeView.model_validate(STObj))
        



        

    
    