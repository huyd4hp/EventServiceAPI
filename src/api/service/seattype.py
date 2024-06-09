from sqlalchemy.orm import Session
from core.database.mysql import Seat,SeatType,Event
from fastapi.encoders import jsonable_encoder
from api.schema import SeatTypeCreate,SeatTypeDetail,SeatTypeUpdate,SeatTypeView,SeatView
from typing import List

class SeatTypeService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,Owner_ID:int=None,Event_ID:int=None) -> List[SeatTypeView]: 
        ''' Danh sách SeatType thuộc quản lí của User '''
        query = self.db.query(SeatType).join(Event,SeatType.event == Event.id)
        if Event_ID:
            query = query.filter(SeatType.event == Event_ID)
        if Owner_ID:
            query = query.filter(Event.owner == Owner_ID)
        metadata = [SeatTypeView.model_validate(obj) for obj in query.all()]
        return jsonable_encoder(metadata)
    
    def detail(self,SeatType_ID:int) -> List[SeatTypeDetail]:
        ''' Danh sách Seat của SeatType '''
        STObj = self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        if STObj is None:
            return None
        Seats = [SeatView.model_validate(seat) for seat in self.db.query(Seat).filter(Seat.type == STObj.id).all()]
        metadata = SeatTypeDetail.model_validate(STObj)
        metadata.seats = jsonable_encoder(Seats)
        return jsonable_encoder(metadata)
    
    def findByInfo(self,Type:str,Event_ID:int) -> SeatTypeView | None:
        '''Tìm SeatType'''
        STObj = self.db.query(SeatType).filter(SeatType.type == Type, SeatType.event == Event_ID).first()
        if STObj is None:
            return None
        return jsonable_encoder(SeatTypeView.model_validate(STObj)) 
    
    def findByID(self,SeatType_ID:int) -> SeatTypeView | None:
        '''Tìm SeatType bằng ID'''
        STObj = self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        if STObj is None:
            return None
        return jsonable_encoder(SeatTypeView.model_validate(STObj)) 

    def add(self,SeatTypeInfo:SeatTypeCreate) -> SeatTypeView:
        '''Thêm SeatType'''
        NewST = SeatType(**SeatTypeInfo.model_dump())
        self.db.add(NewST)
        self.db.commit()
        return jsonable_encoder(SeatTypeView.model_validate(NewST))
    
    
    def delete(self,SeatType_ID:int):
        '''Xoá SeatType bằng ID'''
        obj =self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
        
    def update(self,SeatType_ID:int,SeatTypeInfo:SeatTypeUpdate):
        obj = self.db.query(SeatType).filter(SeatType.id == SeatType_ID).first()
        if obj is None:
            return None
        obj.type = SeatTypeInfo.type
        obj.price = SeatTypeInfo.price
        self.db.commit()
        return jsonable_encoder(SeatTypeView.model_validate(obj))
        



        

    
    