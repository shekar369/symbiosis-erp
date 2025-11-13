from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from typing import List, Optional
from pydantic import BaseModel

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.wage import WageStatement
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.services.wage_calculation_service import WageCalculationService
from app.services.email_service import EmailService
from app.utils.pdf_generator import PDFGenerator
from app.utils.bank_transfer_generator import BankTransferGenerator

router = APIRouter()


# Request/Response Models
class CalculateWageRequest(BaseModel):
    employee_id: int
    month: int
    year: int


class BulkPayrollRequest(BaseModel):
    month: int
    year: int
    location_id: Optional[int] = None


class ApprovePayrollRequest(BaseModel):
    wage_statement_ids: List[int]


class WageStatementResponse(BaseModel):
    id: int
    employee_id: int
    month: int
    year: int
    total_days: int
    present_days: int
    absent_days: int
    leave_days: int
    basic_salary: float
    total_earnings: float
    total_deductions: float
    net_salary: float
    status: str

    class Config:
        from_attributes = True


@router.post("/calculate", response_model=dict)
def calculate_employee_wage(
    request: CalculateWageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calculate wage for a single employee"""
    try:
        service = WageCalculationService(db)
        wage_data = service.calculate_monthly_wage(
            employee_id=request.employee_id,
            month=request.month,
            year=request.year,
            create_statement=True
        )

        return {
            "success": True,
            "message": "Wage calculated successfully",
            "data": wage_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating wage: {str(e)}"
        )


@router.post("/process-bulk", response_model=dict)
def process_bulk_payroll(
    request: BulkPayrollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Process payroll for all active employees in tenant"""
    try:
        service = WageCalculationService(db)
        result = service.process_bulk_payroll(
            tenant_id=current_user.tenant_id,
            month=request.month,
            year=request.year
        )

        return {
            "success": True,
            "message": f"Bulk payroll processing complete. {result['successful']} successful, {result['failed']} failed.",
            "summary": {
                "total_employees": result['total_employees'],
                "successful": result['successful'],
                "failed": result['failed']
            },
            "successful_records": result['successful_records'],
            "failed_records": result['failed_records']
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing bulk payroll: {str(e)}"
        )


@router.get("/wage-statements", response_model=List[WageStatementResponse])
def get_wage_statements(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020, le=2030),
    employee_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get wage statements with filters"""
    query = db.query(WageStatement).join(Employee).filter(
        Employee.tenant_id == current_user.tenant_id
    )

    if month:
        query = query.filter(WageStatement.month == month)
    if year:
        query = query.filter(WageStatement.year == year)
    if employee_id:
        query = query.filter(WageStatement.employee_id == employee_id)
    if status:
        query = query.filter(WageStatement.status == status)

    statements = query.offset(skip).limit(limit).all()
    return statements


@router.get("/wage-statement/{employee_id}")
def get_employee_wage_statement(
    employee_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed wage statement for an employee"""
    statement = db.query(WageStatement).filter(
        and_(
            WageStatement.employee_id == employee_id,
            WageStatement.month == month,
            WageStatement.year == year
        )
    ).first()

    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wage statement not found"
        )

    # Verify tenant access
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or employee.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Get earnings and deductions from JSON breakdown
    earnings_breakdown = statement.earnings_breakdown or {}
    deductions_breakdown = statement.deductions_breakdown or {}

    # Get designation and department names
    designation_name = employee.designation.name if employee.designation else None
    department_name = employee.department.name if employee.department else None

    return {
        "id": statement.id,
        "employee_id": statement.employee_id,
        "employee": {
            "code": employee.employee_code,
            "name": f"{employee.first_name} {employee.last_name}",
            "email": employee.email,
            "designation": designation_name,
            "department": department_name
        },
        "period": {
            "month": statement.month,
            "year": statement.year
        },
        "attendance": {
            "total_days": statement.total_days,
            "present_days": statement.present_days,
            "absent_days": statement.absent_days,
            "leave_days": statement.leave_days
        },
        "earnings": {
            "basic_salary": statement.basic_salary,
            "total_earnings": statement.total_earnings,
            "breakdown": earnings_breakdown
        },
        "deductions": {
            "total_deductions": statement.total_deductions,
            "breakdown": deductions_breakdown
        },
        "net_salary": statement.net_salary,
        "status": statement.status,
        "calculated_at": statement.calculated_at.isoformat() if statement.calculated_at else None,
        "approved_at": statement.approved_at.isoformat() if statement.approved_at else None,
        "paid_at": statement.paid_at.isoformat() if statement.paid_at else None
    }


