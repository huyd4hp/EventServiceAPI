from fastapi import APIRouter,Depends,Query
from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from api.service import AddonService,EventService
from api.response import Response,HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_403_FORBIDDEN,HTTP_204_NO_CONTENT
from api.schema import AddonView,AddonCreate,AddonUpdate

AddonServiceRouter = APIRouter(
    tags=["Manage - AddonService"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@AddonServiceRouter.get('/addon-services',response_model=AddonView)
def manage_addon_services(event = Query(None),user = Depends(ManagementUser), db = Depends(get_db)):
    metadata = AddonService(db).all(
        Manager_ID = None if user.get("role") == "Admin" else user.get("_id"),
        
        Event_ID = event,
    )
    return Response(
        message = "List Addon Services",
        metadata= metadata
    )

@AddonServiceRouter.get('/addon-service/{Addon_ID}',response_model=AddonView)
def view_addon_service(Addon_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    addon_instance = AddonService(db).find(Addon_ID)
    if addon_instance is None:
        raise HTTP_404_NOT_FOUND("Addon Service Not Found")
    event_instance = EventService(db).find(addon_instance.get("event"))
    if user.get("role") != "Admin" and event_instance.get("owner") != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    return Response(
        message = "List Addon Services",
        metadata= addon_instance
    )

@AddonServiceRouter.delete('/addon-service/{Addon_ID}',response_model=AddonView)
def delete_addon_service(Addon_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    addon_instance = AddonService(db).find(Addon_ID)
    if addon_instance is None:
        raise HTTP_404_NOT_FOUND("Addon Service Not Found")
    event_instance = EventService(db).find(addon_instance.get("event"))
    if user.get("role") != "Admin" and event_instance.get("owner") != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    AddonService(db).delete(Addon_ID)
    raise HTTP_204_NO_CONTENT()

@AddonServiceRouter.post("/addon-service",response_model=AddonView)
def view_addon_service(Information:AddonCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    event_instance = EventService(db).find(Information.event)
    if event_instance is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") != "Admin" and event_instance.get("owner") != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    for addon in AddonService(db).all(Owner_ID=event_instance.get("owner"),Event_ID=event_instance.get("id")):
        if addon.get("name").lower() == Information.name.lower():
            raise HTTP_409_CONFLICT(f"Addon Service Name Existed (Conflict ID:{addon.get("id")})")
    NewAddon = AddonService(db).add(Information)
    return Response(
        status=201,
        message="Created Addon Service",
        metadata=NewAddon,
    )

@AddonServiceRouter.put("/addon-service/{Addon_ID}",response_model=AddonView)
def view_addon_service(Addon_ID:int,Information:AddonUpdate,user = Depends(ManagementUser), db = Depends(get_db)):
    addon_instance = AddonService(db).find(Addon_ID)
    if addon_instance is None:
        raise HTTP_404_NOT_FOUND("Addon Service Not Found")
    event_instance = EventService(db).find(addon_instance.get("event"))
    if user.get("role") != "Admin" and event_instance.get("owner") != user.get("_id"):
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    if Information.name:
        for addon in AddonService(db).all(
            Owner_ID=event_instance.get("owner"),
            Event_ID=event_instance.get("id")
        ):
            if addon.get("name").lower() == Information.name.lower() and addon.get("id") != Addon_ID:
                raise HTTP_409_CONFLICT(f"Addon Service Name Existed (Conflict ID:{addon.get("id")})")
    NewAddon = AddonService(db).update(Addon_ID,Information)
    return Response(
        message = "Updated Addon Service",
        metadata= NewAddon,
    )
    
    

