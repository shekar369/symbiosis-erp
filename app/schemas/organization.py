from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    tenant_id: int


class DepartmentResponse(DepartmentBase):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DesignationBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DesignationCreate(DesignationBase):
    tenant_id: int


class DesignationResponse(DesignationBase):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GradeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class GradeCreate(GradeBase):
    tenant_id: int


class GradeResponse(GradeBase):
    id: int
    tenant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
