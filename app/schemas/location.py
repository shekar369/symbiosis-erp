from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.location import FacilityType, ActType


# State Schemas
class StateBase(BaseModel):
    name: str
    code: str  # AP, TG, KA, TN, MH
    is_active: bool = True


class StateCreate(StateBase):
    pass


class StateUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None


class StateResponse(StateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Location Schemas
class LocationBase(BaseModel):
    name: str
    city: str
    facility_type: FacilityType = FacilityType.REGULAR
    act_type: ActType
    address_line1: str
    address_line2: Optional[str] = None
    postal_code: str  # 6-digit pincode
    is_active: bool = True


class LocationCreate(LocationBase):
    state_id: int
    tenant_id: int


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state_id: Optional[int] = None
    facility_type: Optional[FacilityType] = None
    act_type: Optional[ActType] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None


class LocationResponse(LocationBase):
    id: int
    state_id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime
    state: Optional[StateResponse] = None

    class Config:
        from_attributes = True


# Employee Location Assignment Schemas
class EmployeeLocationAssignmentBase(BaseModel):
    employee_id: int
    location_id: int
    from_date: datetime = Field(default_factory=datetime.utcnow)
    to_date: Optional[datetime] = None
    is_current: bool = True


class EmployeeLocationAssignmentCreate(EmployeeLocationAssignmentBase):
    pass


class EmployeeLocationAssignmentUpdate(BaseModel):
    to_date: datetime
    is_current: bool = False


class EmployeeLocationAssignmentResponse(EmployeeLocationAssignmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    created_at: datetime
    location: Optional[LocationResponse] = None

    class Config:
        from_attributes = True
