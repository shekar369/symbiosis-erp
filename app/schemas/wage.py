from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class WageStatementBase(BaseModel):
    employee_id: int
    month: int
    year: int


class WageStatementCreate(WageStatementBase):
    pass


class WageStatementResponse(WageStatementBase):
    id: int
    basic_salary: float
    total_earnings: float
    total_deductions: float
    net_salary: float
    total_days: int
    present_days: int
    absent_days: int
    leave_days: int
    earnings_breakdown: Optional[Dict[str, Any]] = None
    deductions_breakdown: Optional[Dict[str, Any]] = None
    status: str
    calculated_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PayrollCalculationRequest(BaseModel):
    month: int
    year: int
    employee_ids: Optional[list[int]] = None
