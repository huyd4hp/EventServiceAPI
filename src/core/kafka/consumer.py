from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from typing import Any,List
import asyncio

class KafkaConsumer:
    def __init__(self,KAFKA_BOOTSTRAP_SERVERS:str,TOPIC:List[Any]):
        self.consumer = AIOKafkaConsumer(
            *TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,  
            group_id='my_group_id'
        )
    async def connect(self):
        await self.consumer.start()
    async def close(self):
        await self.consumer.stop()      

    async def __handle_booking__(self):
        async for msg in self.consumer:
            if msg.topic == "booking":
                print(msg)

    async def __handle_user__(self):
        async for msg in self.consumer:
            if msg.topic == "user":
                print(msg)

    async def run(self):
        await asyncio.gather(
            self.__handle_user__(),
            self.__handle_booking__(),
        )



