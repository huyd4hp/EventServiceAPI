from aiokafka import AIOKafkaConsumer
from typing import Any,List
from core.database.mysql import async_get_db,Event,Seat,Voucher
from core.database.redis import RedisBooking
import json

class KafkaConsumer:
    def __init__(self,KAFKA_BOOTSTRAP_SERVERS:str,TOPIC:List[Any]):
        self.consumer = AIOKafkaConsumer(
            *TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        )
    async def connect(self):
        await self.consumer.start()
    async def close(self):
        await self.consumer.stop()      

    async def __update_profile__(self,msg):
        CLIENT_ID = msg.key.decode()
        value = json.loads(msg.value.decode())
        first_name = value['first_name'] if value['first_name'] else event.split(" ")[0] if event is not None else ""
        last_name = value['last_name'] if value['last_name'] else event.split(" ")[1] if event is not None else ""
        if 'first_name' in value or 'last_name' in value:
            async with async_get_db() as db:
                events = db.query(Event).filter(Event.owner == CLIENT_ID).all()
                for event in events:
                    event.owner_name = ' '.join((first_name + ' ' + last_name).split())
                db.commit()

    async def __booking__(self,msg):
        booking_detail = json.loads(msg.value.decode())
        async with async_get_db() as db:
            seat = db.query(Seat).filter(Seat.id == booking_detail['seat']).first()
            seat.status = "Pending"
            RedisBooking.set(seat.id, json.dumps(booking_detail))
            if 'voucher' in booking_detail:
                voucher = db.query(Voucher).filter(Voucher.id == booking_detail['voucher']).first()
                voucher.remaining = voucher.remaining - 1 
            db.commit()
            
            
    async def __payment__(self,msg):
        status = msg.key.decode()
        if status == "Paid":
            seat_id = msg.value.decode()
            async with async_get_db() as db:
                seat = db.query(Seat).filter(Seat.id == seat_id).first()
                seat.status = "Ordered"
                booking = json.loads(RedisBooking.get(seat_id))
                seat.owner = booking['buyer_id']
                db.commit()
                RedisBooking.delete(seat_id)
        if status == "Failed":
            booking_detail = json.loads(msg.value.decode())
            async with async_get_db() as db:
                cacheBooking = json.loads(RedisBooking.get(booking_detail['seat']).decode())
                seat_id = cacheBooking['seat']
                seat = db.query(Seat).filter(Seat.id == seat_id).first()
                seat.status = "NotOrdered"
                seat.owner = None
                if 'voucher' in cacheBooking:
                    voucher_id = cacheBooking['voucher']
                    voucher = db.query(Voucher).filter(Voucher.id == voucher_id).first()
                    voucher.remaining += 1
                db.commit()
                


        
    async def run(self):
        async for msg in self.consumer:
            print(msg)
            if msg.topic == "update_profile":
                await self.__update_profile__(msg)
            if msg.topic == "booking":
                await self.__booking__(msg)
            if msg.topic == "payment_return":
                await self.__payment__(msg)


