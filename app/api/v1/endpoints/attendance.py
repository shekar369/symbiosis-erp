from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.crud.attendance import attendance as attendance_crud
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=AttendanceResponse)
async def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return attendance_crud.create_attendance(db=db, attendance=attendance)


@router.get("/", response_model=List[AttendanceResponse])
async def list_attendance(
    skip: int = 0,
    limit: int = 20,
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return attendance_crud.get_attendance_records(db=db, skip=skip, limit=limit, employee_id=employee_id)


@router.post("/upload")
async def upload_attendance(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement attendance upload from Excel/CSV
    return {"message": "Attendance upload - to be implemented", "filename": file.filename}
