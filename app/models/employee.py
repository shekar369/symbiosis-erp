from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime, Enum, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class EmploymentType(str, enum.Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    employee_code = Column(String, unique=True, nullable=False, index=True)

    # Basic Information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)  # Database uses VARCHAR, not enum constraint
    marital_status = Column(String)  # Database uses VARCHAR, not enum constraint
    father_husband_name = Column(String)
    blood_group = Column(String)

    # Contact Information
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    alternate_phone = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_number = Column(String)
    emergency_contact_relation = Column(String)

    # Employment Details
    date_of_joining = Column(Date, nullable=False)
    date_of_leaving = Column(Date)
    employment_type = Column(String)  # Database uses VARCHAR, not enum constraint
    probation_period_months = Column(Integer)
    confirmation_date = Column(Date)
    notice_period_days = Column(Integer)
    status = Column(String)  # Database uses VARCHAR, not enum constraint

    # Foreign keys
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=True)
    reporting_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    addresses = relationship("EmployeeAddress", back_populates="employee", cascade="all, delete-orphan")
    documents = relationship("EmployeeDocument", back_populates="employee", cascade="all, delete-orphan")
    bank_details = relationship("EmployeeBankDetails", back_populates="employee", cascade="all, delete-orphan", uselist=False)
    salary_details = relationship("EmployeeSalaryDetails", back_populates="employee", cascade="all, delete-orphan", uselist=False)
    statutory_details = relationship("EmployeeStatutoryDetails", back_populates="employee", cascade="all, delete-orphan", uselist=False)
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    grade = relationship("Grade", back_populates="employees")
    tenant = relationship("Tenant", back_populates="employees")
    reporting_manager = relationship("Employee", remote_side=[id], backref="subordinates")


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


class EmployeeBankDetails(Base):
    __tablename__ = "employee_bank_details"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)
    account_holder_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    branch_name = Column(String)
    ifsc_code = Column(String, nullable=False)
    account_type = Column(String)  # savings, current
    pan_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = relationship("Employee", back_populates="bank_details")


class EmployeeSalaryDetails(Base):
    __tablename__ = "employee_salary_details"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)

    # Salary Components
    basic_salary = Column(Numeric(10, 2), nullable=False, default=0)
    hra = Column(Numeric(10, 2), default=0)
    conveyance_allowance = Column(Numeric(10, 2), default=0)
    medical_allowance = Column(Numeric(10, 2), default=0)
    special_allowance = Column(Numeric(10, 2), default=0)
    other_allowance = Column(Numeric(10, 2), default=0)

    # Calculated Fields
    gross_salary = Column(Numeric(10, 2), default=0)

    # Deductions
    pf_employee = Column(Numeric(10, 2), default=0)
    pf_employer = Column(Numeric(10, 2), default=0)
    esic_employee = Column(Numeric(10, 2), default=0)
    esic_employer = Column(Numeric(10, 2), default=0)
    professional_tax = Column(Numeric(10, 2), default=0)
    tds = Column(Numeric(10, 2), default=0)

    # Final Amounts
    total_deductions = Column(Numeric(10, 2), default=0)
    net_salary = Column(Numeric(10, 2), default=0)
    ctc = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = relationship("Employee", back_populates="salary_details")


class EmployeeStatutoryDetails(Base):
    __tablename__ = "employee_statutory_details"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True)

    # Statutory Numbers
    pan_number = Column(String)
    aadhaar_number = Column(String)
    uan_number = Column(String)  # Universal Account Number for PF
    esic_number = Column(String)

    # Applicability Flags
    pf_applicable = Column(Boolean, default=True)
    esic_applicable = Column(Boolean, default=True)
    lwf_applicable = Column(Boolean, default=False)  # Labour Welfare Fund
    pt_applicable = Column(Boolean, default=True)  # Professional Tax

    # Additional Info
    previous_employer_pf_number = Column(String)
    date_of_exit_from_previous_pf = Column(Date)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = relationship("Employee", back_populates="statutory_details")
