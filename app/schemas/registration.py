from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class RegistrationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class OrganizationRegistrationBase(BaseModel):
    name: str
    business_type: str
    registration_number: str
    tax_id: str
    contact_person: str
    email: EmailStr
    phone: str
    address: str
    employee_count: int
    website: Optional[str] = None
    notes: Optional[str] = None


class OrganizationRegistrationCreate(OrganizationRegistrationBase):
    pass


class OrganizationRegistrationUpdate(BaseModel):
    status: RegistrationStatus
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None


class OrganizationRegistrationResponse(OrganizationRegistrationBase):
    id: int
    status: RegistrationStatus
    tenant_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None

    class Config:
        from_attributes = True