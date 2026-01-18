from pydantic import BaseModel
from datetime import date
from typing import Optional


class HolidayBase(BaseModel):
    name: str
    date: date
    is_mandatory: bool = True
    description: Optional[str] = None


class HolidayCreate(HolidayBase):
    pass


class HolidayUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    is_mandatory: Optional[bool] = None
    description: Optional[str] = None


class HolidayResponse(HolidayBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True


class BulkHolidayCreate(BaseModel):
    """For creating multiple holidays at once (e.g., yearly calendar)"""
    holidays: list[HolidayCreate]


# Working Calendar Schemas
class WorkingCalendarCreate(BaseModel):
    monday: bool = True
    tuesday: bool = True
    wednesday: bool = True
    thursday: bool = True
    friday: bool = True
    saturday: bool = False
    sunday: bool = False


class WorkingCalendarResponse(WorkingCalendarCreate):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
