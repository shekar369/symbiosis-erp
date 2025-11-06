from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    date_of_joining: date
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    grade_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    tenant_id: Optional[int] = None  # Auto-assigned from authenticated user if not provided


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    grade_id: Optional[int] = None
    status: Optional[str] = None


class EmployeeProfileUpdate(BaseModel):
    """Schema for employee self-service profile updates - limited fields"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None


class EmployeeResponse(EmployeeBase):
    id: int
    tenant_id: int
    status: str
    date_of_leaving: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

