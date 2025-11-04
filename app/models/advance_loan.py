from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum, DateTime
from datetime import datetime
import enum

from app.db.base import Base


class LoanStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DEFAULTED = "defaulted"


class Advance(Base):
    __tablename__ = "advances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    reason = Column(String)
    approved_by = Column(Integer, ForeignKey("users.id"))
    deducted_amount = Column(Float, default=0)
    remaining_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    loan_type = Column(String, nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, default=0)
    tenure_months = Column(Integer, nullable=False)
    monthly_emi = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    paid_amount = Column(Float, default=0)
    remaining_amount = Column(Float)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
