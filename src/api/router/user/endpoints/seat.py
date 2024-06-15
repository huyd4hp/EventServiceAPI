from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import SeatService,SeatTypeService,EventService
from api.response import Response,HTTP_404_NOT_FOUND
SeatRouter = APIRouter(
    tags = ["View - Seat"],
    dependencies=[
        Depends(get_db)
    ]
)

@SeatRouter.get("/seats/{Event_ID}")
def view_seat(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    seattypes = SeatTypeService(db).all(
        Owner_ID=event['owner'],
        Event_ID=event['id']
    )
    LstSeats = []
    for st in seattypes:
        LstSeats.append(SeatService(db).all(Owner_ID=event['owner'],Type=st.get("id")))
    return Response(
        metadata = LstSeats
    )

@SeatRouter.get("/seat/{Seat_ID}")
def view_seat(Seat_ID:int, db = Depends(get_db)):
    seat = SeatService(db).find(Seat_ID)
    if seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    seattype = SeatTypeService(db).find(seat.get("type"))
    seat['type'] = seattype
    return Response(
        metadata = seat    
    )
    
