from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import VoucherService,EventService
from api.response import Response,HTTP_404_NOT_FOUND
VoucherRouter = APIRouter(
    tags = ["View - Voucher"],
    dependencies=[
        Depends(get_db)
    ]
)

@VoucherRouter.get("/vouchers/{Event_ID}")
def view_addon_services(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata=VoucherService(db).all(
            Manager_ID=event['owner'],
            Event_ID=event['id']
        )
    )

@VoucherRouter.get("/voucher/{Voucher_ID}")
def view_addon_services(Voucher_ID:int,db = Depends(get_db)):
    voucher = VoucherService(db).find(Voucher_ID)
    if voucher is None:
        raise HTTP_404_NOT_FOUND("Addon Service Not Found")
    return Response(
        metadata=voucher
    )

    
