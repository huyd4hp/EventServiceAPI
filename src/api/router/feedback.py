from fastapi import APIRouter,Depends,Query
from core.database.mysql import get_db
from api.auth.dependencies import User
from api.response import *
from api.schema import *
from api.service import FeedbackService,EventService


FeedBackRouter = APIRouter(
    tags=["FeedBack"],
    dependencies=[
        Depends(User),
        Depends(get_db)
    ]
)

@FeedBackRouter.get("/feedbacks",response_model=FeedbackView)
def all_feed_backs(user = Depends(User), db = Depends(get_db),
                   event = Query(None)):
    metadata = FeedbackService(db).all(
        User_ID=user.get("_id"),
        Role=user.get("role"),
        Event_ID=event
    )
    return Response(
        message = "All Feedbacks",
        metadata= metadata
    )

@FeedBackRouter.post("/feedback",response_model=FeedbackView)
def add_feed_back(FeedbackInfo:FeedbackCreate,user = Depends(User), db = Depends(get_db)):
    metadata = FeedbackService(db).add(user.get("_id"),FeedbackInfo,)
    if metadata is None:
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to create feedback")
    return Response(
        status=201,
        message="New Feedback",
        metadata=metadata,
    )

@FeedBackRouter.put("/feedback/{Feedback_ID}")
def update_feed_back(Feedback_ID:int, FeedBackInfo:FeedbackUpdate,user = Depends(User), db = Depends(get_db)):
    FBTable = FeedbackService(db)
    FBObj = FBTable.find(Feedback_ID)
    if FBObj is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    if user.get("role") == "Admin" or EventService(db).find(FBObj.get("event")) == user.get("_id") or FBObj.get("owner") == user.get("_id"):
        NewInstance = FBTable.update(Feedback_ID,FeedBackInfo)
        if NewInstance is None:
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to update Feedback")
        return Response(
            message="Updated Feedback",
            metadata=NewInstance,
        )
        
    raise HTTP_403_FORBIDDEN("Access Forbidden")
@FeedBackRouter.delete("/feedback/{Feedback_ID}")
def delete_fedd_back(Feedback_ID:int,user = Depends(User), db = Depends(get_db)):
    FeedbackTable = FeedbackService(db)
    #---------------_#
    FBObj = FeedbackTable.find(Feedback_ID)
    if FBObj is None:
        raise HTTP_404_NOT_FOUND("Feedback Not Found")
    if user.get("role") == "Admin" or EventService(db).find(FBObj.get("event")) == user.get("_id") or FBObj.get("owner") == user.get("_id"):
        deleted = FeedbackTable.delete(Feedback_ID)
        if Feedback_ID == deleted:
            raise HTTP_204_NO_CONTENT()
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to delete Feedback!")
    raise HTTP_403_FORBIDDEN("Access Forbidden")



