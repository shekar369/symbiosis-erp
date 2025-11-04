from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class WageStatus(str, enum.Enum):
    DRAFT = "draft"
    CALCULATED = "calculated"
    APPROVED = "approved"
    PAID = "paid"


class WageStatement(Base):
    __tablename__ = "wage_statements"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Earnings
    basic_salary = Column(Float, default=0)
    total_earnings = Column(Float, default=0)

    # Deductions
    total_deductions = Column(Float, default=0)

    # Net
    net_salary = Column(Float, default=0)

    # Days
    total_days = Column(Integer, default=0)
    present_days = Column(Integer, default=0)
    absent_days = Column(Integer, default=0)
    leave_days = Column(Integer, default=0)

    # Detailed breakdown
    earnings_breakdown = Column(JSON)
    deductions_breakdown = Column(JSON)

    status = Column(Enum(WageStatus), default=WageStatus.DRAFT)
    calculated_at = Column(DateTime)
    approved_at = Column(DateTime)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
