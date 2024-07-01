from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.service import SeatService,EventService
from api.response import Response,HTTP_404_NOT_FOUND
from api.schema import SeatView
SeatRouter = APIRouter(
    tags = ["View - Seat"],
    dependencies=[
        Depends(get_db)
    ]
)

@SeatRouter.get("/seats/{Event_ID}",response_model=SeatView)
def view_seat(Event_ID:int,db = Depends(get_db),status:str=Query(None)):
    metadata = SeatService(db).all(Event_ID=Event_ID,Status=status)
    return Response(
        metadata = metadata,
    )

@SeatRouter.get("/seat/{Seat_ID}")
def view_seat(Seat_ID:int, db = Depends(get_db)):
    seat = SeatService(db).find(Seat_ID)
    if seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    else:
        seattype = SeatTypeService(db).find(seat.get("type"))
        event = EventService(db).find(seattype['event'])
        seat['type'] = seattype['type']
        seat['price'] = seattype['price']
        seat['event'] = seattype['event']
        seat['event_owner'] = event['owner']
        return Response(
            metadata = seat    
        )
    