@router.post("/approve")
def approve_wage_statements(
    request: ApprovePayrollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Approve multiple wage statements"""
    approved_count = 0
    failed_count = 0
    errors = []

    for statement_id in request.wage_statement_ids:
        try:
            statement = db.query(WageStatement).filter(
                WageStatement.id == statement_id
            ).first()

            if not statement:
                errors.append(f"Statement {statement_id} not found")
                failed_count += 1
                continue

            # Verify tenant access
            employee = db.query(Employee).filter(
                Employee.id == statement.employee_id
            ).first()

            if not employee or employee.tenant_id != current_user.tenant_id:
                errors.append(f"Statement {statement_id} - Access denied")
                failed_count += 1
                continue

            # Update status
            statement.status = "approved"
            approved_count += 1

        except Exception as e:
            errors.append(f"Statement {statement_id} - {str(e)}")
            failed_count += 1

    db.commit()

    return {
        "success": True,
        "message": f"Approved {approved_count} statements, {failed_count} failed",
        "summary": {
            "approved": approved_count,
            "failed": failed_count
        },
        "errors": errors
    }


@router.post("/mark-paid")
def mark_statements_as_paid(
    request: ApprovePayrollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark wage statements as paid"""
    paid_count = 0
    failed_count = 0
    errors = []

    for statement_id in request.wage_statement_ids:
        try:
            statement = db.query(WageStatement).filter(
                WageStatement.id == statement_id
            ).first()

            if not statement:
                errors.append(f"Statement {statement_id} not found")
                failed_count += 1
                continue

            # Verify tenant access and approval status
            employee = db.query(Employee).filter(
                Employee.id == statement.employee_id
            ).first()

            if not employee or employee.tenant_id != current_user.tenant_id:
                errors.append(f"Statement {statement_id} - Access denied")
                failed_count += 1
                continue

            if statement.status != "approved":
                errors.append(f"Statement {statement_id} - Not approved")
                failed_count += 1
                continue

            # Update status
            statement.status = "paid"
            paid_count += 1

        except Exception as e:
            errors.append(f"Statement {statement_id} - {str(e)}")
            failed_count += 1

    db.commit()

    return {
        "success": True,
        "message": f"Marked {paid_count} statements as paid, {failed_count} failed",
        "summary": {
            "paid": paid_count,
            "failed": failed_count
        },
        "errors": errors
    }


@router.get("/summary")
def get_payroll_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get payroll summary for a month"""
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year
        )
    ).all()

    total_employees = len(statements)
    total_gross = sum(s.total_earnings for s in statements)
    total_deductions = sum(s.total_deductions for s in statements)
    total_net = sum(s.net_salary for s in statements)

    # Count by status
    status_counts = {}
    for statement in statements:
        status = statement.status
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "period": {"month": month, "year": year},
        "summary": {
            "total_employees": total_employees,
            "total_gross_salary": round(total_gross, 2),
            "total_deductions": round(total_deductions, 2),
            "total_net_salary": round(total_net, 2)
        },
        "status_breakdown": status_counts
    }


@router.get("/payslip/{employee_id}")
def download_payslip(
    employee_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download PDF payslip for an employee"""
    # Get wage statement
    statement = db.query(WageStatement).filter(
        and_(
            WageStatement.employee_id == employee_id,
            WageStatement.month == month,
            WageStatement.year == year
        )
    ).first()

    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wage statement not found"
        )

    # Get employee details
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or employee.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data for PDF
    wage_data = {
        "employee_id": statement.employee_id,
        "month": statement.month,
        "year": statement.year,
        "total_days": statement.total_days,
        "present_days": statement.present_days,
        "absent_days": statement.absent_days,
        "leave_days": statement.leave_days,
        "basic_salary": statement.basic_salary,
        "total_earnings": statement.total_earnings,
        "total_deductions": statement.total_deductions,
        "net_salary": statement.net_salary,
        "earnings_breakdown": statement.earnings_breakdown or {},
        "deductions_breakdown": statement.deductions_breakdown or {}
    }

    # Get related data
    designation_name = employee.designation.name if employee.designation else "N/A"
    department_name = employee.department.name if employee.department else "N/A"

    # Get bank and statutory details
    bank_account = "N/A"
    pan_number = "N/A"
    pf_number = "N/A"

    if employee.bank_details:
        bank_account = employee.bank_details.account_number
        if employee.bank_details.pan_number:
            pan_number = employee.bank_details.pan_number

    if employee.statutory_details:
        if employee.statutory_details.pan_number:
            pan_number = employee.statutory_details.pan_number
        if employee.statutory_details.uan_number:
            pf_number = employee.statutory_details.uan_number

    employee_data = {
        "employee_code": employee.employee_code,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "designation": designation_name,
        "department": department_name,
        "date_of_joining": str(employee.date_of_joining) if employee.date_of_joining else "N/A",
        "bank_account": bank_account,
        "pan": pan_number,
        "pf_number": pf_number
    }

    tenant_data = {
        "name": tenant.name if tenant else "Company Name",
        "address": tenant.address if tenant and hasattr(tenant, 'address') else "Company Address"
    }

    # Generate PDF
    pdf_buffer = PDFGenerator.generate_payslip(
        wage_statement=wage_data,
        employee_details=employee_data,
        tenant_details=tenant_data
    )

    # Return as downloadable file
    filename = f"payslip_{employee.employee_code}_{month:02d}_{year}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/salary-register")
