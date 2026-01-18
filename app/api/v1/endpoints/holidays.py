from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from typing import List, Optional
from datetime import date

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.holiday import Holiday
from app.schemas.holiday import (
    HolidayCreate,
    HolidayUpdate,
    HolidayResponse,
    BulkHolidayCreate
)

router = APIRouter()


@router.get("/", response_model=List[HolidayResponse])
def list_holidays(
    year: Optional[int] = Query(None, description="Filter by year"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month"),
    is_mandatory: Optional[bool] = Query(None, description="Filter by mandatory/optional"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all holidays for the current tenant"""
    query = db.query(Holiday).filter(Holiday.tenant_id == current_user.tenant_id)

    if year:
        query = query.filter(extract('year', Holiday.date) == year)
    if month:
        query = query.filter(extract('month', Holiday.date) == month)
    if is_mandatory is not None:
        query = query.filter(Holiday.is_mandatory == is_mandatory)

    holidays = query.order_by(Holiday.date).all()
    return holidays


@router.post("/", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED)
def create_holiday(
    holiday_data: HolidayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new holiday"""
    existing = db.query(Holiday).filter(
        Holiday.tenant_id == current_user.tenant_id,
        Holiday.date == holiday_data.date
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A holiday already exists on {holiday_data.date}"
        )

    holiday = Holiday(**holiday_data.model_dump(), tenant_id=current_user.tenant_id)
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return holiday


@router.put("/{holiday_id}", response_model=HolidayResponse)
def update_holiday(
    holiday_id: int,
    holiday_data: HolidayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing holiday"""
    holiday = db.query(Holiday).filter(
        Holiday.id == holiday_id,
        Holiday.tenant_id == current_user.tenant_id
    ).first()

    if not holiday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")

    update_data = holiday_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(holiday, field, value)

    db.commit()
    db.refresh(holiday)
    return holiday


@router.delete("/{holiday_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holiday(
    holiday_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a holiday"""
    holiday = db.query(Holiday).filter(
        Holiday.id == holiday_id,
        Holiday.tenant_id == current_user.tenant_id
    ).first()

    if not holiday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")

    db.delete(holiday)
    db.commit()
    return None
