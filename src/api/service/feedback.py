from sqlalchemy.orm import Session
from core.database.mysql import FeedBack,Event
from api.schema import FeedbackView,FeedbackUpdate,FeedbackCreate
from fastapi.encoders import jsonable_encoder
from typing import List
class FeedbackService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,Manager_ID:str,Event_ID:int) -> List[FeedbackView]:
        query = self.db.query(FeedBack).join(Event,FeedBack.event == Event.id)
        if Manager_ID:
            query = query.filter(Event.owner == Manager_ID)
        if Event_ID:
            query = query.filter(Event.id == Event_ID)
        data = [FeedbackView.model_validate(fb) for fb in query.all()]
        metadata = jsonable_encoder(data)
        return metadata
    
    def find(self,Feedback_ID:int) -> FeedbackView | None:
        instance = self.db.query(FeedBack).filter(FeedBack.id == Feedback_ID).first()
        if instance is None:
            return None
        data = FeedbackView.model_validate(instance)
        return jsonable_encoder(data)
    
    def update(self,ID:int,Information:FeedbackUpdate) -> FeedbackView:
        instance = self.db.query(FeedBack).filter(FeedBack.id == ID).first()
        if Information.content is not None:
            instance.content = Information.content
        if Information.star is not None:
            instance.star = Information.star
        self.db.commit()
        instance = self.db.query(FeedBack).filter(FeedBack.id == ID).first()
        return jsonable_encoder(FeedbackView.model_validate(instance))

    def add(self,Feedback:FeedbackCreate):
        fb = FeedBack(**FeedBack)
        self.db.add(fb)
        self.db.commit()
        
    def delete(self,Feedback_ID:int) -> int:
        instance = self.db.query(FeedBack).filter(FeedBack.id == Feedback_ID).first()
        self.db.delete(instance)
        self.db.commit()
        return Feedback_ID
        

    