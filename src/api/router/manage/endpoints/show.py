from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from datetime import datetime
from api.auth.dependencies import ManagementUser
from api.schema import ShowView,ShowCreate,ShowUpdate
from api.service import ShowService,EventService
from api.response import Response,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_204_NO_CONTENT,HTTP_409_CONFLICT,HTTP_400_BAD_REQUEST

ShowRouter = APIRouter(
    tags=["Manage - Show"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)
@ShowRouter.get("/shows",response_model=ShowView)
def manage_shows(
    user = Depends(ManagementUser), db = Depends(get_db),
    event = Query(None),date = Query(None)
    ):
    return Response(
        metadata= ShowService(db).all(
            Manager_ID = None if user.get("role") == "Admin" else user.get("_id"),
            Event_ID = event, Date= date,
        )
    )

@ShowRouter.get("/show/{Show_ID}",response_model=ShowView)
def view_show(Show_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    show = ShowService(db).find(Show_ID)
    if show is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    event = EventService(db).find(show.get("event"))
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    return Response(
        metadata = show
    )

@ShowRouter.delete("/show/{Show_ID}")
def delete_show(Show_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    show = ShowService(db).find(Show_ID)
    if show is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    event = EventService(db).find(show.get("event"))
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    ShowService(db).delete(Show_ID)
    EventService(db).__update__(event.get("id"))
    raise HTTP_204_NO_CONTENT()

@ShowRouter.post("/show",response_model=ShowView)
def create_show(Information:ShowCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    event = EventService(db).find(Information.event)
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    shows = ShowService(db).all(Manager_ID = user.get("_id"),Event_ID = Information.event)
    for show in shows:
        if show.get("name").lower() == Information.name.lower():
            raise HTTP_409_CONFLICT(f"Show Name Existed (Conflict ID:{show.get("id")})")
    if Information.start >= Information.end:
        raise HTTP_400_BAD_REQUEST("Error Timeline Show")
    shows = ShowService(db).all(Manager_ID = user.get("_id"),Event_ID = Information.event,Date=Information.date)
    for show in shows:
        if not (Information.end <= datetime.strptime(show.get("start"), "%H:%M:%S").time() 
                or 
                datetime.strptime(show.get("end"), "%H:%M:%S").time() <= Information.start):
            raise HTTP_409_CONFLICT(f"Conflict Timeline (Conflict ID:{show.get("id")})")
    show = ShowService(db).add(Information)
    EventService(db).__update__(event.get("id"))
    return Response(
        message = "Created Show",
        metadata = show
    )

@ShowRouter.put("/show/{Show_ID}",response_model=ShowView)
def update_show(Show_ID:int, Form:ShowUpdate,user = Depends(ManagementUser), db = Depends(get_db)):
    show = ShowService(db).find(Show_ID)
    if show is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    event = EventService(db).find(show.get("event"))
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    
    UpdateName = Form.name if Form.name else show.get("name")
    UpdateDate = Form.date if Form.date else show.get("date")
    UpdateStart = Form.start if Form.start else show.get("start")
    UpdateEnd = Form.end if Form.end else show.get("end")

    shows = ShowService(db).all(
        Manager_ID = event.get("owner"),
        Event_ID = event.get("id")
    )
    for show in shows:
        if show.get("name").lower() == UpdateName.lower():
            raise HTTP_409_CONFLICT(f"Show Name Existed (Conflict ID:{show.get("id")})")
    shows = ShowService(db).all(
        Manager_ID = event.get("owner"),
        Event_ID = event.get("id"),
        Date = UpdateDate,
    )
    for show in shows:
        if not (UpdateEnd <= datetime.strptime(show.get("start"), "%H:%M:%S").time() 
                or 
                datetime.strptime(show.get("end"), "%H:%M:%S").time() <= UpdateStart):
            raise HTTP_409_CONFLICT(f"Conflict Timeline (Conflict ID:{show.get("id")})")
    show = ShowService(db).update(Show_ID,Form)
    return Response(
        message = "Updated Show",
        metadata = show,
    )

    
    

    
    