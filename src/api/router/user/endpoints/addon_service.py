from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import AddonService,EventService
from api.response import Response,HTTP_404_NOT_FOUND
AddonRouter = APIRouter(
    tags = ["View - AddonService"],
    dependencies=[
        Depends(get_db)
    ]
)

@AddonRouter.get("/addons/{Event_ID}")
def view_addon_services(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata=AddonService(db).all(
            Manager_ID=event['owner'],
            Event_ID=event['id']
        )
    )

@AddonRouter.get("/addon/{Addon_ID}")
def view_addon_services(Addon_ID:int,db = Depends(get_db)):
    addon = AddonService(db).find(Addon_ID)
    if addon is None:
        raise HTTP_404_NOT_FOUND("Addon Service Not Found")
    return Response(
        metadata=addon
    )

    
