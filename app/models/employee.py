from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    employee_code = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    date_of_birth = Column(Date)
    date_of_joining = Column(Date, nullable=False)
    date_of_leaving = Column(Date)
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    
    # Foreign keys
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    addresses = relationship("EmployeeAddress", back_populates="employee", cascade="all, delete-orphan")
    documents = relationship("EmployeeDocument", back_populates="employee", cascade="all, delete-orphan")
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    grade = relationship("Grade", back_populates="employees")
    tenant = relationship("Tenant", back_populates="employees")


class EmployeeAddress(Base):
    __tablename__ = "employee_addresses"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    address_type = Column(String)  # permanent, current
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

    employee = relationship("Employee", back_populates="addresses")


class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    document_type = Column(String)  # aadhar, pan, passport, etc.
    document_number = Column(String)
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="documents")
