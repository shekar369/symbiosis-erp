from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.employee import Employee
from app.schemas.bank import BankDetailsCreate, BankDetailsUpdate, BankDetailsResponse
from app.crud.bank import bank_details as bank_crud

router = APIRouter()


@router.get("/my-bank-details", response_model=BankDetailsResponse)
async def get_my_bank_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get bank details for the currently logged-in employee"""
    # Find employee by email matching the user's email
    employee = db.query(Employee).filter(
        Employee.email == current_user.email,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found for current user"
        )

    bank_details = bank_crud.get_by_employee(db=db, employee_id=employee.id)
    if not bank_details:
        raise HTTPException(status_code=404, detail="Bank details not found")

    return bank_details


@router.post("/my-bank-details", response_model=BankDetailsResponse)
async def create_my_bank_details(
    bank_data: BankDetailsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create bank details for the currently logged-in employee"""
    # Find employee by email matching the user's email
    employee = db.query(Employee).filter(
        Employee.email == current_user.email,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found for current user"
        )

    # Check if bank details already exist
    existing_bank_details = bank_crud.get_by_employee(db=db, employee_id=employee.id)
    if existing_bank_details:
        raise HTTPException(
            status_code=400,
            detail="Bank details already exist. Use PUT to update."
        )

    # Override employee_id with the current employee's ID
    bank_data.employee_id = employee.id

    return bank_crud.create(db=db, bank_details=bank_data)


@router.put("/my-bank-details", response_model=BankDetailsResponse)
async def update_my_bank_details(
    bank_update: BankDetailsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update or create bank details for the currently logged-in employee (upsert)"""
    # Find employee by email matching the user's email
    employee = db.query(Employee).filter(
        Employee.email == current_user.email,
        Employee.tenant_id == current_user.tenant_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found for current user"
        )

    # Try to update existing bank details
    updated_bank_details = bank_crud.update(
        db=db,
        employee_id=employee.id,
        bank_update=bank_update
    )

    # If bank details don't exist, create them
    if not updated_bank_details:
        update_dict = bank_update.model_dump(exclude_unset=True)

        # Create requires all mandatory fields, ensure they're provided
        if not all(k in update_dict for k in ['account_holder_name', 'account_number', 'bank_name', 'ifsc_code']):
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: account_holder_name, account_number, bank_name, ifsc_code"
            )

        bank_data = BankDetailsCreate(
            employee_id=employee.id,
            **update_dict
        )
        return bank_crud.create(db=db, bank_details=bank_data)

    return updated_bank_details


@router.get("/{employee_id}/bank-details", response_model=BankDetailsResponse)
async def get_employee_bank_details(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get bank details for a specific employee (admin/employer access)"""
    bank_details = bank_crud.get_by_employee(db=db, employee_id=employee_id)
    if not bank_details:
        raise HTTPException(status_code=404, detail="Bank details not found")

    return bank_details
