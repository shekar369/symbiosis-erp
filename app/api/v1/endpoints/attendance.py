from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import logging
from datetime import datetime

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUploadResponse
from app.crud.attendance import attendance as attendance_crud
from app.models.user import User
from app.models.tenant import Tenant
from app.services.attendance_upload_service import AttendanceUploadService
from app.services.attendance_template_service import AttendanceTemplateService

router = APIRouter()
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads/attendance"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=AttendanceResponse)
async def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return attendance_crud.create_attendance(db=db, attendance=attendance)


@router.get("/", response_model=List[AttendanceResponse])
async def list_attendance(
    skip: int = 0,
    limit: int = 20,
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return attendance_crud.get_attendance_records(db=db, skip=skip, limit=limit, employee_id=employee_id)


@router.post("/upload", response_model=AttendanceUploadResponse)
async def upload_attendance(
    file: UploadFile = File(...),
    replace_existing: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload attendance data from Excel file

    Args:
        file: Excel file with attendance data (expected format: Employee Database.xlsx structure)
        replace_existing: If True, delete existing attendance records for the month before uploading
        db: Database session
        current_user: Current authenticated user

    Returns:
        AttendanceUploadResponse with upload status and statistics
    """

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only Excel files (.xlsx, .xls) are supported"
        )

    # Save uploaded file temporarily
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File uploaded: {file_path}")

        # Create upload tracking record
        upload_record = attendance_crud.create_upload_record(
            db=db,
            tenant_id=current_user.tenant_id,
            file_name=file.filename,
            file_path=file_path,
            uploaded_by=current_user.id,
            total_records=0  # Will update after parsing
        )

        # Parse the attendance file
        upload_service = AttendanceUploadService(db=db, tenant_id=current_user.tenant_id)
        attendance_records, metadata = upload_service.parse_attendance_file(file_path)

        logger.info(f"Parsed {len(attendance_records)} attendance records from file")

        # Validate records
        valid_records, validation_errors = upload_service.validate_records(attendance_records)

        logger.info(f"Validated {len(valid_records)} records, {len(validation_errors)} errors")

        # If replace_existing is True, delete existing attendance for the month
        if replace_existing and len(valid_records) > 0:
            # Get unique employee IDs from valid records
            employee_ids = list(set([record["employee_id"] for record in valid_records]))

            deleted_count = attendance_crud.delete_attendance_for_month_bulk(
                db=db,
                employee_ids=employee_ids,
                month=metadata["month"],
                year=metadata["year"]
            )

            logger.info(f"Deleted {deleted_count} existing attendance records for {metadata['month']}/{metadata['year']}")

        # Bulk insert valid records
        successful_count = 0
        if len(valid_records) > 0:
            successful_count = attendance_crud.bulk_create(db=db, attendance_records=valid_records)
            logger.info(f"Successfully inserted {successful_count} attendance records")

        # Calculate status
        failed_count = len(attendance_records) - successful_count
        if successful_count == len(attendance_records):
            status = "success"
        elif successful_count > 0:
            status = "partial"
        else:
            status = "failed"

        # Update upload record with results
        upload_record = attendance_crud.update_upload_record(
            db=db,
            upload_id=upload_record.id,
            successful_records=successful_count,
            failed_records=failed_count,
            status=status
        )

        # Prepare response
        response_data = {
            "id": upload_record.id,
            "file_name": upload_record.file_name,
            "total_records": len(attendance_records),
            "successful_records": successful_count,
            "failed_records": failed_count,
            "status": status,
            "uploaded_at": upload_record.uploaded_at,
            "errors": metadata.get("errors", []) + validation_errors,
            "warnings": metadata.get("warnings", []),
            "metadata": {
                "month": metadata["month"],
                "year": metadata["year"],
                "employee_count": metadata["employee_count"]
            }
        }

        return response_data

    except Exception as e:
        logger.error(f"Error processing attendance upload: {str(e)}")

        # Update upload record as failed if it exists
        try:
            if 'upload_record' in locals():
                attendance_crud.update_upload_record(
                    db=db,
                    upload_id=upload_record.id,
                    successful_records=0,
                    failed_records=0,
                    status="failed"
                )
        except:
            pass

        raise HTTPException(
            status_code=500,
            detail=f"Error processing attendance upload: {str(e)}"
        )

    finally:
        # Clean up uploaded file (optional - you may want to keep it for audit)
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        pass


@router.get("/template/info")
async def get_template_info(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get information about the attendance template for a specific month

    Args:
        month: Month (1-12)
        year: Year (e.g., 2024)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Template information including employee count, days in month, etc.
    """
    # Validate month and year
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

    if year < 2000 or year > 2100:
        raise HTTPException(status_code=400, detail="Year must be between 2000 and 2100")

    template_service = AttendanceTemplateService(db=db, tenant_id=current_user.tenant_id)
    template_info = template_service.get_template_info(month=month, year=year)

    return template_info


@router.get("/template/download")
async def download_template(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Download attendance template Excel file for a specific month

    Args:
        month: Month (1-12)
        year: Year (e.g., 2024)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Excel file download
    """
    # Validate month and year
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

    if year < 2000 or year > 2100:
        raise HTTPException(status_code=400, detail="Year must be between 2000 and 2100")

    try:
        # Get tenant info for company name/address
        tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
        company_name = tenant.name if tenant else "Company Name"
        company_address = tenant.address if tenant and hasattr(tenant, 'address') else "Company Address"

        # Generate template
        template_service = AttendanceTemplateService(db=db, tenant_id=current_user.tenant_id)
        file_path = template_service.generate_template(
            month=month,
            year=year,
            company_name=company_name,
            company_address=company_address
        )

        # Get month name for filename
        month_name = datetime(year, month, 1).strftime('%B')
        filename = f"Attendance_Template_{month_name}_{year}.xlsx"

        logger.info(f"Generated template for {month_name} {year}: {file_path}")

        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating template: {str(e)}"
        )
