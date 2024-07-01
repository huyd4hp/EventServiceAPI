from fastapi import APIRouter,Depends
from fastapi import Response as FastResponse
from core.database.mysql import get_db
from api.service import EventService,SeatService,ShowService
from api.schema import EventQuery
from api.response import Response,HTTP_404_NOT_FOUND
from core.minio import MinIOClient
EventRouter = APIRouter(
    tags = ["View - Event"],
    dependencies=[
        Depends(get_db)
    ]
)

@EventRouter.get("/events")
def list_events(Form:EventQuery = Depends(),db = Depends(get_db)):
    events = EventService(db).all()
    for event in events:
        event.pop('about')
        event['attends'] = len(SeatService(db).all(Event_ID=event['id'],Status="Ordered"))
        event['left'] = len(SeatService(db).all(Event_ID=event['id'],Status="NotOrdered"))
        event['agenda'] = ShowService(db).all(Event_ID=event['id'])
    return Response(
        metadata = events
    )
    
@EventRouter.get("/event/{Event_ID}")
def view_event(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata = event
    )

@EventRouter.get('/image/{imageName}')
def view_image(imageName:str):
    image = MinIOClient.getImage(imageName)
    if not image:
        return Response(
            status=404,
            message="Image Not Found"
        )
    image_data = image.read()
    image_type = image.headers.get('Content-Type', 'image/jpeg')
    return FastResponse(content=image_data, media_type=image_type)
