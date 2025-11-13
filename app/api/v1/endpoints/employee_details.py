from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.crud import employee_details as crud
from app.schemas.employee import (
    EmployeeBankDetailsCreate, EmployeeBankDetailsUpdate, EmployeeBankDetailsResponse,
    EmployeeSalaryDetailsCreate, EmployeeSalaryDetailsUpdate, EmployeeSalaryDetailsResponse,
    EmployeeStatutoryDetailsCreate, EmployeeStatutoryDetailsUpdate, EmployeeStatutoryDetailsResponse
)
from app.models.user import User
from app.models.employee import Employee

router = APIRouter()


# ==================== Bank Details Endpoints ====================

@router.get("/{employee_id}/bank-details", response_model=EmployeeBankDetailsResponse)
async def get_employee_bank_details(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get bank details for an employee"""
    # Verify employee exists and belongs to current user's tenant
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    bank_details = crud.get_bank_details(db, employee_id)
    if not bank_details:
        raise HTTPException(status_code=404, detail="Bank details not found")

    return bank_details


@router.post("/{employee_id}/bank-details", response_model=EmployeeBankDetailsResponse)
async def create_employee_bank_details(
    employee_id: int,
    bank_details: EmployeeBankDetailsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create bank details for an employee"""
    # Verify employee exists and belongs to current user's tenant
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if bank details already exist
    existing = crud.get_bank_details(db, employee_id)
    if existing:
        raise HTTPException(status_code=400, detail="Bank details already exist for this employee")

    return crud.create_bank_details(db, employee_id, bank_details)


@router.put("/{employee_id}/bank-details", response_model=EmployeeBankDetailsResponse)
async def update_employee_bank_details(
    employee_id: int,
    bank_details: EmployeeBankDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update bank details for an employee"""
    # Verify employee exists and belongs to current user's tenant
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated = crud.update_bank_details(db, employee_id, bank_details)
    if not updated:
        raise HTTPException(status_code=404, detail="Bank details not found")

    return updated


# ==================== Salary Details Endpoints ====================

@router.get("/{employee_id}/salary-details", response_model=EmployeeSalaryDetailsResponse)
async def get_employee_salary_details(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get salary details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    salary_details = crud.get_salary_details(db, employee_id)
    if not salary_details:
        raise HTTPException(status_code=404, detail="Salary details not found")

    return salary_details


@router.post("/{employee_id}/salary-details", response_model=EmployeeSalaryDetailsResponse)
async def create_employee_salary_details(
    employee_id: int,
    salary_details: EmployeeSalaryDetailsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create salary details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = crud.get_salary_details(db, employee_id)
    if existing:
        raise HTTPException(status_code=400, detail="Salary details already exist for this employee")

    return crud.create_salary_details(db, employee_id, salary_details)


@router.put("/{employee_id}/salary-details", response_model=EmployeeSalaryDetailsResponse)
async def update_employee_salary_details(
    employee_id: int,
    salary_details: EmployeeSalaryDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update salary details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated = crud.update_salary_details(db, employee_id, salary_details)
    if not updated:
        raise HTTPException(status_code=404, detail="Salary details not found")

    return updated


# ==================== Statutory Details Endpoints ====================

@router.get("/{employee_id}/statutory-details", response_model=EmployeeStatutoryDetailsResponse)
async def get_employee_statutory_details(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get statutory details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    statutory_details = crud.get_statutory_details(db, employee_id)
    if not statutory_details:
        raise HTTPException(status_code=404, detail="Statutory details not found")

    return statutory_details


@router.post("/{employee_id}/statutory-details", response_model=EmployeeStatutoryDetailsResponse)
async def create_employee_statutory_details(
    employee_id: int,
    statutory_details: EmployeeStatutoryDetailsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create statutory details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = crud.get_statutory_details(db, employee_id)
    if existing:
        raise HTTPException(status_code=400, detail="Statutory details already exist for this employee")

    return crud.create_statutory_details(db, employee_id, statutory_details)


@router.put("/{employee_id}/statutory-details", response_model=EmployeeStatutoryDetailsResponse)
async def update_employee_statutory_details(
    employee_id: int,
    statutory_details: EmployeeStatutoryDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update statutory details for an employee"""
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated = crud.update_statutory_details(db, employee_id, statutory_details)
    if not updated:
        raise HTTPException(status_code=404, detail="Statutory details not found")

    return updated
