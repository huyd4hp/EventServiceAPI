from sqlalchemy.orm import Session
from core.database.mysql import FeedBack,Event
from fastapi.encoders import jsonable_encoder
from api.schema import FeedbackView,FeedbackCreate,FeedbackUpdate
from datetime import datetime
from typing import List
class FeedbackService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,User_ID:str,Role:str="Admin",Event_ID:int=None) -> List[FeedbackView]:
        data = None
        if Role == "User":
            data = self.db.query(FeedBack).filter(FeedBack.owner == User_ID)
        if Role == "EventAdmin":
            data = self.db.query(FeedBack).join(Event,Event.id == FeedBack.event).filter(Event.owner == User_ID)
        if Role == "Admin":
            data = self.db.query(FeedBack)
        #----- Filter -----#
        if Event_ID:
            data = data.filter(FeedBack.event == Event_ID)
        metadata = [FeedbackView.model_validate(fb) for fb in data.all()]
        return  jsonable_encoder(metadata)

    def find(self,Feedback_ID:int=None,Content:str=None,Event_ID:int=None) -> FeedbackView:
        query = self.db.query(FeedBack)
        if Feedback_ID:
            query = query.filter(FeedBack.id == Feedback_ID)
        if Content:
            query = query.filter(FeedBack.content == Content)
        if Event_ID:
            query = query.filter(FeedBack.event == Event_ID)
        data = query.first()
        metadata = jsonable_encoder(data)
        return metadata
    
    def delete(self,Feedback_ID:int):
        data = self.db.query(FeedBack).filter(FeedBack.id == Feedback_ID).first()
        self.db.delete(data)
        try:
            self.db.commit()
            return Feedback_ID
        except:
            return None
        
    def add(self,Owner_ID:int,FeedbackInfo:FeedbackCreate) -> FeedbackView:
        try:
            obj = FeedBack(**FeedbackInfo.model_dump())
            obj.created_at = datetime.now()
            obj.owner = Owner_ID
            self.db.add(obj)
            self.db.commit()
            print(obj.id)
            instance = self.db.query(FeedBack).filter(FeedBack.id == obj.id).first()
            return jsonable_encoder(FeedbackView.model_validate(instance))
        except:
            return None
        
    def update(self,Feedback_ID:int,FeedBackInfo:FeedbackUpdate) -> FeedbackView:
        try:
            object = self.db.query(FeedBack).filter(FeedBack.id == Feedback_ID).first()
            object.content = FeedBackInfo.content
            self.db.commit()
            object = self.db.query(FeedBack).filter(FeedBack.id == Feedback_ID).first()
            return jsonable_encoder(FeedbackView.model_validate(object))
        except:
            return None