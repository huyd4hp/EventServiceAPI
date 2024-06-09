from fastapi import FastAPI
import uvicorn
from core import settings
from core.database.mysql import Base,Engine
from api.router import AppRouter
from api.auth.middleware import ExceptionHandlerMiddleware
from core.kafka import KafkaClient
import asyncio
# Lifespan
async def lifespan(app:FastAPI):
    kafka = KafkaClient(
        KAFKA_BOOTSTRAP_SERVERS=settings.KAFKA_BOOTSTRAP_SERVERS,
        TOPIC="booking",
    )
    await kafka.connect()
    asyncio.create_task(kafka.run())
    yield
    await kafka.close() 
# App
app = FastAPI(
    title=settings.APP_TITLE,
    debug=settings.APP_DEBUG,
    version=settings.APP_VERSION,
    docs_url="/docs",
    root_path="/api/v1",
    lifespan=lifespan,
)
# Database
Base.metadata.create_all(Engine)
# Router
app.include_router(AppRouter)
# Handle Error
app.add_middleware(ExceptionHandlerMiddleware)
# Run App
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
    )