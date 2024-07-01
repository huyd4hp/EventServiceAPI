from fastapi import FastAPI
import uvicorn
from core import KAFKA_BOOTSTRAP_SERVERS,APP_DEBUG,APP_PORT,APP_TITLE,APP_VERSION,MINIO_ACCESS_KEY,MINIO_SECRET_KEY,MINIO_PORT
from core.database.mysql import Base,Engine
from api.router import ManageRouter,UserRouter
from api.auth.middleware import ExceptionHandlerMiddleware
from fastapi.middleware.cors import CORSMiddleware
from core.kafka import KafkaConsumer
from core.minio import MinIO
import asyncio
# Lifespan
async def lifespan(app:FastAPI):
    Consumer = KafkaConsumer(
        KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS,
        TOPIC=["update_profile","booking","payment_return"]
    )
    await Consumer.connect()
    MinIO(
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        port=MINIO_PORT,
        buckets=['image']
    )
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
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
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
