from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.service import EventService,SeatService,SeatTypeService,ShowService
from api.schema import EventQuery
from api.response import Response,HTTP_404_NOT_FOUND
EventRouter = APIRouter(
    tags = ["View - Event"],
    dependencies=[
        Depends(get_db)
    ]
)

@EventRouter.get("/events")
def list_events(Form:EventQuery = Depends(),db = Depends(get_db)):
    events = EventService(db).all()
    start = Form.offset + (Form.page - 1) * Form.limit
    end = start + Form.limit
    events = events[start:end]
    for event in events:
        event['attendates'] = 0
        event['left'] = 0
        event['price'] = "Free"
        event.pop('about')
        event.pop("end_date")
        seattypes = SeatTypeService(db).all(
            Manager_ID = event['owner'],
            Event_ID = event['id']
        )
        price= []
        for st in seattypes:
            price.append(st.get("price"))
            event['attendates'] += len(SeatService(db).all(Manager_ID= event['owner'],Type = st['id'],Status = 'Ordered'))
            event['left'] += len(SeatService(db).all(Manager_ID= event['owner'],Type = st['id'],Status = 'NOT_ORDERED'))

        event['show'] = ShowService(db).all(Manager_ID = event['owner'],Event_ID = event['id'])
        if len(price) == 1 and 0 in price:
            event['price'] = "Free"
        elif len(price) == 0:
            event['price'] = None
        else:
            event['price'] = f"From {min(price)}"
        
        
    return Response(
        metadata = events
    )
    
@EventRouter.get("/event/{Event_ID}")
def view_event(Event_ID:int,db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    event['attendates'] = 0
    event['left'] = 0
    event['price'] = "Free"
    seattypes = SeatTypeService(db).all(
        Manager_ID = event['owner'],
        Event_ID = event['id']
    )
    price= []
    for st in seattypes:
        price.append(st.get("price"))
        event['attendates'] += len(SeatService(db).all(Manager_ID= event['owner'],Type = st['id'],Status = 'Ordered'))
        event['left'] += len(SeatService(db).all(Manager_ID= event['owner'],Type = st['id'],Status = 'NOT_ORDERED'))

    event['show'] = ShowService(db).all(Manager_ID = event['owner'],Event_ID = event['id'])
    if len(price) == 1 and 0 in price:
        event['price'] = "Free"
    elif len(price) == 0:
        event['price'] = None
    else:
        event['price'] = f"From {min(price)}"
    return Response(
        metadata = event
    )