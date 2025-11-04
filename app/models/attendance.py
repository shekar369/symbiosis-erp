from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(Time)
    check_out = Column(Time)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    hours_worked = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AttendanceUpload(Base):
    __tablename__ = "attendance_uploads"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_records = Column(Integer, default=0)
    successful_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    status = Column(String, default="pending")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
