from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.auth.dependencies import ManagementUser
from api.service import ShowService,EventService
from api.response import *
from api.schema import *
from datetime import time

ShowRouter = APIRouter(
    tags=["Show"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@ShowRouter.get("/shows",response_model=ShowView)
def all_shows(
    user = Depends(ManagementUser), db = Depends(get_db),
    event = Query(None),
    date = Query(None)
    ):
    metadata = ShowService(db).all(
        Owner_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID=event,
        Date=date,
    )
    return Response(
        message="All Show",
        metadata=metadata
    )

@ShowRouter.post('/show',response_model=ShowView)
def add_show(ShowInfo:ShowCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    ShowTable = ShowService(db)
    #-----------------------------#
    EventObj = EventService(db).find(ShowInfo.event)
    if EventObj is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if not(user.get("role") == "Admin" or user.get("_id") == EventObj.get("owner")):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    holder = ShowTable.find(Name=ShowInfo.name,Event_ID=ShowInfo.event)        
    if holder:
        raise HTTP_409_CONFLICT("Show Existed")
    if ShowInfo.end <= ShowInfo.start:
        raise HTTP_400_BAD_REQUEST("End time cannot be before or equal to start time")
    #--Check conflic time--#
    ShowOnDate = ShowTable.all(user.get("_id"),EventObj.get("id"),ShowInfo.date)    
    for show in ShowOnDate:
        newTL = [ShowInfo.start, ShowInfo.end]
        oldTL = list(map(lambda t: time(*map(int, t.split(':'))), [show.get("start"), show.get("end")]))
        if (newTL[0] < oldTL[1] and newTL[1] > oldTL[0]) or (oldTL[0] < newTL[1] and oldTL[1] > newTL[0]):
            raise HTTP_409_CONFLICT(f"Conflict Time with Show {show.get('name')} (id={show.get('id')})")        
    #-----------------#
    NewShow = ShowTable.add(ShowInfo)
    if not NewShow:
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to create Show!")        
    return Response(
        status=201,
        message="New Show",
        metadata=NewShow
    )
        
    

@ShowRouter.put("/show/{Show_ID}", response_model=ShowView)
def update_show(Show_ID:int,ShowInfo:ShowUpdate,user = Depends(ManagementUser), db = Depends(get_db)):
    ShowTable = ShowService(db)
    HolderShow = ShowTable.find(Show_ID=Show_ID)
    if HolderShow is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    # ---- #
    EventObj = EventService(db).find(HolderShow.get("event"))
    if not(user.get("role") == "Admin" or user.get("_id") == EventObj.get("owner")):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    # ---- # 
    ShowObj = ShowTable.find(HolderShow.get("id"))
    if ShowObj.get("name") == ShowInfo.name:
        raise HTTP_409_CONFLICT("Show.name Existed")
    # ---- #
    ShowOnDate = []
    if ShowInfo.date:
        ShowOnDate = ShowTable.all(user.get("_id"),EventObj.get("id"),ShowInfo.date)
    else:
        ShowOnDate = ShowTable.all(user.get("_id"),EventObj.get("id"),HolderShow.get("date"))
    for show in ShowOnDate:
        if show.get("id") == Show_ID:
            continue
        # Check
        newTL = [HolderShow.get("start") if ShowInfo.start is None else ShowInfo.start,HolderShow.get("end") if ShowInfo.end is None else ShowInfo.end]
        oldTL = [show.get("start"),show.get("end")]
        if (newTL[0] < oldTL[1] and newTL[1] > oldTL[0]) or (oldTL[0] < newTL[1] and oldTL[1] > newTL[0]):
            raise HTTP_409_CONFLICT(f"Conflict Time with Show {show.get('name')} (id={show.get('id')})")        
    UpdatedShow = ShowTable.update(Show_ID,ShowInfo)
    if UpdatedShow:
        return Response(
            message="Updated Show",
            metadata=UpdatedShow,
        )
    raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to update Show!")
    

@ShowRouter.delete("/show/{Show_ID}")
def delete_show(Show_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    ShowTable = ShowService(db)
    ShowObj = ShowTable.find(Show_ID=Show_ID)
    if ShowObj is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    EventObj = EventService(db).find(ShowObj.get("event"))
    if user.get("role") == "Admin" or user.get("_id") == EventObj.get("owner"):
        if ShowTable.delete(Show_ID):
            raise HTTP_204_NO_CONTENT()
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to delete Show!")
    raise HTTP_403_FORBIDDEN("Access Forbidden")


