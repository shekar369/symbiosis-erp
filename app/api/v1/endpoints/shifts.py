from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import time

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.shift import Shift, ShiftAssignment

router = APIRouter()


# ─── Request schemas ────────────────────────────────────────────────────────────

class ShiftCreate(BaseModel):
    name: str
    code: str
    start_time: time
    end_time: time
    grace_time_minutes: Optional[int] = 0
    is_active: Optional[bool] = True


class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    grace_time_minutes: Optional[int] = None
    is_active: Optional[bool] = None


# ─── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/")
async def list_shifts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Return all shifts for the current tenant."""
    shifts = (
        db.query(Shift)
        .filter(Shift.tenant_id == current_user.tenant_id)
        .order_by(Shift.name)
        .all()
    )
    return [
        {
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "start_time": str(s.start_time),
            "end_time": str(s.end_time),
            "grace_time_minutes": s.grace_time_minutes,
            "is_active": s.is_active,
            "created_at": str(s.created_at),
        }
        for s in shifts
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shift(
    payload: ShiftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new shift for the current tenant."""
    existing = (
        db.query(Shift)
        .filter(Shift.code == payload.code)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Shift with code '{payload.code}' already exists",
        )

    shift = Shift(
        tenant_id=current_user.tenant_id,
        name=payload.name,
        code=payload.code,
        start_time=payload.start_time,
        end_time=payload.end_time,
        grace_time_minutes=payload.grace_time_minutes,
        is_active=payload.is_active,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return {
        "id": shift.id,
        "name": shift.name,
        "code": shift.code,
        "start_time": str(shift.start_time),
        "end_time": str(shift.end_time),
        "grace_time_minutes": shift.grace_time_minutes,
        "is_active": shift.is_active,
    }


@router.get("/{shift_id}")
async def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id, Shift.tenant_id == current_user.tenant_id)
        .first()
    )
    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return {
        "id": shift.id,
        "name": shift.name,
        "code": shift.code,
        "start_time": str(shift.start_time),
        "end_time": str(shift.end_time),
        "grace_time_minutes": shift.grace_time_minutes,
        "is_active": shift.is_active,
        "created_at": str(shift.created_at),
    }


@router.put("/{shift_id}")
async def update_shift(
    shift_id: int,
    payload: ShiftUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id, Shift.tenant_id == current_user.tenant_id)
        .first()
    )
    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(shift, field, value)
    db.commit()
    db.refresh(shift)
    return {"message": "Shift updated", "id": shift.id}


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id, Shift.tenant_id == current_user.tenant_id)
        .first()
    )
    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    db.delete(shift)
    db.commit()
