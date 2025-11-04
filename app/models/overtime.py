from sqlalchemy import Column, Integer, ForeignKey, Date, Float, String, DateTime
from datetime import datetime

from app.db.base import Base


class Overtime(Base):
    __tablename__ = "overtime"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)
    rate_multiplier = Column(Float, default=1.5)
    amount = Column(Float)
    approved_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
