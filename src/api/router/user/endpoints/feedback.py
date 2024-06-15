from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.auth.dependencies import User
from api.service import EventService,FeedbackService,SeatService,SeatTypeService
from api.schema import FeedbackCreate
from api.response import HTTP_404_NOT_FOUND,Response,HTTP_403_FORBIDDEN
FeedBackRouter = APIRouter(
    tags = ["View/Post - Feedback"],
    dependencies=[
        Depends(get_db)
    ]
)

@FeedBackRouter.get("/feedbacks/{Event_ID}")
def list_feedbacks(Event_ID:int, db = Depends(get_db)):
    if EventService(db).find(Event_ID) is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    return Response(
        metadata = FeedbackService(db).all(Event_ID=Event_ID)
    )

@FeedBackRouter.get("/feedback/{Feedback_ID}")
def view_feedback(Feedback_ID:int, db = Depends(get_db)):
    instance = FeedbackService(db).find(Feedback_ID)
    if instance is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    return Response(
        metadata = instance
    )

@FeedBackRouter.post("/feedback")
def feedback(Form:FeedbackCreate,user = Depends(User), db = Depends(get_db)):
    for seattype in SeatTypeService(db).all(Event_ID=Form.event):
        for seat in SeatService(db).all(Type=seattype.get("id"),Status="Ordered"):
            if user.get("_id") == seat.get("owner"):
                instance = FeedbackService(db).add(user.get("_id"),Form)
                return Response(
                    metadata = instance
                )
    raise HTTP_403_FORBIDDEN("Forbidden")
    


