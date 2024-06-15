from sqlalchemy.orm import Session
from core.database.mysql import Event,Voucher
from fastapi.encoders import jsonable_encoder
from api.schema import VoucherView,VoucherCreate,VoucherUpdate
from typing import List
class VoucherService:
    def __init__(self,db:Session):
        self.db = db

    def all(self,Manager_ID:int = None,Event_ID:int=None)-> List[VoucherView]:
        query = self.db.query(Voucher).join(Event,Voucher.event == Event.id)
        if Manager_ID:
            query = query.filter(Event.owner==Manager_ID)
        if Event_ID:
            query = query.filter(Event.id==Event_ID)
        metadata = [VoucherView.model_validate(V) for V in query.all()]
        return jsonable_encoder(metadata)
    
    def find(self,Voucher_ID:int) -> VoucherView | None:
        instance = self.db.query(Voucher).filter(Voucher.id == Voucher_ID).first()
        if instance is None:
            return None
        data = VoucherView.model_validate(instance)
        metadata = jsonable_encoder(data)
        return metadata

    
    def add(self,VoucherInfo:VoucherCreate) -> VoucherView:
        obj = Voucher(**VoucherInfo.model_dump(exclude={"quantity"}))
        obj.remaining = VoucherInfo.quantity
        self.db.add(obj)
        self.db.commit()
        return jsonable_encoder(VoucherView.model_validate(obj))
        
    def delete(self,Voucher_ID:int) -> int:
        obj = self.db.query(Voucher).filter_by(id=Voucher_ID).first()
        self.db.delete(obj)
        self.db.commit()
        return Voucher_ID

    def update(self,Voucher_ID:int, VoucherInfo:VoucherUpdate) -> VoucherView:
        obj = self.db.query(Voucher).filter_by(id=Voucher_ID).first()
        if VoucherInfo.name is not None:
            obj.name = VoucherInfo.name
        if VoucherInfo.discount_max is not None:
            obj.discount_max = VoucherInfo.discount_max
        if VoucherInfo.discount_percent is not None:
            obj.discount_percent = VoucherInfo.discount_percent
        if VoucherInfo.remaining is not None:
            obj.remaining = VoucherInfo.remaining
        self.db.commit()
        data = self.db.query(Voucher).filter_by(id=Voucher_ID).first()
        metadata = VoucherView.model_validate(data)
        return jsonable_encoder(metadata)