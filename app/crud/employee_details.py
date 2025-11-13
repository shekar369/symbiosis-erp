from typing import Optional
from sqlalchemy.orm import Session

from app.models.employee import EmployeeBankDetails, EmployeeSalaryDetails, EmployeeStatutoryDetails
from app.schemas.employee import (
    EmployeeBankDetailsCreate, EmployeeBankDetailsUpdate,
    EmployeeSalaryDetailsCreate, EmployeeSalaryDetailsUpdate,
    EmployeeStatutoryDetailsCreate, EmployeeStatutoryDetailsUpdate
)


# ==================== Bank Details CRUD ====================

def get_bank_details(db: Session, employee_id: int) -> Optional[EmployeeBankDetails]:
    """Get bank details for an employee"""
    return db.query(EmployeeBankDetails).filter(
        EmployeeBankDetails.employee_id == employee_id
    ).first()


def create_bank_details(
    db: Session, 
    employee_id: int, 
    bank_details: EmployeeBankDetailsCreate
) -> EmployeeBankDetails:
    """Create bank details for an employee"""
    db_bank_details = EmployeeBankDetails(
        employee_id=employee_id,
        **bank_details.model_dump()
    )
    db.add(db_bank_details)
    db.commit()
    db.refresh(db_bank_details)
    return db_bank_details


def update_bank_details(
    db: Session,
    employee_id: int,
    bank_details: EmployeeBankDetailsUpdate
) -> Optional[EmployeeBankDetails]:
    """Update bank details for an employee"""
    db_bank_details = get_bank_details(db, employee_id)
    if db_bank_details:
        update_data = bank_details.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bank_details, field, value)
        db.commit()
        db.refresh(db_bank_details)
    return db_bank_details


def delete_bank_details(db: Session, employee_id: int) -> bool:
    """Delete bank details for an employee"""
    db_bank_details = get_bank_details(db, employee_id)
    if db_bank_details:
        db.delete(db_bank_details)
        db.commit()
        return True
    return False


# ==================== Salary Details CRUD ====================

def _calculate_salary_components(salary_obj):
    """Calculate gross salary, total deductions, net salary, and CTC"""
    # Calculate gross salary (sum of all allowances)
    gross_salary = (
        (salary_obj.basic_salary or 0) +
        (salary_obj.hra or 0) +
        (salary_obj.conveyance_allowance or 0) +
        (salary_obj.medical_allowance or 0) +
        (salary_obj.special_allowance or 0) +
        (salary_obj.other_allowance or 0)
    )
    salary_obj.gross_salary = gross_salary

    # Calculate total deductions (employee portion only)
    total_deductions = (
        (salary_obj.pf_employee or 0) +
        (salary_obj.esic_employee or 0) +
        (salary_obj.professional_tax or 0) +
        (salary_obj.tds or 0)
    )
    salary_obj.total_deductions = total_deductions

    # Calculate net salary
    salary_obj.net_salary = gross_salary - total_deductions

    # Calculate CTC (Gross + Employer contributions)
    ctc = gross_salary + (salary_obj.pf_employer or 0) + (salary_obj.esic_employer or 0)
    salary_obj.ctc = ctc


def get_salary_details(db: Session, employee_id: int) -> Optional[EmployeeSalaryDetails]:
    """Get salary details for an employee"""
    return db.query(EmployeeSalaryDetails).filter(
        EmployeeSalaryDetails.employee_id == employee_id
    ).first()


def create_salary_details(
    db: Session,
    employee_id: int,
    salary_details: EmployeeSalaryDetailsCreate
) -> EmployeeSalaryDetails:
    """Create salary details for an employee"""
    db_salary_details = EmployeeSalaryDetails(
        employee_id=employee_id,
        **salary_details.model_dump()
    )

    # Automatically calculate gross, deductions, net, and CTC
    _calculate_salary_components(db_salary_details)

    db.add(db_salary_details)
    db.commit()
    db.refresh(db_salary_details)
    return db_salary_details


def update_salary_details(
    db: Session,
    employee_id: int,
    salary_details: EmployeeSalaryDetailsUpdate
) -> Optional[EmployeeSalaryDetails]:
    """Update salary details for an employee"""
    db_salary_details = get_salary_details(db, employee_id)
    if db_salary_details:
        update_data = salary_details.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_salary_details, field, value)

        # Automatically recalculate gross, deductions, net, and CTC
        _calculate_salary_components(db_salary_details)

        db.commit()
        db.refresh(db_salary_details)
    return db_salary_details


def delete_salary_details(db: Session, employee_id: int) -> bool:
    """Delete salary details for an employee"""
    db_salary_details = get_salary_details(db, employee_id)
    if db_salary_details:
        db.delete(db_salary_details)
        db.commit()
        return True
    return False


# ==================== Statutory Details CRUD ====================

def get_statutory_details(db: Session, employee_id: int) -> Optional[EmployeeStatutoryDetails]:
    """Get statutory details for an employee"""
    return db.query(EmployeeStatutoryDetails).filter(
        EmployeeStatutoryDetails.employee_id == employee_id
    ).first()


def create_statutory_details(
    db: Session,
    employee_id: int,
    statutory_details: EmployeeStatutoryDetailsCreate
) -> EmployeeStatutoryDetails:
    """Create statutory details for an employee"""
    db_statutory_details = EmployeeStatutoryDetails(
        employee_id=employee_id,
        **statutory_details.model_dump()
    )
    db.add(db_statutory_details)
    db.commit()
    db.refresh(db_statutory_details)
    return db_statutory_details


def update_statutory_details(
    db: Session,
    employee_id: int,
    statutory_details: EmployeeStatutoryDetailsUpdate
) -> Optional[EmployeeStatutoryDetails]:
    """Update statutory details for an employee"""
    db_statutory_details = get_statutory_details(db, employee_id)
    if db_statutory_details:
        update_data = statutory_details.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_statutory_details, field, value)
        db.commit()
        db.refresh(db_statutory_details)
    return db_statutory_details


def delete_statutory_details(db: Session, employee_id: int) -> bool:
    """Delete statutory details for an employee"""
    db_statutory_details = get_statutory_details(db, employee_id)
    if db_statutory_details:
        db.delete(db_statutory_details)
        db.commit()
        return True
    return False
