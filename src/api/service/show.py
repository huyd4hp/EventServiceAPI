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
    def all(self,Owner_ID:int = None,Event_ID:int=None) -> List[ShowView]:
        query = self.db.query(Show).join(Event,Show.event==Event.id)
        if Owner_ID:
            query = query.filter(Event.owner == Owner_ID)
        if Event_ID:
            query = query.filter(Event.id == Event_ID)
        metadata = [ShowView.model_validate(Show) for Show in query.all()]
        return jsonable_encoder(metadata)
    

    def find(self,Show_ID:int = None,Name:str=None,Event_ID:int=None) -> ShowView | None:
        query = self.db.query(Show)
        if Show_ID:
            query = query.filter(Show.id == Show_ID)
        if Name:
            query = query.filter(Show.name == Name)
        if Event_ID:
            query = query.filter(Show.event == Event_ID)
        object = query.first()
        if object is None:
            return None
        return jsonable_encoder(ShowView.model_validate(object))
    

    
    def add(self,ShowInfo:ShowCreate) -> ShowView | None:
        try:
            obj = Show(**ShowInfo.model_dump())
            self.db.add(obj)
            self.db.commit()
            # ----Update----#
            EventObj = self.db.query(Event).filter_by(id=ShowInfo.event).first()
            EventObj.start_date=self.db.query(Show).filter(Show.event == ShowInfo.event).order_by(Show.date.asc()).first().date
            EventObj.end_date=self.db.query(Show).filter(Show.event == ShowInfo.event).order_by(Show.date.desc()).first().date
            # ----Commit----#
            self.db.commit()
            NewShow = self.db.query(Show).filter(Show.name == ShowInfo.name, Show.event == ShowInfo.event).first()
            return jsonable_encoder(ShowView.model_validate(NewShow))
        except:
            return None
        
    def update(self,Show_ID:int,ShowInfo:ShowUpdate) -> ShowView:
        try:
            ShowObj = self.db.query(Show).filter_by(id=Show_ID).first()
            if ShowInfo.name is not None:
                ShowObj.name = ShowInfo.name
            if ShowInfo.date is not None:
                ShowObj.date = ShowInfo.date
            if ShowInfo.start is not None:
                ShowObj.start = ShowInfo.start
            if ShowInfo.end is not None:
                ShowObj.end = ShowInfo.end
            self.db.commit()
            data = self.db.query(Show).filter_by(id=Show_ID).first()
            metadata = ShowView.model_validate(data)
            return jsonable_encoder(metadata)
        except:
            return None



    #     except:
    #         return None
    
    def delete(self,Show_ID:int):
        try:
            object = self.db.query(Show).filter_by(id=Show_ID).first()
            self.db.delete(object)
            self.db.commit()
            return Show_ID
        except:
            return None
        







