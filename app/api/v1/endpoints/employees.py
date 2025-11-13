from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeProfileUpdate
from app.crud.employee import employee as employee_crud
from app.models.user import User
from app.models.employee import Employee
from app.services.employee_template_service import EmployeeTemplateService

router = APIRouter()


@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Auto-assign tenant_id from current user to ensure data isolation
    # Create employee directly to preserve date types
    db_employee = Employee(
        tenant_id=current_user.tenant_id,
        employee_code=employee.employee_code,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone,
        date_of_birth=employee.date_of_birth,
        date_of_joining=employee.date_of_joining,
        department_id=employee.department_id,
        designation_id=employee.designation_id,
        grade_id=employee.grade_id,
        status="active"
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/me", response_model=EmployeeResponse)
async def get_current_employee(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the employee record for the currently logged-in user"""
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

    return employee


@router.put("/me/profile", response_model=EmployeeResponse)
async def update_my_profile(
    profile_update: EmployeeProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update profile for the currently logged-in employee (self-service)"""
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

    # Update only the allowed fields
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.get("/", response_model=List[EmployeeResponse])
async def list_employees(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return employee_crud.get_employees(db=db, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    employee = employee_crud.get_employee(db=db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    employee = employee_crud.update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    success = employee_crud.delete_employee(db=db, employee_id=employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


@router.get("/template/info")
async def get_template_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get information about the employee template"""
    template_service = EmployeeTemplateService(db=db, tenant_id=current_user.tenant_id)
    template_info = template_service.get_template_info()
    return template_info


@router.get("/template/download")
async def download_template(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download employee template Excel file"""
    try:
        template_service = EmployeeTemplateService(db=db, tenant_id=current_user.tenant_id)

        # Get tenant's company name if available
        company_name = getattr(current_user.tenant, 'name', 'Company Name') if hasattr(current_user, 'tenant') else 'Company Name'

        file_path = template_service.generate_template(company_name=company_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to generate template file")

        filename = os.path.basename(file_path)

        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")
