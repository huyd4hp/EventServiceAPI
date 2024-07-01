from sqlalchemy.orm import Session
from core.database.mysql import *
from api.schema import *
from typing import List
from fastapi.encoders import jsonable_encoder

class SeatService:
    def __init__(self,db:Session):
        self.db = db
        
    def all(self,Manager_ID:str=None,Status:str=None,Event_ID:int=None) -> List[SeatView]:
        query = self.db.query(Seat).join(Event,Event.id == Seat.event)
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        if Event_ID:
            query = query.filter(Event.id == Event_ID)
        if Status:
            query = query.filter(Seat.status == Status)
        metadata = [SeatView.model_validate(seat) for seat in query]
        return jsonable_encoder(metadata)
        

    def find(self,Seat_ID:int) -> SeatView | None:
        data = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        if data is None:
            return None
        metadata = SeatView.model_validate(data)
        return jsonable_encoder(metadata)    

    def add(self,SeatInfo:SeatCreate) -> List[SeatView]:
        RandomSeat = self.db.query(Seat).filter(Seat.event == SeatInfo.event).first()
        metadata = []
        for i in range(0,SeatInfo.count):
            instance = Seat(
                event=SeatInfo.event,
                price= RandomSeat.price,
            )
            self.db.add(instance)
            self.db.flush()
            metadata.append(SeatView.model_validate(instance))
        return jsonable_encoder(metadata)

    
    def update(self,Seat_ID:int,SeatInfo:SeatUpdate) -> SeatView:
        instance = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        if SeatInfo.status:
            instance.status = SeatInfo.status
        if SeatInfo:
            if SeatInfo.status == "NotOrdered":
                instance.owner = None
            else:
                instance.owner = SeatInfo.owner
        self.db.commit()
        instance = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        return jsonable_encoder(SeatView.model_validate(instance))




    def delete(self,Seat_ID:int):
        '''Xoá Seat theo ID'''
        instance = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        self.db.delete(instance)
        self.db.commit()
        return Seat_ID
    

        