from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveRequestUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    days: float
    status: str
    reason: Optional[str] = None

    class Config:
        from_attributes = True


class LeaveBalanceResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    total_leaves: float
    used_leaves: float
    balance_leaves: float

    class Config:
        from_attributes = True


class LeaveTypeCreate(BaseModel):
    name: str
    code: str
    days_per_year: float
    is_paid: bool = True
    carry_forward: bool = False
    max_carry_forward_days: float = 0
    description: Optional[str] = None


class LeaveTypeUpdate(BaseModel):
    name: Optional[str] = None
    days_per_year: Optional[float] = None
    is_paid: Optional[bool] = None
    carry_forward: Optional[bool] = None
    max_carry_forward_days: Optional[float] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class LeaveTypeResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    code: str
    days_per_year: float
    is_paid: bool
    carry_forward: bool
    max_carry_forward_days: float
    is_active: bool
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
