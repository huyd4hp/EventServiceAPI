from sqlalchemy.orm import Session
from core.database.mysql import *
from api.schema import *
from typing import List
from fastapi.encoders import jsonable_encoder

class SeatService:
    def __init__(self,db:Session):
        self.db = db
        
    def all(self,Manager_ID:str=None,Type:int=None,Code:str="",Status:str=None,Event_ID:int=None) -> List[SeatView]:
        '''Tất cả Seat'''
        query = self.db.query(Seat).join(SeatType,Seat.type == SeatType.id).join(Event,Event.id == SeatType.event)
        if Event_ID:
            query = query.filter(Event.id == Event_ID)
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        if Type:
            query = query.filter(Seat.type==Type)
        query = query.filter(
            Seat.code.icontains(Code)
        )
        if Status:
            query = query.filter(
                Seat.status == Status
            )
        metadata = [SeatView.model_validate(obj) for obj in query.all()]
        return jsonable_encoder(metadata)    

    def find(self,Seat_ID:int) -> SeatView | None:
        data = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        if data is None:
            return None
        metadata = SeatView.model_validate(data)
        return jsonable_encoder(metadata)    
    
    def add(self,SeatInfo:SeatCreate) -> List[Seat]:
        exists = self.db.query(Seat).filter(
            Seat.code.ilike(f"{SeatInfo.code}%"),
            Seat.type == SeatInfo.type
        ).all()
        metadata = []
        start = len(exists) + 1
        end = len(exists) + 1 + SeatInfo.count
        for i in range(start,end):
            NewSeat = Seat(
                code = f"{SeatInfo.code}{i}",
                type = SeatInfo.type
            )
            self.db.add(NewSeat)
            metadata.append(jsonable_encoder(NewSeat))
        self.db.commit()
        return metadata
    
    def update(self,Seat_ID:int,SeatInfo:SeatUpdate) -> SeatView:
        instance = self.db.query(Seat).filter(Seat.id == Seat_ID).first()
        instance.status = SeatInfo.status
        if instance.status == "NOT_ORDERED":
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
    

        