from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import ShowService,EventService
from api.response import Response,HTTP_404_NOT_FOUND
ShowRouter = APIRouter(
    tags = ["View - Show"],
    dependencies=[
        Depends(get_db)
    ]
)

@ShowRouter.get("/shows/{Event_ID}")
def list_shows(Event_ID:int,db=Depends(get_db)):
    if EventService(db).find(Event_ID) is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata=ShowService(db).all(Event_ID=Event_ID)
    ) 

@ShowRouter.get("/show/{Show_ID}")
def view_show(Show_ID:int,db=Depends(get_db)):
    show = ShowService(db).find(Show_ID)
    if show is None:
        raise HTTP_404_NOT_FOUND("Show Not Found")
    return Response(
        metadata=show
    )