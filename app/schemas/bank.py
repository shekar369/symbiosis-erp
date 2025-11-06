from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BankDetailsBase(BaseModel):
    account_holder_name: str
    account_number: str
    bank_name: str
    branch_name: Optional[str] = None
    ifsc_code: str
    account_type: Optional[str] = None  # savings, current
    pan_number: Optional[str] = None


class BankDetailsCreate(BankDetailsBase):
    employee_id: int


class BankDetailsUpdate(BaseModel):
    account_holder_name: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_type: Optional[str] = None
    pan_number: Optional[str] = None


class BankDetailsResponse(BankDetailsBase):
    id: int
    employee_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
