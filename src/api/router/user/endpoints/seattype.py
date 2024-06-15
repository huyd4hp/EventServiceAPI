from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import EventService,SeatTypeService
from api.response import HTTP_404_NOT_FOUND,Response
SeatTypeRouter = APIRouter(
    tags = ["View - SeatType"],
    dependencies=[
        Depends(get_db)
    ]
)

@SeatTypeRouter.get("/seattypes/{Event_ID}")
def list_type(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata = SeatTypeService(db).all(
            Manager_ID=event['owner'],
            Event_ID=event['id']
        )
    )

@SeatTypeRouter.get("/seattype/{ID}")
def view_type(SeatType_ID:int,db= Depends(get_db)):
    instance = SeatTypeService(db).find(SeatType_ID)
    if instance:
        raise HTTP_404_NOT_FOUND("Not Found")
    return Response(
        metadata = instance
    )