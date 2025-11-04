from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class TenantBase(BaseModel):
    name: str
    slug: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
