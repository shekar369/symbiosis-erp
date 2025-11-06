from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveType(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    days_per_year = Column(Float, nullable=False)  # max days per year
    is_paid = Column(Integer, default=1)  # 1 = paid, 0 = unpaid
    carry_forward = Column(Integer, default=0)  # 1 = yes, 0 = no
    max_carry_forward_days = Column(Float, default=0)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Float, default=0)
    used_days = Column(Float, default=0)
    balance_days = Column(Float, default=0)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Float, nullable=False)
    reason = Column(String)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
