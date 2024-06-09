from sqlalchemy.orm import Session
from core.database.mysql import *
from api.schema import *
from typing import List
from fastapi.encoders import jsonable_encoder

class SeatService:
    def __init__(self,db:Session):
        self.db = db
    def all(self,SeatType_ID:int) -> List[SeatView]:
        '''Tất cả Seat của SeatType'''
        data = self.db.query(Seat).filter(Seat.type == SeatType_ID).all()
        metadata = [SeatView.model_validate(seat) for seat in data]
        return jsonable_encoder(metadata)
    def find(self,Seat_ID:int) -> SeatView | None:
        data = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        if data is None:
            return None
        metadata = SeatView.model_validate(data)
        return jsonable_encoder(metadata)
    def type(self,Seat_ID:int) -> SeatTypeView:
        '''SeatType của Seat'''
        data = self.db.query(SeatType).join(Seat,Seat.type==SeatType.id).filter(Seat.id == Seat_ID).first()
        if data is None:
            return None
        metadata = SeatTypeView.model_validate(data)
        return jsonable_encoder(metadata)
    def add(self,SeatInfo:SeatCreate,SeatType_ID:int) -> List[SeatView]:
        holder = self.db.query(Seat).filter(Seat.code == SeatInfo.code, Seat.type == SeatType_ID).first()
        if holder:
            return None
        start = len(self.db.query(Seat).filter(Seat.type == SeatType_ID).all()) + 1
        code = SeatInfo.code
        for i in range(start,start+SeatInfo.count):
            object = Seat(
                code = code + str(i),
                type = SeatType_ID
            )
            self.db.add(object)
        self.db.commit()
        news = self.db.query(Seat).filter(Seat.type == SeatType_ID).offset(start-1).all()
        metadata = [SeatView.model_validate(obj) for obj in news]
        return jsonable_encoder(metadata)
    
    def delete(self,Seat_ID:int):
        '''Xoá Seat theo ID'''
        object = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        if object is None:
            return False
        self.db.delete(object)
        self.db.commit()
        return Seat_ID
    

        