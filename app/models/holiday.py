from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorkingCalendar(Base):
    __tablename__ = "working_calendars"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    monday = Column(Boolean, default=True)
    tuesday = Column(Boolean, default=True)
    wednesday = Column(Boolean, default=True)
    thursday = Column(Boolean, default=True)
    friday = Column(Boolean, default=True)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
