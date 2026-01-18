from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import tempfile

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.employee import Employee, EmployeeStatus, EmployeeSalaryDetails
from app.models.attendance import Attendance
from app.models.organization import Department, Designation, Grade
from app.utils.excel_parser import ExcelParser

router = APIRouter()


@router.post("/employees")
async def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload employee data from Excel file
    Returns summary of uploaded, failed, and validation errors
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files (.xlsx, .xls) are supported"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse and validate Excel file
        valid_records, validation_errors = ExcelParser.parse_employee_file(tmp_file_path)

        uploaded_count = 0
        failed_count = 0
        errors_list = []

        # Convert validation errors to dict
        for error in validation_errors:
            errors_list.append(error.to_dict())

        # Process valid records
        for record in valid_records:
            try:
                # Check if employee code already exists
                existing = db.query(Employee).filter(
                    Employee.employee_code == record['employee_code'],
                    Employee.tenant_id == current_user.tenant_id
                ).first()

                if existing:
                    errors_list.append({
                        "row": "N/A",
                        "column": "employee_code",
                        "value": record['employee_code'],
                        "error": "Employee code already exists"
                    })
                    failed_count += 1
                    continue

                # Look up department, designation, grade if provided
                department = None
                if record.get('department'):
                    department = db.query(Department).filter(
                        Department.name == record['department'],
                        Department.tenant_id == current_user.tenant_id
                    ).first()

                designation = None
                if record.get('designation'):
                    designation = db.query(Designation).filter(
                        Designation.name == record['designation'],
                        Designation.tenant_id == current_user.tenant_id
                    ).first()

                grade = None
                if record.get('grade'):
                    grade = db.query(Grade).filter(
                        Grade.name == record['grade'],
                        Grade.tenant_id == current_user.tenant_id
                    ).first()

                # Create employee
                employee = Employee(
                    tenant_id=current_user.tenant_id,
                    employee_code=record['employee_code'],
                    first_name=record['first_name'],
                    last_name=record['last_name'],
                    email=record.get('email', f"{record['employee_code']}@temp.com"),
                    phone=record.get('phone'),
                    date_of_birth=record.get('date_of_birth'),
                    date_of_joining=record['date_of_joining'],
                    status=EmployeeStatus(record.get('status', 'active')),
                    department_id=department.id if department else None,
                    designation_id=designation.id if designation else None,
                    grade_id=grade.id if grade else None,
                )

                db.add(employee)
                uploaded_count += 1

            except Exception as e:
                errors_list.append({
                    "row": "N/A",
                    "column": "general",
                    "value": record.get('employee_code', 'Unknown'),
                    "error": str(e)
                })
                failed_count += 1

        # Commit all successful inserts
        if uploaded_count > 0:
            db.commit()

        return {
            "success": True,
            "message": f"Upload complete. {uploaded_count} employees uploaded, {failed_count} failed.",
            "summary": {
                "total_rows": len(valid_records) + len(validation_errors),
                "uploaded": uploaded_count,
                "failed": failed_count,
                "validation_errors": len(validation_errors)
            },
            "errors": errors_list[:100]  # Return first 100 errors
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)


