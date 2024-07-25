from fastapi import FastAPI
from core import (
    KAFKA_BOOTSTRAP_SERVERS,  
    APP_VERSION,
    APP_HOST,
    APP_PORT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_PORT,
)
from core.database.mysql import Base, Engine
from api.router import ManageRouter, UserRouter
from api.auth.middleware import ExceptionHandlerMiddleware
from api.response import Response
from fastapi.middleware.cors import CORSMiddleware
from core.kafka import KafkaConsumer
from core.minio import MinIO
import asyncio
from core.consul import consulClient
# Lifespan
async def lifespan(app: FastAPI):
    Consumer = KafkaConsumer(
        KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS,
        TOPIC=["update_profile", "booking", "payment_return"],
    )
    await Consumer.connect()
    MinIO(
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        port=MINIO_PORT,
        buckets=["image"],
    )
    consulClient.RegisterService(
        service_id="EventService",
        name="EventService",
        address="nginx.event",
        port=80,
        tags=["EventService","FastAPI"],
    )
    consulClient.AddCheck(
        service_id="EventService",
        name=f"{APP_HOST} Health Check",
        http=f"http://{APP_HOST}:{APP_PORT}/v1/health"
    )
    asyncio.create_task(Consumer.run())
    yield
    await Consumer.close()
# App
app = FastAPI(
    title="Event Service API",
    version=APP_VERSION,
    root_path="/v1",
    docs_url="/docs/event",
    lifespan=lifespan,
)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Database
Base.metadata.create_all(Engine)
# Router
app.include_router(
    router=ManageRouter,    
    prefix="/manage",
)
app.include_router(
    router=UserRouter,
    prefix="",
)

@app.get("/health")
def HealthCheck():
    return Response()
# Handle Error
app.add_middleware(ExceptionHandlerMiddleware)
