from sqlalchemy.orm import Session
from core.database.mysql import AddonService as AddonTable
from core.database.mysql import Event
from fastapi.encoders import jsonable_encoder
from api.schema import *
from typing import List
class AddonService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,Owner_ID:int = None,Event_ID:int = None) -> List[AddonView]:
        query = self.db.query(AddonTable).join(Event,AddonTable.event == Event.id)
        if Owner_ID:
            query = query.filter(Event.owner==Owner_ID)
        if Event_ID:
            query = query.filter(AddonTable.event==Event_ID)
        metadata = [AddonView.model_validate(V) for V in query.all()]
        return jsonable_encoder(metadata)
    
    def find(self,Name:str,Event_ID:int) -> AddonView | None:
        obj = self.db.query(AddonTable).filter(AddonTable.name == Name, AddonTable.event == Event_ID).first()
        if obj is None:
            return None
        return jsonable_encoder(AddonView.model_validate(obj))
    
    def findByID(self,Service_ID:int) -> AddonView | None:
        obj = self.db.query(AddonTable).filter(AddonTable.id == Service_ID).first()
        if obj is None:
            return None
        return jsonable_encoder(AddonView.model_validate(obj))
    
    def add(self,AddonInfo:AddonCreate):
        obj = AddonTable(**AddonInfo.model_dump())
        self.db.add(obj)
        try:
            self.db.commit()
            obj = self.db.query(AddonTable).filter(AddonTable.name == AddonInfo.name, AddonTable.event == AddonInfo.event).first()
            return jsonable_encoder(AddonView.model_validate(obj))
        except:
            return None
    
    def update(self,Service_ID:int,AddonInfo:AddonUpdate) -> AddonView | None:
        obj = self.db.query(AddonTable).filter(AddonTable.id == Service_ID).first()
        if obj is None:
            return None
        if AddonInfo.name is not None:
            obj.name = AddonInfo.name
        if AddonInfo.available is not None:
            obj.available = AddonInfo.available
        if AddonInfo.description is not None:
            obj.description = AddonInfo.description
        if AddonInfo.price is not None:
            obj.price = AddonInfo.price
        try:
            self.db.commit()
            data = self.db.query(AddonTable).filter(AddonTable.id == Service_ID).first()
            metadata = jsonable_encoder(AddonView.model_validate(data))
            return metadata
        except:
            return None
    def delete(self,Service_ID):
        obj = self.db.query(AddonTable).filter_by(id=Service_ID).first()
        self.db.delete(obj)
        try:
            self.db.commit()
            return Service_ID
        except:
            return None