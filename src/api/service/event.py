from core.database.mysql import Event,Show
from datetime import date
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List
from api.schema import EventView,EventUpdate,EventCreate


class EventService:
    def __init__(self,db:Session):
        self.db = db

    def __update__(self,Event_ID:int):
        event = self.db.query(Event).filter(Event.id == Event_ID).first()
        if event is None:
            return 
        shows = self.db.query(Show).filter(Show.event == Event_ID).all()
        if shows is None:
            return 
        event.start_date = min(show.date for show in shows)
        event.end_date = max(show.date for show in shows)
        self.db.commit()
    
    def all(self,
            Manager_ID:str = None,
            Name:str="",
            Location:str="",
            Start_Date:date=None,
        ) -> List[EventView]:
        query = self.db.query(Event).filter(
            Event.name.icontains(Name),
            Event.location.icontains(Location),
        )
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        if Start_Date:
            query = query.filter(Event.start_date == Start_Date)
        data = query.all()
        metadata = [EventView.model_validate(V) for V in data]
        return jsonable_encoder(metadata)
         
    def find(self,Event_ID:int) -> EventView | None:
        instance = self.db.query(Event).filter_by(id=Event_ID).first()
        if instance is None:
            return None
        return jsonable_encoder(EventView.model_validate(instance))

    def update(self,Event_ID:int,Information:EventUpdate) -> EventView | None:
        event = self.db.query(Event).filter(Event.id == Event_ID).first()
        if Information.name:
            event.name = Information.name
        if Information.about:
            event.about = Information.about
        if Information.location:
            event.location = Information.location
        # Commit
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(event))    
        
        
    def delete(self,id:int) -> EventView | None:
        instance = self.db.query(Event).filter_by(id=id).first()
        self.db.delete(instance)
        self.db.commit()
        return instance.id
            
    
    def add(self,EventInfo:EventCreate,user:dict) -> EventView | None:
        obj =  Event(**EventInfo.model_dump())
        obj.owner = user.get("_id")
        first_name = user.get("first_name") if user.get("first_name") != None else ""
        last_name = user.get("last_name") if user.get("last_name") != None else ""
        owner_name = first_name + " " + last_name
        if owner_name == " ":
            owner_name = None
        obj.owner_name = owner_name
        self.db.add(obj)
        # Commit            
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(obj))    

    
    
