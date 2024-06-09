from fastapi import APIRouter,Depends
from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from api.service import VoucherService,EventService
from api.schema import VoucherView,VoucherCreate,VoucherUpdate
from api.response import Response,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT,HTTP_204_NO_CONTENT

VoucherRouter = APIRouter(
    tags=["Voucher"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@VoucherRouter.get("/vouchers",response_model=VoucherView)
def all_voucher(user = Depends(ManagementUser), db = Depends(get_db)):
    metadata = VoucherService(db).all(
        Owner_ID = None if user.get("role") == "Admin" else user.get("_id")
    )
    return Response(
        message="All Vouchers",
        metadata=metadata
    )

@VoucherRouter.post("/voucher", response_model=VoucherView)
def create_voucher(VoucherInfo:VoucherCreate,user = Depends(ManagementUser), db = Depends(get_db)):
    Event = EventService(db).find(VoucherInfo.event)
    if Event is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if user.get("role") == "Admin" or Event.get("owner") == user.get("_id"):
        holder = VoucherService(db).find(VoucherInfo)
        if holder:
            raise HTTP_409_CONFLICT("Voucher Existed")
        VoucherObj = VoucherService(db).add(VoucherInfo)
        if VoucherObj is None:
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to create Voucher!")
        return Response(
            status=201,
            message="New Voucher",
            metadata=VoucherObj,
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")


@VoucherRouter.delete("/voucher/{Voucher_ID}")
def delete_voucher(Voucher_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    obj = VoucherService(db).findByID(Voucher_ID)
    if obj is None:
        raise HTTP_404_NOT_FOUND("Voucher_ID Not Found")
    Event = EventService(db).find(obj.get("id"))
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        if VoucherService(db).delete(Voucher_ID) == Voucher_ID:
            raise HTTP_204_NO_CONTENT()
        raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to delete Voucher!")
    raise HTTP_403_FORBIDDEN("Access Forbidden")

@VoucherRouter.put("/voucher/{Voucher_ID}")
def update_voucher(Voucher_ID:int,VoucherInfo:VoucherUpdate,user = Depends(ManagementUser), db = Depends(get_db)):
    obj = VoucherService(db).findByID(Voucher_ID)
    if obj is None:
        raise HTTP_404_NOT_FOUND("Voucher_ID Not Found")
    Event = EventService(db).find(obj.get("id"))
    if user.get("role") == "Admin" or user.get("_id") == Event.get("owner"):
        metadata = VoucherService(db).update(Voucher_ID,VoucherInfo)
        if metadata is None: 
            raise HTTP_500_INTERNAL_SERVER_ERROR("Failed to delete Voucher!")
        return Response(
            status=200,
            message="Updated Voucher",
            metadata=metadata
        )
    raise HTTP_403_FORBIDDEN("Access Forbidden")





