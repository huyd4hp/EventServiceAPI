from aiokafka import AIOKafkaConsumer
from typing import Any,List
from core.database.mysql import async_get_db,Event,Seat,Voucher,AddonService
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
            seat = db.query(Seat).filter(Seat.id == booking_detail['seat_id']).first()
            seat.status = "Pending"
            for id in booking_detail['addons_id']:
                addon = db.query(AddonService).filter(AddonService.id == id).first()
                addon.available -= 1
            if 'voucher_id' in booking_detail:
                voucher = db.query(Voucher).filter(Voucher.id == booking_detail['voucher_id']).first()
                voucher.remaining -= 1
            db.commit()
            
    async def __payment__(self,msg):
        status = msg.key.decode()
        if status == "Paid":
            seat_id = msg.value.decode()
            async with async_get_db() as db:
                seat = db.query(Seat).filter(Seat.id == seat_id).first()
                seat.status = "ORDERED"
                db.commit()
        if status == "Failed":
            booking_detail = json.loads(msg.value.decode())
            async with async_get_db() as db:
                seat = db.query(Seat).filter(Seat.id == booking_detail['seat_id']).first()
                if "voucher_id" in booking_detail:
                    voucher = db.query(Voucher).filter(Voucher.id == booking_detail['voucher_id']).first()
                    voucher.remaining += 1
                for id in booking_detail['addons_id']:
                    addon = db.query(AddonService).filter(AddonService.id == id).first()
                    addon.available += 1
                seat.status = "NOT_ORDERED"
                db.commit()
        
    async def run(self):
        async for msg in self.consumer:
            if msg.topic == "update_profile":
                await self.__update_profile__(msg)
            if msg.topic == "booking":
                await self.__booking__(msg)
            if msg.topic == "payment_return":
                print(msg)
                await self.__payment__(msg)


