from fastapi import APIRouter,Depends,Query
from api.auth.dependencies import ManagementUser
from api.service import FeedbackService,EventService
from api.schema import FeedbackView,FeedbackUpdate,FeedbackCreate
from core.database.mysql import get_db
from api.response import Response,HTTP_404_NOT_FOUND,HTTP_204_NO_CONTENT,HTTP_403_FORBIDDEN

FeedBackRouter = APIRouter(
    tags=["Manage - Feedback"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@FeedBackRouter.get("/feedbacks",response_model=FeedbackView)
def manage_feedbacks(
    user = Depends(ManagementUser),db = Depends(get_db),
    event = Query(None)
    ):
    metadata = FeedbackService(db).all(
        Manager_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID   = event
    )
    return Response(
        metadata = metadata
    )
    
@FeedBackRouter.get("/feedback/{Feedback_ID}",response_model=FeedbackView)
def view_feed_back(Feedback_ID:int,user = Depends(ManagementUser),db = Depends(get_db)):
    instance = FeedbackService(db).find(Feedback_ID)
    if instance is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    return Response(
        metadata = instance
    )

@FeedBackRouter.delete("/feedback/{Feedback_ID}")
def delete_feed_back(Feedback_ID:int,user = Depends(ManagementUser),db = Depends(get_db)):
    feedback = FeedbackService(db).find(Feedback_ID)
    if feedback is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    event = EventService(db).find(feedback.get("event"))
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    FeedbackService(db).delete(Feedback_ID)
    raise HTTP_204_NO_CONTENT()

@FeedBackRouter.put("/feedback/{Feedback_ID}")
def update_feed_back(Feedback_ID:int,Information:FeedbackUpdate,user = Depends(ManagementUser),db = Depends(get_db)):
    feedback = FeedbackService(db).find(Feedback_ID)
    if feedback is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    event = EventService(db).find(feedback.get("event"))
    if user.get("role") != "Admin" and user.get("_id") != event.get("owner"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    NewFeedBack = FeedbackService(db).update(Feedback_ID,Information)
