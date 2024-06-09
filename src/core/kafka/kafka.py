from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from typing import Any
from core.database.mysql import async_get_db
from api.service import SeatService,SeatTypeService,EventService
import json
class KafkaClient:
    def __init__(self,KAFKA_BOOTSTRAP_SERVERS:Any,TOPIC:Any):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )
        self.consumer = AIOKafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,  
            group_id='my_group_id'
        )
    async def connect(self):
        await self.producer.start()
        await self.consumer.start()
    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()      
    async def run(self):
        async for msg in self.consumer:
            async with async_get_db() as db:
                Seat = SeatService(db).find(msg.value.decode())
                if Seat:
                    SeatType = SeatTypeService(db).findByID(Seat.get("type"))
                    Event = EventService(db).find(SeatType.get("event"))

                    seat_detail = Seat
                    seat_detail['type'] = SeatType
                    seat_detail['event'] = Event
                    await self.producer.send_and_wait(
                        topic='seat-detail',
                        key=msg.value,
                        value = json.dumps(seat_detail).encode()
                    )
                else:
                    await self.producer.send_and_wait(
                        topic='seat-detail',
                        key=msg.value,
                        value=None
                    )
                print(f"Seat: {Seat}")



