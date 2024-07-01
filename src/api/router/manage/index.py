from fastapi import APIRouter,Depends
from .endpoints.event import EventRouter
from .endpoints.seat import SeatRouter
from .endpoints.voucher import VoucherRouter
from .endpoints.feedback import FeedBackRouter
from .endpoints.show import ShowRouter
from api.auth.dependencies import login_required

ManageRouter = APIRouter(
    dependencies=[
        Depends(login_required),
    ],
)
ManageRouter.include_router(EventRouter)
ManageRouter.include_router(SeatRouter)
ManageRouter.include_router(VoucherRouter)
ManageRouter.include_router(FeedBackRouter)
ManageRouter.include_router(ShowRouter)