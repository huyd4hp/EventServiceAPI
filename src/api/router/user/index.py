from fastapi import APIRouter
from .endpoints.event import EventRouter
from .endpoints.seat import SeatRouter
from .endpoints.voucher import VoucherRouter
from .endpoints.feedback import FeedBackRouter
from .endpoints.show import ShowRouter
UserRouter = APIRouter()

UserRouter.include_router(EventRouter)
UserRouter.include_router(ShowRouter)
UserRouter.include_router(SeatRouter)
UserRouter.include_router(VoucherRouter)
UserRouter.include_router(FeedBackRouter)