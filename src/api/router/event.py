from fastapi import APIRouter,Depends,Query
from api.auth.dependencies import ManagementUser
from api.service import EventService
from api.schema import EventCreate,EventDetail,EventPatch,EventPut,EventView
from core.database.mysql import get_db
from api.response import Response,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_403_FORBIDDEN,HTTP_204_NO_CONTENT

EventRouter = APIRouter(
    tags=["Event"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)
@EventRouter.get("/events",response_model=EventView)
def all_events(
    user = Depends(ManagementUser), db = Depends(get_db),
    name = Query(""),
    location = Query(""),
    start_date = Query(None),
    end_date = Query(None)
):
    metadata = EventService(db).all(
        Owner_ID= None if user.get("role") == "Admin" else user.get("_id"),
        Name=name,
        Location=location,
        Start_Date=start_date,
        End_Date=end_date,
    )
    return Response(
        metadata=metadata
    )
    
@EventRouter.get("/event/{Event_ID}",response_model=EventDetail)
def detail_event(
    Event_ID:int,user = Depends(ManagementUser), db = Depends(get_db)
):
    metadata = EventService(db).detail(Event_ID);
    if metadata is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") != "Admin" and metadata.get("owner") != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    
    return Response(
        metadata=metadata    
    )
    

@EventRouter.post("/event",response_model=EventView)
def create_event(Event:EventCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    Event = EventService(db).add(Event,user.get("_id"))
    if Event is None:
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to create Event!")
    return Response(
        status=201,
        metadata=Event
    )
    

@EventRouter.put("/event/{Event_ID}",response_model=EventView)
def update_event(EventPut:EventPut,Event_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    EventTable = EventService(db)
    # ---------------------------------#
    Event = EventTable(db).find(Event_ID)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") != "Admin" and user.get("_id") != Event['owner']:
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    Event = EventTable(db).put(Event_ID,EventPut)
    if Event is None:
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to update Event!")
    return Response(
        message="Updated Event",
        metadata=Event,
    )

    

@EventRouter.patch("/event/{Event_ID}",response_model=EventView)
def patch_event(Event_ID:int,EventPatch:EventPatch,user = Depends(ManagementUser), db = Depends(get_db)):
    EventTable = EventService(db)
    #----------------------------------#
    Event = EventTable.find(Event_ID)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    Event = EventTable.patch(Event_ID,EventPatch)
    if Event is None:
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to patch Event!")
    return Response(
        status=200,
        message="Updated Event",
        metadata=Event
    )
    

@EventRouter.delete("/event/{Event_ID}")
def delete_event(Event_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    EventTable = EventService(db)
    Event = EventTable.find(Event_ID)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") == "Admin" or user.get("_id") == Event.id:
        EventTable.delete(Event_ID)
        raise HTTP_204_NO_CONTENT()
    raise HTTP_403_FORBIDDEN("Access Forbidden ")