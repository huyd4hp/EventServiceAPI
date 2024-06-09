from sqlalchemy import Column,BigInteger,SmallInteger,Float,Date,Time,Enum,ForeignKey,UniqueConstraint,CheckConstraint,String,Text
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import datetime as DT

import enum

class Base(DeclarativeBase):
    pass

class SeatStatus(enum.Enum):
    NOT_ORDERED = "NotOrdered"
    ORDERED = "Ordered"
    PENDING = "Pending"
    CANCELLED = "Cancelled"

# Ghế 1 chưa được đặt 
# User đặt ghế 1 -> Lưu vào redis
# User 2 đặt ghế 1 -> có trong redis -> return Seat is booking

class Event(Base):
    __tablename__ = "Event"
    
    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255),nullable=False) 
    about = Column(Text)
    location = Column(Text,nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    owner = Column(String(255),nullable=False) 

    __table_args__ = (
        CheckConstraint('end_date >= start_date', name='event_date_check'),
    )


class AddonService(Base):
    __tablename__ = "AddonService"

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255),nullable=False) 
    description = Column(Text)
    available = Column(SmallInteger,default=-1)
    price = Column(Float,default=0)
    event = Column(BigInteger, ForeignKey("Event.id",ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("name", "event", name="ServiceEvent"),
        CheckConstraint('price >= 0')
    )

class SeatType(Base):
    __tablename__ = "SeatType"
    # Column
    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    type = Column(String(10),nullable=False)
    price = Column(Float,default = 0)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"))
    # Condition
    __table_args__ = (
        UniqueConstraint("type", "event", name="TypeEvent"),
        CheckConstraint('price >= 0')
    )
    
class Seat(Base):
    # Tablename
    __tablename__ = "Seat"
    # Column
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    code = Column(String(10),nullable=False)
    type = Column(BigInteger,ForeignKey("SeatType.id",ondelete="CASCADE"))
    status = Column(Enum(SeatStatus),nullable=False,default=SeatStatus.NOT_ORDERED)
    owner = Column(String(255))    
    # Condition
    __table_args__ = (
        UniqueConstraint("code", "type", name="CodeType"),
    )

class Show(Base):
    __tablename__ = "Show"

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    date = Column(Date,nullable=False)
    start = Column(Time,nullable=False)
    end = Column(Time,nullable=False)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("name", "event", name="ShowEvent"),
        CheckConstraint('end >= start', name='show_time_check'),
    )

class FeedBack(Base):
    __tablename__ = "FeedBack"

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    content = Column(Text,nullable=False)
    star = Column(SmallInteger)
    created_at = Column(Date,default=DT.UTC)
    owner = Column(String(255),nullable=False)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"))

    __table_args__ = (
        CheckConstraint('star > 0 AND star <= 5', name='star_value_check'),
    )

class Voucher(Base):
    __tablename__ = "Voucher"

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255),nullable=False)
    remaining = Column(SmallInteger,nullable=False,default=0)
    discount_percent = Column(Float)
    discount_max = Column(Float)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("name", "event", name="NameVoucher"),
        CheckConstraint('discount_percent >= 0', name='non_negative_discount_percent'),
        CheckConstraint('discount_max >= 0', name='non_negative_discount_max'),
    )   