from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    grace_time_minutes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
