from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.auth.dependencies import ManagementUser
from api.service import SeatTypeService,EventService
from api.response import *
from api.schema import SeatTypeView,SeatTypeCreate,SeatTypeUpdate

SeatTypeRouter = APIRouter(
    tags=["Manage - Seat Type"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@SeatTypeRouter.get("/seattypes",response_model=SeatTypeView)
def manage_seat_types(
    user = Depends(ManagementUser), db = Depends(get_db),
    event = Query(None)
    ):
    metadata = SeatTypeService(db).all(
        Owner_ID= None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID= event,
    )
    return Response(
        message="List Seat Type",
        metadata=metadata,
    )

@SeatTypeRouter.get("/seattype/{SeatType_ID}",response_model=SeatTypeView)
def view_seat_type(SeatType_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    SeatType = SeatTypeService(db).find(ID=SeatType_ID)
    if SeatType is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(SeatType.get("event"))
    if Event['owner'] != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    return Response(
        metadata=SeatType
    )
   

@SeatTypeRouter.post("/seattype",response_model=SeatTypeView)
def create_seat_type(Information:SeatTypeCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    Event = EventService(db).find(Information.event)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    #------------------------#
    SeatTypeTable = SeatTypeService(db)
    if user.get("role") != "Admin" and user.get("_id") != Event['owner']:
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    for e in SeatTypeTable.all(Owner_ID=Event['owner'],Event_ID=Event['id']):
        if e['type'].lower() == Information.type.lower():
            raise HTTP_409_CONFLICT("SeatType Existed")
    NewST = SeatTypeTable.add(Information)
    return Response(
        status=201,
        message="Created SeatType",
        metadata=NewST
    )
    
        
@SeatTypeRouter.put("/seattype/{SeatType_ID}")#,response_model=SeatTypeView)
def update_seat_tye(SeatType_ID:int,Information:SeatTypeUpdate, user = Depends(ManagementUser), db = Depends(get_db)):
    SeatTypeTable = SeatTypeService(db)
    #---------------------#
    STObj = SeatTypeTable.find(SeatType_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(STObj['event'])
    if user.get("role") != "Admin" and Event['owner'] != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    NewST = SeatTypeTable.update(SeatType_ID,Information)
    return Response(
        status=200,
        message="Updated SeatType",
        metadata=NewST,
    )
    

@SeatTypeRouter.delete("/seattype/{SeatType_ID}")
def delete_seat_type(SeatType_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    STObj = SeatTypeService(db).find(ID=SeatType_ID)
    if STObj is None:
        raise HTTP_404_NOT_FOUND("SeatType Not Found")
    Event = EventService(db).find(STObj['event'])
    if user.get("role") != "Admin" and Event['owner'] != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    SeatTypeService(db).delete(SeatType_ID)
    raise HTTP_204_NO_CONTENT()
    
