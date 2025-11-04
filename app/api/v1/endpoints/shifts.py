from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_shifts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement shift listing
    return {"message": "Shift management - to be implemented"}


@router.post("/")
async def create_shift(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement shift creation
    return {"message": "Shift creation - to be implemented"}
