from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import SeatService,SeatTypeService
from api.response import Response
SeatRouter = APIRouter(
    tags = ["View - Seat"],
    dependencies=[
        Depends(get_db)
    ]
)

@SeatRouter.get("/seat/{Seat_ID}")
def view_seat(Seat_ID:int,db = Depends(get_db)):
    seat = SeatService(db).find(Seat_ID)
    seattype = SeatTypeService(db).find(seat.get('type'))
    seat['type'] = seattype
    return Response(
        metadata = seat
    )
