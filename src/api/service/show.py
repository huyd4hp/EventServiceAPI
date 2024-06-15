from sqlalchemy.orm import Session
from core.database.mysql import Show,Event
from fastapi.encoders import jsonable_encoder
from api.schema import ShowView,ShowCreate,ShowUpdate
from datetime import date
from typing import List
# Service
class ShowService:
    def __init__(self,db:Session):
        self.db = db
    def all(self,Manager_ID:str=None,Event_ID:int=None,Date:date=None) -> List[ShowView]:
        query = self.db.query(Show).join(Event)
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        if Event_ID:
            query = query.filter(Event.id == Event_ID)
        if Date:
            query = query.filter(Show.date == Date)
        data = [ShowView.model_validate(show) for show in query.all()]
        metadata = jsonable_encoder(data)
        return metadata
    def find(self,Show_ID:int) -> ShowView | None:
        instance = self.db.query(Show).filter(Show.id == Show_ID).first()
        if instance is None:
            return None
        return jsonable_encoder(ShowView.model_validate(instance))
    def delete(self,Show_ID:int):
        object = self.db.query(Show).filter_by(id=Show_ID).first()
        self.db.delete(object)
        self.db.commit()
        return Show_ID
    def update(self,Show_ID:int,ShowInfo:ShowUpdate) -> ShowView:
        instance = self.db.query(Show).filter(Show.id == Show_ID).first()
        if ShowInfo.name:
            instance.name = ShowInfo.name
        if ShowInfo.date:
            instance.date = ShowInfo.date
        if ShowInfo.start:
            instance.start = ShowInfo.start
        if ShowInfo.end:
            instance.end = ShowInfo.end
        self.db.commit()
        instance = self.db.query(Show).filter(Show.id == Show_ID).first()
        data = ShowView.model_validate(instance)
        metadata = jsonable_encoder(data)
        return metadata
    
    def add(self,ShowInfo:ShowCreate):
        show = Show(**ShowInfo.model_dump())
        self.db.add(show)
        self.db.commit()
        show = self.db.query(Show).filter(Show.event == ShowInfo.event, Show.name == Show.name).first()
        return jsonable_encoder(ShowView.model_validate(show))
        

        