def download_salary_register(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download consolidated salary register PDF"""
    # Get all wage statements for the month
    statements = db.query(WageStatement).join(Employee).filter(
        and_(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year
        )
    ).all()

    if not statements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No wage statements found for this period"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        wage_statements.append({
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "present_days": statement.present_days,
            "total_earnings": statement.total_earnings,
            "net_salary": statement.net_salary,
            "deductions_breakdown": statement.deductions_breakdown or {}
        })

    tenant_data = {
        "name": tenant.name if tenant else "Company Name",
        "address": tenant.address if tenant and hasattr(tenant, 'address') else "Company Address"
    }

    # Generate PDF
    pdf_buffer = PDFGenerator.generate_salary_register(
        wage_statements=wage_statements,
        month=month,
        year=year,
        tenant_details=tenant_data
    )

    # Return as downloadable file
    filename = f"salary_register_{month:02d}_{year}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/bank-transfer-file")
def download_bank_transfer_file(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    format: str = Query("csv", regex="^(csv|neft|hdfc|icici|sbi)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Download bank transfer file for salary payments

    Supported formats:
    - csv: Standard CSV format
    - neft: NEFT text format for bank upload
    - hdfc: HDFC Bank specific CSV
    - icici: ICICI Bank specific CSV
    - sbi: SBI Bank specific CSV
    """
    # Get approved wage statements only
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
            detail="No approved wage statements found for this period"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        wage_statements.append({
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "bank_account": employee.bank_account if hasattr(employee, 'bank_account') else "",
            "ifsc_code": employee.ifsc_code if hasattr(employee, 'ifsc_code') else "",
            "bank_name": employee.bank_name if hasattr(employee, 'bank_name') else "N/A",
            "branch": employee.branch if hasattr(employee, 'branch') else "N/A",
            "net_salary": statement.net_salary,
            "month": statement.month,
            "year": statement.year
        })

    company_details = {
        "name": tenant.name if tenant else "Company Name",
        "company_code": tenant.company_code if tenant and hasattr(tenant, 'company_code') else "0000"
    }

    # Generate file based on format
    if format == "neft":
        file_buffer = BankTransferGenerator.generate_neft_file(
            wage_statements=wage_statements,
            company_details=company_details,
            month=month,
            year=year
        )
        media_type = "text/plain"
        extension = "txt"
    else:
        # CSV formats
        format_type = format if format in ["hdfc", "icici", "sbi"] else "standard"
        file_buffer = BankTransferGenerator.generate_csv_file(
            wage_statements=wage_statements,
            month=month,
            year=year,
            format_type=format_type
        )
        media_type = "text/csv"
        extension = "csv"

    # Return as downloadable file
    filename = f"salary_transfer_{format}_{month:02d}_{year}.{extension}"

    return StreamingResponse(
        iter([file_buffer.getvalue()]),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/payment-summary")
def download_payment_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download payment summary text file"""
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
            detail="No approved wage statements found for this period"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data
    wage_statements = []
    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()
        wage_statements.append({
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "bank_name": employee.bank_name if hasattr(employee, 'bank_name') else "N/A",
            "net_salary": statement.net_salary
        })

    company_details = {
        "name": tenant.name if tenant else "Company Name"
    }

    # Generate summary
    summary_buffer = BankTransferGenerator.generate_payment_summary(
        wage_statements=wage_statements,
        month=month,
        year=year,
        company_details=company_details
    )

    # Return as downloadable file
    filename = f"payment_summary_{month:02d}_{year}.txt"

    return StreamingResponse(
        iter([summary_buffer.getvalue()]),
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/send-payslip-email/{employee_id}")
def send_payslip_email(
    employee_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Send payslip via email to employee"""
    # Get wage statement
    statement = db.query(WageStatement).filter(
        and_(
            WageStatement.employee_id == employee_id,
            WageStatement.month == month,
            WageStatement.year == year
        )
    ).first()

    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wage statement not found"
        )

    # Get employee details
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or employee.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    if not employee.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee email not found"
        )

    # Get tenant details
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()

    # Prepare data for PDF
    wage_data = {
        "employee_id": statement.employee_id,
        "month": statement.month,
        "year": statement.year,
        "total_days": statement.total_days,
        "present_days": statement.present_days,
        "absent_days": statement.absent_days,
        "leave_days": statement.leave_days,
        "basic_salary": statement.basic_salary,
        "total_earnings": statement.total_earnings,
        "total_deductions": statement.total_deductions,
        "net_salary": statement.net_salary,
        "earnings_breakdown": statement.earnings_breakdown or {},
        "deductions_breakdown": statement.deductions_breakdown or {}
    }

    # Get related data
    designation_name = employee.designation.name if employee.designation else "N/A"
    department_name = employee.department.name if employee.department else "N/A"

    # Get bank and statutory details
    bank_account = "N/A"
    pan_number = "N/A"
    pf_number = "N/A"

    if employee.bank_details:
        bank_account = employee.bank_details.account_number
        if employee.bank_details.pan_number:
            pan_number = employee.bank_details.pan_number

    if employee.statutory_details:
        if employee.statutory_details.pan_number:
            pan_number = employee.statutory_details.pan_number
        if employee.statutory_details.uan_number:
            pf_number = employee.statutory_details.uan_number

    employee_data = {
        "employee_code": employee.employee_code,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "designation": designation_name,
        "department": department_name,
        "date_of_joining": str(employee.date_of_joining) if employee.date_of_joining else "N/A",
        "bank_account": bank_account,
        "pan": pan_number,
        "pf_number": pf_number
    }

    tenant_data = {
        "name": tenant.name if tenant else "Company Name",
        "address": tenant.address if tenant and hasattr(tenant, 'address') else "Company Address"
    }

    # Generate PDF
    pdf_buffer = PDFGenerator.generate_payslip(
        wage_statement=wage_data,
        employee_details=employee_data,
        tenant_details=tenant_data
    )

    # Send email
    email_service = EmailService()
    result = email_service.send_payslip_email(
        employee_email=employee.email,
        employee_name=f"{employee.first_name} {employee.last_name}",
        month=month,
        year=year,
        payslip_pdf=pdf_buffer,
        company_name=tenant.name if tenant else "Company Name"
    )

    if result:
        return {
            "success": True,
            "message": f"Payslip sent successfully to {employee.email}"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email. Please check SMTP configuration."
        )


