from fastapi import APIRouter,Depends
from .event import EventRouter
from .seat import SeatRouter
from .voucher import VoucherRouter
from .addon_service import AddonServiceRouter
from .show import ShowRouter
from .feedback import FeedBackRouter
from ..auth.dependencies import login_required

AppRouter = APIRouter(
    dependencies=[
        Depends(login_required),
    ]
)
AppRouter.include_router(EventRouter)
AppRouter.include_router(SeatRouter)
AppRouter.include_router(VoucherRouter)
AppRouter.include_router(AddonServiceRouter)
AppRouter.include_router(ShowRouter)
AppRouter.include_router(FeedBackRouter)