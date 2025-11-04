from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.wage import WageStatement
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.utils.statutory_forms_generator import StatutoryFormsGenerator

router = APIRouter()


@router.get("/epf-ecr")
def download_epf_ecr(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download EPF-ECR CSV file"""
    # Get approved wage statements
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
            WageStatement.status.in_(["approved", "paid"])
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved wage statements found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        if statement.pf_employee > 0:  # Only PF applicable employees
            wage_statements.append({
                "uan": employee.uan if hasattr(employee, 'uan') else "",
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "employee_code": employee.employee_code,
                "gross_salary": statement.gross_salary,
                "basic_salary": statement.basic_salary,
                "pf_employee": statement.pf_employee,
                "pf_employer": statement.pf_employer,
                "days_absent": statement.days_absent
            })

    establishment_details = {
        "name": tenant.name if tenant else "Company Name",
        "epf_code": tenant.epf_code if tenant and hasattr(tenant, 'epf_code') else "N/A",
        "epf_registration": tenant.epf_registration if tenant and hasattr(tenant, 'epf_registration') else "N/A"
    }

    # Generate EPF-ECR file
    file_buffer = StatutoryFormsGenerator.generate_epf_ecr(
        wage_statements=wage_statements,
        month=month,
        year=year,
        establishment_details=establishment_details
    )

    filename = f"EPF_ECR_{month:02d}_{year}.csv"

    return StreamingResponse(
        iter([file_buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/esi-return")
def download_esi_return(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download ESI monthly return CSV"""
    # Get approved wage statements
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
            WageStatement.status.in_(["approved", "paid"])
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved wage statements found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        if statement.esi_employee > 0:  # Only ESI applicable employees
            wage_statements.append({
                "esic_ip_number": employee.esic_ip_number if hasattr(employee, 'esic_ip_number') else "",
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "days_worked": statement.days_worked,
                "gross_salary": statement.gross_salary,
                "esi_employee": statement.esi_employee,
                "esi_employer": statement.esi_employer
            })

    establishment_details = {
        "name": tenant.name if tenant else "Company Name",
        "esic_code": tenant.esic_code if tenant and hasattr(tenant, 'esic_code') else "N/A"
    }

    # Generate ESI return file
    file_buffer = StatutoryFormsGenerator.generate_esi_return(
        wage_statements=wage_statements,
        month=month,
        year=year,
        establishment_details=establishment_details
    )

    filename = f"ESI_Return_{month:02d}_{year}.csv"

    return StreamingResponse(
        iter([file_buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/pt-form-v")
def download_pt_form_v(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    state: str = Query("Maharashtra"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download Professional Tax Form V PDF"""
    # Get approved wage statements
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
            WageStatement.status.in_(["approved", "paid"])
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved wage statements found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        if statement.professional_tax > 0:
            wage_statements.append({
                "employee_name": f"{employee.first_name} {employee.last_name}",
                "employee_code": employee.employee_code,
                "gross_salary": statement.gross_salary,
                "professional_tax": statement.professional_tax
            })

    establishment_details = {
        "name": tenant.name if tenant else "Company Name",
        "pt_registration": tenant.pt_registration if tenant and hasattr(tenant, 'pt_registration') else "N/A"
    }

    # Generate PT Form V
    pdf_buffer = StatutoryFormsGenerator.generate_pt_form_v(
        wage_statements=wage_statements,
        month=month,
        year=year,
        state=state,
        establishment_details=establishment_details
    )

    filename = f"PT_Form_V_{month:02d}_{year}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/form-xiii")
def download_form_xiii(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download Form-XIII (Workmen Register) PDF"""
    # Get approved wage statements
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
            WageStatement.status.in_(["approved", "paid"])
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved wage statements found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        wage_statements.append({
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "father_name": employee.father_name if hasattr(employee, 'father_name') else "N/A",
            "age": employee.age if hasattr(employee, 'age') else "N/A",
            "designation": employee.designation,
            "net_salary": statement.net_salary,
            "days_worked": statement.days_worked
        })

    establishment_details = {
        "name": tenant.name if tenant else "Company Name",
        "contract_labour_reg": tenant.contract_labour_reg if tenant and hasattr(tenant, 'contract_labour_reg') else "N/A"
    }

    # Generate Form-XIII
    pdf_buffer = StatutoryFormsGenerator.generate_form_xiii(
        wage_statements=wage_statements,
        month=month,
        year=year,
        establishment_details=establishment_details
    )

    filename = f"Form_XIII_{month:02d}_{year}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/pf-challan-summary")
def download_pf_challan_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download PF challan summary PDF"""
    # Get approved wage statements
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
            WageStatement.status.in_(["approved", "paid"])
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved wage statements found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        if statement.pf_employee > 0:
            wage_statements.append({
                "basic_salary": statement.basic_salary,
                "pf_employee": statement.pf_employee,
                "pf_employer": statement.pf_employer
            })

    establishment_details = {
        "name": tenant.name if tenant else "Company Name",
        "epf_code": tenant.epf_code if tenant and hasattr(tenant, 'epf_code') else "N/A",
        "epf_registration": tenant.epf_registration if tenant and hasattr(tenant, 'epf_registration') else "N/A"
    }

    # Generate PF challan summary
    pdf_buffer = StatutoryFormsGenerator.generate_monthly_pf_challan_summary(
        wage_statements=wage_statements,
        month=month,
        year=year,
        establishment_details=establishment_details
    )

    filename = f"PF_Challan_Summary_{month:02d}_{year}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
