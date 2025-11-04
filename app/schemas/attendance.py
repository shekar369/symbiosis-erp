from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str = "present"


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    id: int
    hours_worked: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceUploadResponse(BaseModel):
    id: int
    file_name: str
    total_records: int
    successful_records: int
    failed_records: int
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