@router.post("/attendance")
async def upload_attendance(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload attendance data from Excel file
    Returns summary of uploaded, failed, and validation errors
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files (.xlsx, .xls) are supported"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse and validate Excel file
        valid_records, validation_errors = ExcelParser.parse_attendance_file(tmp_file_path)

        uploaded_count = 0
        failed_count = 0
        errors_list = []

        # Convert validation errors to dict
        for error in validation_errors:
            errors_list.append(error.to_dict())

        # Process valid records
        for record in valid_records:
            try:
                # Find employee by code
                employee = db.query(Employee).filter(
                    Employee.employee_code == record['employee_code'],
                    Employee.tenant_id == current_user.tenant_id
                ).first()

                if not employee:
                    errors_list.append({
                        "row": "N/A",
                        "column": "employee_code",
                        "value": record['employee_code'],
                        "error": "Employee not found"
                    })
                    failed_count += 1
                    continue

                # Check if attendance already exists for this date
                existing = db.query(Attendance).filter(
                    Attendance.employee_id == employee.id,
                    Attendance.date == record['date']
                ).first()

                if existing:
                    # Update existing record
                    if record.get('check_in'):
                        existing.check_in = record['check_in']
                    if record.get('check_out'):
                        existing.check_out = record['check_out']
                    if record.get('status'):
                        existing.status = record['status']
                    if record.get('remarks'):
                        existing.remarks = record['remarks']
                else:
                    # Create new attendance record
                    attendance = Attendance(
                        employee_id=employee.id,
                        date=record['date'],
                        check_in=record.get('check_in'),
                        check_out=record.get('check_out'),
                        status=record.get('status', 'present'),
                        remarks=record.get('remarks'),
                    )
                    db.add(attendance)

                uploaded_count += 1

            except Exception as e:
                errors_list.append({
                    "row": "N/A",
                    "column": "general",
                    "value": record.get('employee_code', 'Unknown'),
                    "error": str(e)
                })
                failed_count += 1

        # Commit all successful inserts/updates
        if uploaded_count > 0:
            db.commit()

        return {
            "success": True,
            "message": f"Upload complete. {uploaded_count} attendance records processed, {failed_count} failed.",
            "summary": {
                "total_rows": len(valid_records) + len(validation_errors),
                "uploaded": uploaded_count,
                "failed": failed_count,
                "validation_errors": len(validation_errors)
            },
            "errors": errors_list[:100]  # Return first 100 errors
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)


@router.post("/wages")
async def upload_wages(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload wages data from Excel file
    Returns summary of uploaded, failed, and validation errors
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files (.xlsx, .xls) are supported"
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        # Parse and validate Excel file
        valid_records, validation_errors = ExcelParser.parse_wages_file(tmp_file_path)

        uploaded_count = 0
        failed_count = 0
        errors_list = []

        # Convert validation errors to dict
        for error in validation_errors:
            errors_list.append(error.to_dict())

        # Process valid records
        for record in valid_records:
            try:
                # Find employee by code
                employee = db.query(Employee).filter(
                    Employee.employee_code == record['employee_code'],
                    Employee.tenant_id == current_user.tenant_id
                ).first()

                if not employee:
                    errors_list.append({
                        "row": "N/A",
                        "column": "employee_code",
                        "value": record['employee_code'],
                        "error": "Employee not found"
                    })
                    failed_count += 1
                    continue

                # Check if salary details already exist
                salary_details = db.query(EmployeeSalaryDetails).filter(
                    EmployeeSalaryDetails.employee_id == employee.id
                ).first()

                if not salary_details:
                    salary_details = EmployeeSalaryDetails(employee_id=employee.id)
                    db.add(salary_details)

                # Update fields
                salary_details.basic_salary = record.get('basic_salary', 0)
                salary_details.hra = record.get('hra', 0)
                salary_details.conveyance_allowance = record.get('conveyance_allowance', 0)
                salary_details.special_allowance = record.get('special_allowance', 0)
                salary_details.other_allowance = record.get('other_allowance', 0)
                salary_details.pf_employee = record.get('pf_employee', 0)
                salary_details.pf_employer = record.get('pf_employer', 0)
                salary_details.esic_employee = record.get('esic_employee', 0)
                salary_details.esic_employer = record.get('esic_employer', 0)
                salary_details.professional_tax = record.get('professional_tax', 0)
                salary_details.tds = record.get('tds', 0)
                
                # Recalculate totals
                salary_details.gross_salary = (
                    salary_details.basic_salary + 
                    salary_details.hra + 
                    salary_details.conveyance_allowance + 
                    salary_details.special_allowance + 
                    salary_details.other_allowance
                )
                
                salary_details.total_deductions = (
                    salary_details.pf_employee + 
                    salary_details.esic_employee + 
                    salary_details.professional_tax + 
                    salary_details.tds
                )
                
                salary_details.net_salary = salary_details.gross_salary - salary_details.total_deductions
                
                # CTC Calculation (Gross + Employer Contributions)
                salary_details.ctc = (
                    salary_details.gross_salary + 
                    salary_details.pf_employer + 
                    salary_details.esic_employer
                )

                uploaded_count += 1

            except Exception as e:
                errors_list.append({
                    "row": "N/A",
                    "column": "general",
                    "value": record.get('employee_code', 'Unknown'),
                    "error": str(e)
                })
                failed_count += 1

        # Commit all successful inserts/updates
        if uploaded_count > 0:
            db.commit()

        return {
            "success": True,
            "message": f"Upload complete. {uploaded_count} wage records processed, {failed_count} failed.",
            "summary": {
                "total_rows": len(valid_records) + len(validation_errors),
                "uploaded": uploaded_count,
                "failed": failed_count,
                "validation_errors": len(validation_errors)
            },
            "errors": errors_list[:100]  # Return first 100 errors
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
