from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from fastapi import APIRouter,Depends,Query
from api.service import SeatService,SeatTypeService,EventService
from api.schema import *
from api.response import *
SeatRouter = APIRouter(
    tags=["Manage - Seat"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@SeatRouter.get("/seats",response_model=SeatView)
def manage_seat(
    user = Depends(ManagementUser), 
    db = Depends(get_db),
    type = Query(None),
    code = Query(""),
    status=Query(None)
):
    metadata = SeatService(db).all(
        Owner_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Type = type, Code=code, Status=status
    )
    return Response(
        message = "List Seat",
        metadata = metadata,
    )
@SeatRouter.get("/seat/{Seat_ID}",response_model=SeatView)
def view_seat(
    Seat_ID: int,
    user = Depends(ManagementUser), 
    db = Depends(get_db),
):
    Seat = SeatService(db).find(Seat_ID)    
    if Seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    SeatType = SeatTypeService(db).find(Seat['type'])
    Event = EventService(db).find(SeatType['event'])
    if user.get("role") != "Admin" and user.get("_id") != Event['owner']:
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    return Response(
        metadata = Seat
    )

@SeatRouter.post("/seat")
def create_seat(
    Information:SeatCreate,
    user = Depends(ManagementUser), 
    db = Depends(get_db),
):  
    SeatType = SeatTypeService(db).find(Information.type)
    Event = EventService(db).find(SeatType['event'])
    if user.get("role") != "Admin" and user.get("_id") != Event['owner']:
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    metadata = SeatService(db).add(Information)
    return Response(
        status=201,
        message=f"Created {len(metadata)} Seats",
        metadata= metadata
    )

@SeatRouter.put("/seat/{Seat_ID}",response_model=SeatView)
def update_seat(Seat_ID:int,Information:SeatUpdate, user = Depends(ManagementUser), db = Depends(get_db)):
    SeatTable = SeatService(db)
    #-------------------------------#
    Seat = SeatTable.find(Seat_ID)
    if Seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    ST = SeatTypeService(db).find(Seat.get("type"))
    Event = EventService(db).find(ST.get("event"))
    if Event.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    NewS = SeatTable.update(Seat_ID,Information)
    return Response(
        message="Updated Seat",
        metadata=NewS,
    )

@SeatRouter.delete("/seat/{Seat_ID}")
def update_seat(Seat_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    SeatTable = SeatService(db)
    #-------------------------------#
    Seat = SeatTable.find(Seat_ID)
    if Seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    ST = SeatTypeService(db).find(Seat.get("type"))
    Event = EventService(db).find(ST.get("event"))
    if Event.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    SeatTable.delete(Seat_ID)
    raise HTTP_204_NO_CONTENT()



    