from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.auth.dependencies import login_required,User
from api.schema import FeedbackCreate
from api.service import EventService,SeatService,SeatTypeService,FeedbackService
from api.response import HTTP_404_NOT_FOUND,Response,HTTP_403_FORBIDDEN

FeedBackRouter = APIRouter(
    tags = ["View/Post - Feedback"],
    dependencies=[
        Depends(User),
        Depends(get_db)
    ]
)

@FeedBackRouter.post("/feedback")
def feedback_event(Form:FeedbackCreate,user = Depends(User), db = Depends(get_db)):
    event = EventService(db).find(Form.event)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    seattypes = SeatTypeService(db).all(
        Manager_ID = event['owner'],
        Event_ID = event['id']
    )
    seats = []
    for st in seattypes:
        seats += SeatService(db).all(
            Manager_ID=event['owner'],
            Type = st.get("id")
        )
    for seat in seats:
        if seat.get("owner") == user.get("_id"):
            feedback = FeedbackService(db).add(Form)
            return Response(
                metadata = feedback
            )
    raise HTTP_403_FORBIDDEN("Forbidden")
            

@FeedBackRouter.get("/feedback/{Event_ID}")
def view_feedback(Event_ID:int,user = Depends(User), db = Depends(get_db)):
    event = EventService(db).find(Event_ID)
    if event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata = FeedbackService(db).all(Manager_ID=event['owner'],Event_ID= event['id'])
    )
    
    
    
