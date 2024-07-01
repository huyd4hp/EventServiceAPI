from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from fastapi import APIRouter,Depends,Query
from api.service import SeatService,EventService
from api.schema import *
from api.response import *
SeatRouter = APIRouter(
    tags=["Manage - Seat"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@SeatRouter.get("/seats")
def manage_seat(
    user = Depends(ManagementUser), 
    db = Depends(get_db),
    status=Query(None),
    event=Query(None)
):
    metadata = SeatService(db).all(
        Manager_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Status = status,
        Event_ID=event,
    )
    return Response(
        metadata=metadata
    )
@SeatRouter.get("/seat/{Seat_ID}",response_model=SeatView)
def view_seat(Seat_ID: int,user = Depends(ManagementUser), db = Depends(get_db),):
    Seat = SeatService(db).find(Seat_ID)    
    if Seat is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    Event = EventService(db).find(Seat['event'])
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
    event = EventService(db).find(Information.event)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if event.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    metadata = SeatService(db).add(Information)
    return Response(
        metadata = metadata
    )

@SeatRouter.put("/seat/{Seat_ID}",response_model=SeatView)
def update_seat(Seat_ID:int,Information:SeatUpdate, user = Depends(ManagementUser), db = Depends(get_db)):
    instance = SeatService(db).find(Seat_ID)
    if instance is None:
        raise HTTP_404_NOT_FOUND("Seat Not Found")
    Event = EventService(db).find(instance.get("event"))
    if Event.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    if Information.status == "Ordered" and Information.owner == None:
        raise HTTP_400_BAD_REQUEST("Cannot purchase without an owner.")
    metadata = SeatService(db).update(Seat_ID,Information)
    return Response(
        message="Updated Seat",
        metadata = metadata,
    )

@SeatRouter.delete("/seat")
def delete_seat(Information:SeatDelete, user = Depends(ManagementUser), db = Depends(get_db)):
    deleted = []
    for i in Information.ids:
        Seat = SeatService(db).find(i)
        if Seat is None:
            continue
        Event = EventService(db).find(Seat['event'])
        if Event.get("owner") != user.get("_id") and user.get("role") != "Admin":
            continue
        deleted.append(i)
    for i in deleted:
        SeatService(db).delete(i)
    return Response(
        message = f"Delete {len(deleted)} seats",
        metadata= deleted
    )




    