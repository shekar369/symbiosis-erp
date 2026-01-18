from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.holiday import WorkingCalendar
from app.schemas.holiday import WorkingCalendarCreate, WorkingCalendarResponse

router = APIRouter()


@router.get("/", response_model=Optional[WorkingCalendarResponse])
def get_working_calendar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the working calendar configuration for the current tenant"""
    working_calendar = db.query(WorkingCalendar).filter(
        WorkingCalendar.tenant_id == current_user.tenant_id
    ).first()

    return working_calendar


@router.post("/", response_model=WorkingCalendarResponse, status_code=status.HTTP_200_OK)
def create_or_update_working_calendar(
    calendar_data: WorkingCalendarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create or update the working calendar configuration"""
    # Check if working calendar already exists
    existing = db.query(WorkingCalendar).filter(
        WorkingCalendar.tenant_id == current_user.tenant_id
    ).first()

    if existing:
        # Update existing
        for field, value in calendar_data.model_dump().items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        working_calendar = WorkingCalendar(
            **calendar_data.model_dump(),
            tenant_id=current_user.tenant_id
        )
        db.add(working_calendar)
        db.commit()
        db.refresh(working_calendar)
        return working_calendar
