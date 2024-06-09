from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.auth.dependencies import ManagementUser
from api.service import SeatTypeService,EventService,SeatService
from api.response import *
from api.schema import *

SeatRouter = APIRouter(
    tags=["Seat"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@SeatRouter.get("/seattypes",response_model=SeatTypeView)
def all_seat_type(event = Query(None),user = Depends(ManagementUser), db = Depends(get_db)):
    metadata = SeatTypeService(db).all(
        Owner_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID=event,
    )
    return Response(
        metadata=metadata
    )
@SeatRouter.get("/seattype/{SeatType_ID}",response_model=SeatTypeDetail)
def all_seat_of_seat_type(SeatType_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    metadata = SeatTypeService(db).detail(SeatType_ID)
    if metadata is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    EventObj = EventService(db).find(metadata.get("event"))
    if user.get("role") == "Admin" or user.get("_id") == EventObj.get("owner"):    
        return Response(
            message="All Seat of Seat Type",
            metadata=metadata
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")


@SeatRouter.post("/seattype",response_model=SeatTypeView)
def add_seat_type(SeatTypeInfo:SeatTypeCreate,user=Depends(ManagementUser),db=Depends(get_db)):
    SeatTypeTable = SeatTypeService(db)
    EventTable = EventService(db)
    #---------------------------------------#
    Event = EventTable.find(SeatTypeInfo.event)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if Event.get("owner") == user.get("_id") or user.get("role") == "Admin":
        holderST = SeatTypeTable.findByInfo(SeatTypeInfo.type,SeatTypeInfo.event)
        if holderST:
            raise HTTP_409_CONFLICT("SeatType Existed")
        metadata = SeatTypeTable.add(SeatTypeInfo)
        return Response(
            status=201,
            message="New Seat Type",
            metadata=metadata
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@SeatRouter.post("/seattype/{SeatType_ID}", response_model = SeatView)
def add_seat_of_seat_type(SeatCreate:SeatCreate,SeatType_ID:int,user=Depends(ManagementUser),db=Depends(get_db)):
    STObj = SeatTypeService(db).findByID(SeatType_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(STObj.get("event"))
    if user.get("role") == "Admin" or Event.get("owner") == user.get("_id"):
        metadata = SeatService(db).add(SeatCreate,SeatType_ID)
        return Response(
            status=201,
            message="New Seat",
            metadata=metadata
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@SeatRouter.delete("/seattype/{SeatType_ID}")
def delete_seat_type(SeatType_ID:int,user=Depends(ManagementUser),db=Depends(get_db)):
    STObj = SeatTypeService(db).findByID(SeatType_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(STObj.get("event"))
    if user.get("role") == "Admin" or Event.get("owner") == user.get("_id"):
        SeatTypeService(db).delete(SeatType_ID)
        raise HTTP_204_NO_CONTENT()
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@SeatRouter.delete("/seat/{Seat_ID}") 
def delete_one_seat(Seat_ID:int,user=Depends(ManagementUser),db=Depends(get_db)):
    STObj = SeatService(db).type(Seat_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("Seat_ID Not Found")
    Event = EventService(db).find(STObj.get("event"))
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        if SeatService(db).delete(Seat_ID):
            raise HTTP_204_NO_CONTENT()
        raise HTTP_500_INTERNAL_SERVER_ERROR()
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@SeatRouter.delete("/seat")
def delete_multi_seat(IDs:SeatDelete,user=Depends(ManagementUser),db=Depends(get_db)):
    deleted = []
    if user.get("role") == "Admin":
        for i in IDs.ids:
            if SeatService(db).delete(i):
                deleted.append(i)
    else:
        for i in IDs.ids:
            STObj = SeatService(db).type(i)
            if STObj is None:
                continue
            Event = EventService(db).find(STObj.get("event"))
            if Event is None:
                continue
            if Event.get("owner") == user.get("_id"):
                if SeatService(db).delete(i):
                    deleted.append(i)
    return Response(
        status=200,
        message="Delete Seat",
        metadata=deleted
    )

@SeatRouter.put("/seattype/{SeatType_ID}",response_model=SeatTypeView)
def update_price(SeatTypeInfo:SeatTypeUpdate,SeatType_ID:int,user=Depends(ManagementUser),db=Depends(get_db)):
    STObj = SeatTypeService(db).findByID(SeatType_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(STObj.get("event"))
    if Event.get("owner") == user.get("_id") or user.get("role") == "Admin":
        metadata = SeatTypeService(db).update(SeatType_ID,SeatTypeInfo)
        if metadata is None:
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to update SeatType!")
        return Response(
            message="Update SeatType",
            metadata=metadata,
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")

    
