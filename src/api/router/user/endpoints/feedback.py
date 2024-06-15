from fastapi import APIRouter,Depends
from core.database.mysql import get_db
from api.auth.dependencies import login_required
FeedBackRouter = APIRouter(
    dependencies=[
        Depends(login_required),
        Depends(get_db)
    ]
)

