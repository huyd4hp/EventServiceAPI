from core.database.mysql import Event,Show,Seat
from datetime import date
from sqlalchemy.orm import Session
from core import APP_PORT
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
        if len(shows) == 0:
            event.start_date = None
            event.end_date = None
        else:
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
    
    def upload_image(self,Event_ID:int,imageName:str):
        event = self.db.query(Event).filter_by(id=Event_ID).first()
        event.image = f'{imageName}'
        self.db.commit()
        return True
    
    def add(self,EventInfo:EventCreate,user:dict) -> EventView | None:
        # Create Event
        event =  Event(**EventInfo.model_dump(exclude={"price","seatCount"}))
        event.owner = user.get("_id")
        first_name = user.get("first_name") if user.get("first_name") != None else ""
        last_name = user.get("last_name") if user.get("last_name") != None else ""
        owner_name = first_name + " " + last_name
        if owner_name == " ":
            owner_name = None
        event.owner_name = owner_name
        self.db.add(event)
        self.db.flush()
        # Create Seat
        for i in range(0,EventInfo.seatCount):
            self.db.add(Seat(
                event = event.id,
                price = EventInfo.price
            ))
        # Commit            
        self.db.commit()
        return jsonable_encoder(EventView.model_validate(event))    

    
    
