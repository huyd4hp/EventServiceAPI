from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.service import EventService,ShowService,SeatService,SeatTypeService
from api.response import Response,HTTP_404_NOT_FOUND
EventRouter = APIRouter(
    tags = ["View - Event"],
    dependencies=[
        Depends(get_db)
    ]
)

@EventRouter.get("/events")
def list_events(db = Depends(get_db)):
    events = EventService(db).all()
    for event in events:
        del event['about']
        event['attendees'] = 0
        event['remainning'] = 0
        # attendees 
        for st in SeatTypeService(db).all(Owner_ID=event['owner'],Event_ID=event['id']):
            event['attendees'] += len(SeatService(db).all(Owner_ID = event['owner'],Type=st['id'],Status="Ordered"))
            event['remainning'] += len(SeatService(db).all(Owner_ID = event['owner'],Type=st['id'],Status="NOT_ORDERED"))
        # price
        event['price'] = "free"
        price = []
        for st in SeatTypeService(db).all(Owner_ID=event['owner'],Event_ID=event['id']):
            price.append(st.get("price"))
        if len(set(price)) == 1 and set(price)[0] > 0:
            event['price'] = set(price)[0]
        if len(set(price)) > 1:
            event['price'] = f"From {min(price)}"
        # Shows - Agenda
        event['show'] = ShowService(db).all(Owner_ID=event['owner'],Event_ID=event['id'])
    return Response(
        message="List Events",
        metadata= events
    )

@EventRouter.get("/event/{Event_ID}")
def view_event(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    event['attendees'] = 0
    event['remainning'] = 0
        # attendees 
    for st in SeatTypeService(db).all(Owner_ID=event['owner'],Event_ID=event['id']):
        event['attendees'] += len(SeatService(db).all(Owner_ID = event['owner'],Type=st['id'],Status="Ordered"))
        event['remainning'] += len(SeatService(db).all(Owner_ID = event['owner'],Type=st['id'],Status="NOT_ORDERED"))
        # price
    event['price'] = "free"
    price = []
    for st in SeatTypeService(db).all(Owner_ID=event['owner'],Event_ID=event['id']):
        price.append(st.get("price"))
    if len(set(price)) == 1 and set(price)[0] > 0:
        event['price'] = set(price)[0]
    if len(set(price)) > 1:
        event['price'] = f"From {min(price)}"
    # Shows - Agenda
    event['show'] = ShowService(db).all(Owner_ID=event['owner'],Event_ID=event['id'])

    return Response(
        metadata= event
    )
    