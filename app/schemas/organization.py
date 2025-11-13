from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DesignationBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DesignationCreate(DesignationBase):
    pass


class DesignationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class DesignationResponse(DesignationBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GradeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class GradeResponse(GradeBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
