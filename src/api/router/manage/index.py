from fastapi import APIRouter,Depends
from .endpoints.event import EventRouter
from .endpoints.seattype import SeatTypeRouter
from .endpoints.seat import SeatRouter
from .endpoints.voucher import VoucherRouter
from .endpoints.addon_service import AddonServiceRouter
from api.auth.dependencies import login_required
ManageRouter = APIRouter(
    dependencies=[
        Depends(login_required),
    ],
)
ManageRouter.include_router(EventRouter)
ManageRouter.include_router(SeatTypeRouter)
ManageRouter.include_router(SeatRouter)
ManageRouter.include_router(VoucherRouter)
ManageRouter.include_router(AddonServiceRouter)