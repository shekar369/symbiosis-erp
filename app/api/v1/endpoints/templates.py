from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.employee import Employee
from app.utils.excel_templates import ExcelTemplateGenerator

router = APIRouter()


@router.get("/employee-database")
def download_employee_database_template(
    act_type: str = Query("contract_labour", description="Act type: contract_labour, shops_establishment, factories"),
    location: Optional[str] = Query(None, description="Location name"),
    current_user: User = Depends(get_current_active_user),
):
    """Download employee database template"""

    template = ExcelTemplateGenerator.create_employee_database_template(
        act_type=act_type,
        location=location
    )

    filename = f"Employee_Database_Template_{act_type}"
    if location:
        filename += f"_{location.replace(' ', '_')}"
    filename += f"_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return StreamingResponse(
        template,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/attendance")
def download_attendance_template(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2020, le=2030, description="Year"),
    location_id: Optional[int] = Query(None, description="Location ID to filter employees"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Download attendance template for a specific month with employee list"""

    # Get employees for the tenant
    query = db.query(Employee).filter(
        Employee.tenant_id == current_user.tenant_id,
        Employee.status == "active"
    )

    if location_id:
        # TODO: Filter by location when employee-location assignment is implemented
        pass

    employees = query.all()
    employee_data = [
        {
            "employee_code": emp.employee_code,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
        }
        for emp in employees
    ]

    template = ExcelTemplateGenerator.create_attendance_template(
        month=month,
        year=year,
        employees=employee_data
    )

    filename = f"Attendance_Template_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return StreamingResponse(
        template,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/salary-statement")
def download_salary_statement_template(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2020, le=2030, description="Year"),
    act_type: str = Query("contract_labour", description="Act type"),
    current_user: User = Depends(get_current_active_user),
):
    """Download salary/wage statement template"""

    template = ExcelTemplateGenerator.create_salary_statement_template(
        month=month,
        year=year,
        act_type=act_type
    )

    filename = f"Salary_Statement_Template_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return StreamingResponse(
        template,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/leave-register")
def download_leave_register_template(
    current_user: User = Depends(get_current_active_user),
):
    """Download leave register template"""

    template = ExcelTemplateGenerator.create_leave_register_template()

    filename = f"Leave_Register_Template_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return StreamingResponse(
        template,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
