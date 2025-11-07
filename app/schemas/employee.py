from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


# ==================== Salary Details Schemas ====================

class EmployeeSalaryDetailsBase(BaseModel):
    basic_salary: Decimal = 0
    hra: Optional[Decimal] = 0
    conveyance_allowance: Optional[Decimal] = 0
    medical_allowance: Optional[Decimal] = 0
    special_allowance: Optional[Decimal] = 0
    other_allowance: Optional[Decimal] = 0
    gross_salary: Optional[Decimal] = 0
    pf_employee: Optional[Decimal] = 0
    pf_employer: Optional[Decimal] = 0
    esic_employee: Optional[Decimal] = 0
    esic_employer: Optional[Decimal] = 0
    professional_tax: Optional[Decimal] = 0
    tds: Optional[Decimal] = 0
    total_deductions: Optional[Decimal] = 0
    net_salary: Optional[Decimal] = 0
    ctc: Optional[Decimal] = 0


class EmployeeSalaryDetailsCreate(EmployeeSalaryDetailsBase):
    employee_id: int


class EmployeeSalaryDetailsUpdate(BaseModel):
    basic_salary: Optional[Decimal] = None
    hra: Optional[Decimal] = None
    conveyance_allowance: Optional[Decimal] = None
    medical_allowance: Optional[Decimal] = None
    special_allowance: Optional[Decimal] = None
    other_allowance: Optional[Decimal] = None
    gross_salary: Optional[Decimal] = None
    pf_employee: Optional[Decimal] = None
    pf_employer: Optional[Decimal] = None
    esic_employee: Optional[Decimal] = None
    esic_employer: Optional[Decimal] = None
    professional_tax: Optional[Decimal] = None
    tds: Optional[Decimal] = None
    total_deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    ctc: Optional[Decimal] = None


class EmployeeSalaryDetailsResponse(EmployeeSalaryDetailsBase):
    id: int
    employee_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Statutory Details Schemas ====================

class EmployeeStatutoryDetailsBase(BaseModel):
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    uan_number: Optional[str] = None
    esic_number: Optional[str] = None
    pf_applicable: Optional[bool] = True
    esic_applicable: Optional[bool] = True
    lwf_applicable: Optional[bool] = False
    pt_applicable: Optional[bool] = True
    previous_employer_pf_number: Optional[str] = None
    date_of_exit_from_previous_pf: Optional[date] = None


class EmployeeStatutoryDetailsCreate(EmployeeStatutoryDetailsBase):
    employee_id: int


class EmployeeStatutoryDetailsUpdate(BaseModel):
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    uan_number: Optional[str] = None
    esic_number: Optional[str] = None
    pf_applicable: Optional[bool] = None
    esic_applicable: Optional[bool] = None
    lwf_applicable: Optional[bool] = None
    pt_applicable: Optional[bool] = None
    previous_employer_pf_number: Optional[str] = None
    date_of_exit_from_previous_pf: Optional[date] = None


class EmployeeStatutoryDetailsResponse(EmployeeStatutoryDetailsBase):
    id: int
    employee_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Employee Schemas ====================

class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None

    # Basic Information
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    father_husband_name: Optional[str] = None
    blood_group: Optional[str] = None

    # Emergency Contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    emergency_contact_relation: Optional[str] = None

    # Employment Details
    date_of_joining: date
    date_of_leaving: Optional[date] = None
    employment_type: Optional[str] = "permanent"
    probation_period_months: Optional[int] = None
    confirmation_date: Optional[date] = None
    notice_period_days: Optional[int] = None

    # Organizational Hierarchy
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    grade_id: Optional[int] = None
    reporting_manager_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    tenant_id: Optional[int] = None  # Auto-assigned from authenticated user if not provided


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    father_husband_name: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    employment_type: Optional[str] = None
    probation_period_months: Optional[int] = None
    confirmation_date: Optional[date] = None
    notice_period_days: Optional[int] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    grade_id: Optional[int] = None
    reporting_manager_id: Optional[int] = None
    status: Optional[str] = None


class EmployeeProfileUpdate(BaseModel):
    """Schema for employee self-service profile updates - limited fields"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    emergency_contact_relation: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    tenant_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    # Related data (optional, loaded when needed)
    salary_details: Optional[EmployeeSalaryDetailsResponse] = None
    statutory_details: Optional[EmployeeStatutoryDetailsResponse] = None

    class Config:
        from_attributes = True

