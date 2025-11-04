from pydantic import BaseModel
from datetime import date
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


class LeaveTypeResponse(BaseModel):
    id: int
    name: str
    code: str
    max_days: Optional[float] = None
    carry_forward: bool = False

    class Config:
        from_attributes = True
