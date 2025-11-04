from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/attendance")
async def attendance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement attendance report
    return {"message": "Attendance report - to be implemented"}


@router.get("/payroll")
async def payroll_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement payroll report
    return {"message": "Payroll report - to be implemented"}
