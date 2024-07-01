from sqlalchemy import Column,BigInteger,SmallInteger,Float,Date,Time,Enum,ForeignKey,UniqueConstraint,CheckConstraint,String,Text,DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func
import enum

class Base(DeclarativeBase):
    pass

class SeatStatus(enum.Enum):
    NotOrdered = "NotOrdered"
    Ordered = "Ordered"
    Pending = "Pending"
    Cancelled = "Cancelled"

class Event(Base):
    __tablename__ = "Event"
    
    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    image = Column(Text)
    name = Column(String(255),nullable=False) 
    about = Column(Text)
    location = Column(Text,nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    owner = Column(String(255),nullable=False) 
    owner_name = Column(String(255),default=None)

    

class Seat(Base):
    # Tablename
    __tablename__ = "Seat"
    # Column
    id = Column(BigInteger,primary_key=True,autoincrement=True)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"),nullable=False)
    price = Column(Float,default=0.0)
    status = Column(Enum(SeatStatus),nullable=False,default=SeatStatus.NotOrdered)
    owner = Column(String(255))    

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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
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
    discount_percent = Column(Float,nullable=False)
    discount_max = Column(Float,nullable=False)
    event = Column(BigInteger,ForeignKey("Event.id",ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("name", "event", name="NameVoucher"),
        CheckConstraint('discount_percent >= 0', name='non_negative_discount_percent'),
        CheckConstraint('discount_max >= 0', name='non_negative_discount_max'),
    )   