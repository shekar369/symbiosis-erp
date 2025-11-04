from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_holidays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement holiday listing
    return {"message": "Holiday management - to be implemented"}


@router.post("/")
async def create_holiday(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement holiday creation
    return {"message": "Holiday creation - to be implemented"}
