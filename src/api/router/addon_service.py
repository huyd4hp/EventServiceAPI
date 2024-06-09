from fastapi import APIRouter,Depends,Query
from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from api.service import AddonService as AS
from api.service import EventService
from api.response import *
from api.schema import *

AddonServiceRouter = APIRouter(
    tags=["Addon Service"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@AddonServiceRouter.get("/addon-services",response_model=AddonView) 
def all_addon_service(
    user = Depends(ManagementUser), db = Depends(get_db),
    event = Query(None)
):
    metadata = AS(db).all(
        Owner_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID=event,
    )
    return Response(
        message="All Addon-Service",
        metadata=metadata
    )

@AddonServiceRouter.post("/addon-service",response_model=AddonView)
def add_addon_service(
    AddonInfo:AddonCreate,
    user = Depends(ManagementUser), db = Depends(get_db)
):
    Event = EventService(db).find(AddonInfo.event)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        ASObj = AS(db).find(AddonInfo.name,AddonInfo.event)
        if ASObj:
            raise HTTP_409_CONFLICT("AddonService Existed")
        NewAS = AS(db).add(AddonInfo)
        if NewAS is None:
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to create AddonService!")
        return Response(
            status=201,
            message="New Addon Service",
            metadata=NewAS,
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@AddonServiceRouter.put("/addon-service/{Service_ID}")
def update_service(
    Service_ID:int,AddonInfo:AddonUpdate,
    user = Depends(ManagementUser), db = Depends(get_db)):
    ASObj = AS(db).findByID(Service_ID)
    if ASObj is None:
        raise HTTP_404_NOT_FOUND("Service Not Found")
    Event = EventService(db).find(ASObj.get("event"))
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        NewAS = AS(db).update(Service_ID,AddonInfo)
        if NewAS is None:
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to update AddonService!")
        return Response(
            message="Updated AddonSerivce",
            metadata=NewAS
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")
    

@AddonServiceRouter.delete("/addon-service/{Service_ID}")
def delete_service(Service_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    ASObj = AS(db).findByID(Service_ID)
    if ASObj is None:
        raise HTTP_404_NOT_FOUND("Service Not Found")
    Event = EventService(db).find(ASObj.get("event"))
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        if AS(db).delete(Service_ID):
            raise HTTP_204_NO_CONTENT()
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to delete AddonService!")
    raise HTTP_403_FORBIDDEN("Access Forbidden")
    