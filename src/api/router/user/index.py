from fastapi import APIRouter
from .endpoints.event import EventRouter
from .endpoints.seat import SeatRouter
from .endpoints.addon_service import AddonRouter
from .endpoints.voucher import VoucherRouter
UserRouter = APIRouter()

UserRouter.include_router(EventRouter)
UserRouter.include_router(SeatRouter)
UserRouter.include_router(AddonRouter)
UserRouter.include_router(VoucherRouter)