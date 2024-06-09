from core.database.mysql import Event as EventModel
from core.database.mysql import SeatType as STModel
from core.database.mysql import AddonService as ASModel
from core.database.mysql import FeedBack as FBModel
from core.database.mysql import Show as ShowModel
from core.database.mysql import Voucher as VoucherModel
from api.response import *
from sqlalchemy import asc
from datetime import date
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List
from api.schema import *
from api.service import *


class EventService:
    def __init__(self,db:Session):
        self.db = db
    
    def all(self,Owner_ID:str = None,Name:str="",Location:str="",Start_Date:date=None,End_Date:date=None) -> List[EventView]:
        data = self.db.query(EventModel).filter(
            EventModel.name.icontains(Name),
            EventModel.location.icontains(Location),
        )
        if Start_Date:
            data = data.filter_by(start_date= Start_Date)
        if End_Date:
            data = data.filter_by(end_date =End_Date)
        if Owner_ID:
            data = data.filter_by(owner=Owner_ID)
        metadata = [EventView.model_validate(event) for event in data.all()]
        return jsonable_encoder(metadata)
    
    def detail(self,Event_ID:int) -> EventDetail | None:
        Event = self.db.query(EventModel).filter_by(id = Event_ID).first()
        if Event is None:
            return None
        SeatTypes = self.db.query(STModel).filter_by(event=Event_ID).all()
        ASs = self.db.query(ASModel).filter(ASModel.event==Event_ID).all()
        Vouchers = self.db.query(VoucherModel).filter(VoucherModel.event==Event_ID).all()
        Agenda = self.db.query(ShowModel).filter(ShowModel.event==Event_ID).order_by(asc(ShowModel.date)).all()
        FBs = [fb.star for fb in self.db.query(FBModel).filter_by(event=Event_ID).all()]

        metadata = EventDetail(
            id = Event.id,
            name = Event.name,
            about = Event.about,
            location = Event.location,
            start_date = Event.start_date,
            end_date=Event.end_date,
            owner=Event.owner,

            seat=jsonable_encoder([SeatTypeView.model_validate(ST) for ST in SeatTypes]),
            addon=jsonable_encoder([AddonView.model_validate(AS) for AS in ASs]),
            agenda=jsonable_encoder([ShowView.model_validate(Show) for Show in Agenda]),
            voucher=jsonable_encoder([VoucherView.model_validate(Voucher) for Voucher in Vouchers]),
            rating= 0 if len(FBs) == 0 else sum(FBs)/len(FBs)
        )
        return jsonable_encoder(metadata)      

    def find(self,Event_ID:int) -> EventView | None:
        Event = self.db.query(EventModel).filter_by(id=Event_ID).first()
        if Event is None:
            return None
        return jsonable_encoder(EventView.model_validate(Event))
    
    def put(self,Event_ID:int,EventInfo:EventPut) -> EventView | None:
        event = self.db.query(EventModel).filter_by(id=Event_ID).first()
        if event is None:
            return None 
        event.name = EventInfo.name
        event.about = EventInfo.about
        event.location = EventInfo.location
        # Commit
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(event))    
        
    def patch(self,Event_ID:int,EventPatch:EventPatch) -> EventView | None:
        event = self.db.query(EventModel).filter_by(id=Event_ID).first()
        if event is None:
            return None
        if EventPatch.name is not None:
            event.name = EventPatch.name
        if EventPatch.about is not None:
            event.about = EventPatch.about
        if EventPatch.location is not None:
            event.location = EventPatch.location
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(event))
        
    
    def delete(self,id:int) -> EventView | None:
        Event = self.db.query(EventModel).filter_by(id=id).first()
        if Event is None:
            return None
        self.db.delete(Event)
        self.db.commit()
        return Event.id
            
    
    def add(self,EventInfo:EventCreate,Owner_ID:str) -> EventView | None:
        obj =  EventModel(**EventInfo.model_dump())
        obj.owner = Owner_ID
        self.db.add(obj)
        # Commit            
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(obj))    

    
    