@router.post("/send-bulk-payslips")
def send_bulk_payslips(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020, le=2030),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Send payslips via email to all employees"""
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

    # Prepare payslip data for all employees
    payslip_data_list = []
    skipped = 0

    for statement in statements:
        employee = db.query(Employee).filter(Employee.id == statement.employee_id).first()

        if not employee.email:
            skipped += 1
            continue

        # Prepare wage data
        wage_data = {
            "employee_id": statement.employee_id,
            "month": statement.month,
            "year": statement.year,
            "total_days": statement.total_days,
            "present_days": statement.present_days,
            "absent_days": statement.absent_days,
            "leave_days": statement.leave_days,
            "basic_salary": statement.basic_salary,
            "total_earnings": statement.total_earnings,
            "total_deductions": statement.total_deductions,
            "net_salary": statement.net_salary,
            "earnings_breakdown": statement.earnings_breakdown or {},
            "deductions_breakdown": statement.deductions_breakdown or {}
        }

        employee_data = {
            "employee_code": employee.employee_code,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "designation": employee.designation,
            "department": employee.department,
            "date_of_joining": str(employee.date_of_joining) if employee.date_of_joining else "N/A",
            "bank_account": employee.bank_account if hasattr(employee, 'bank_account') else "N/A",
            "pan": employee.pan if hasattr(employee, 'pan') else "N/A",
            "pf_number": employee.pf_number if hasattr(employee, 'pf_number') else "N/A"
        }

        tenant_data = {
            "name": tenant.name if tenant else "Company Name",
            "address": tenant.address if tenant and hasattr(tenant, 'address') else "Company Address"
        }

        # Generate PDF
        pdf_buffer = PDFGenerator.generate_payslip(
            wage_statement=wage_data,
            employee_details=employee_data,
            tenant_details=tenant_data
        )

        payslip_data_list.append({
            'employee_email': employee.email,
            'employee_name': f"{employee.first_name} {employee.last_name}",
            'month': month,
            'year': year,
            'payslip_pdf': pdf_buffer
        })

    # Send bulk emails
    email_service = EmailService()
    result = email_service.send_bulk_payslips(
        payslip_data_list=payslip_data_list,
        company_name=tenant.name if tenant else "Company Name"
    )

    return {
        "success": True,
        "message": f"Bulk payslip sending complete",
        "summary": {
            "total_statements": len(statements),
            "emails_sent": result['successful'],
            "emails_failed": result['failed'],
            "skipped_no_email": skipped
        },
        "failed_emails": result.get('failed_emails', [])
    }
