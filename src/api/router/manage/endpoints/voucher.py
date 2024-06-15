from api.auth.dependencies import ManagementUser
from core.database.mysql import get_db
from fastapi import APIRouter,Depends,Query
from api.service import VoucherService,EventService
from api.schema import VoucherView,VoucherCreate,VoucherUpdate
from api.response import HTTP_204_NO_CONTENT,HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_403_FORBIDDEN,Response
VoucherRouter = APIRouter(
    tags=["Manage - Voucher"],
    dependencies=[
        Depends(ManagementUser),
        Depends(get_db)
    ]
)

@VoucherRouter.get("/vouchers",response_model=VoucherView)
def manage_voucher(
    user = Depends(ManagementUser), db = Depends(get_db),
    event = Query(None)
):
    metadata = VoucherService(db).all(
        Manager_ID = None if user.get("role") == "Admin" else user.get("_id"),
        Event_ID= event,
    )
    return Response(
        message="List Voucher",
        metadata = metadata
    )

@VoucherRouter.get("/voucher/{Voucher_ID}",response_model=VoucherView)
def view_voucher(
    Voucher_ID:int,user = Depends(ManagementUser), db = Depends(get_db),
):
    VObj = VoucherService(db).find(Voucher_ID)
    if VObj is None:
        raise HTTP_404_NOT_FOUND("Voucher Not Found")
    EObj = EventService(db).find(VObj['event'])
    if EObj.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    return Response(
        metadata=VObj,
    )

@VoucherRouter.post("/voucher")#,response_model=VoucherView)

def create_voucher(
    Information:VoucherCreate,user = Depends(ManagementUser), db = Depends(get_db),
):
    enstance = EventService(db).find(Information.event)
    if enstance is None:
        raise HTTP_404_NOT_FOUND("Event Not Found")
    if enstance.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    for voucher in VoucherService(db).all(Manager_ID = enstance.get("owner"),Event_ID = enstance.get("id")):
        if voucher.get("name").lower() == Information.name.lower():
            raise HTTP_409_CONFLICT(f"VoucherName Existed (Conflict {voucher.get("id")})")
    NewVoucher = VoucherService(db).add(Information)
    return Response(
        message = "Created Voucher",
        metadata = NewVoucher
    )
    
@VoucherRouter.put("/voucher/{Voucher_ID}",response_model=VoucherView)
def update_voucher(Voucher_ID:int,Information:VoucherUpdate,
                   user = Depends(ManagementUser), db = Depends(get_db)):
    vnstance = VoucherService(db).find(Voucher_ID)
    if vnstance is None:
        raise HTTP_404_NOT_FOUND("Voucher Not Found")
    enstance  = EventService(db).find(vnstance.get("event"))
    if enstance.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    NewVoucher = VoucherService(db).update(Voucher_ID,Information)

    return Response(
        message = "Updated Voucher",
        metadata = NewVoucher
    )

@VoucherRouter.delete("/voucher/{Voucher_ID}")
def delete_voucher(Voucher_ID:int,user = Depends(ManagementUser), db = Depends(get_db)):
    vnstance = VoucherService(db).find(Voucher_ID)
    if vnstance is None:
        raise HTTP_404_NOT_FOUND("Voucher Not Found")
    enstance  = EventService(db).find(vnstance.get("event"))
    if enstance.get("owner") != user.get("_id") and user.get("role") != "Admin":
        raise HTTP_403_FORBIDDEN("Access Forbidden")
    VoucherService(db).delete(Voucher_ID)
    raise HTTP_204_NO_CONTENT()
