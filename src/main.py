#! venv/bin/python3.12
from fastapi import FastAPI
import uvicorn
from core import KAFKA_BOOTSTRAP_SERVERS,APP_DEBUG,APP_PORT,APP_TITLE,APP_VERSION
from core.database.mysql import Base,Engine
from api.router import ManageRouter,UserRouter
from api.auth.middleware import ExceptionHandlerMiddleware
from core.kafka import KafkaConsumer
import asyncio
# Lifespan
async def lifespan(app:FastAPI):
    Consumer = KafkaConsumer(
        KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS,
        TOPIC=["update_profile","booking","payment_return"]
    )
    await Consumer.connect()
    asyncio.create_task(Consumer.run())
    yield
    await Consumer.close() 
# App
app = FastAPI(
    title=APP_TITLE,
    debug=APP_DEBUG,
    version=APP_VERSION,
    root_path="/api/v1",
    docs_url="/",
    lifespan=lifespan,
)
# Database
Base.metadata.create_all(Engine)
# Router
app.include_router(
    router = ManageRouter,
    prefix = "/manage",
)
app.include_router(
    router = UserRouter,
    prefix = "",
)
# Handle Error
app.add_middleware(ExceptionHandlerMiddleware)
# Run App
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=APP_PORT,
        reload=APP_DEBUG,
    )
