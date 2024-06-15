from fastapi import APIRouter
from .endpoints.event import EventRouter
from .endpoints.seat import SeatRouter
ViewRouter = APIRouter()

ViewRouter.include_router(EventRouter)
ViewRouter.include_router(SeatRouter)