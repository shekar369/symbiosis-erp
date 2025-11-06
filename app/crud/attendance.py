from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.attendance import Attendance, AttendanceUpload
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class CRUDAttendance(CRUDBase[Attendance, AttendanceCreate, AttendanceUpdate]):
    def get_attendance_records(
        self, db: Session, skip: int = 0, limit: int = 20, employee_id: int = None
    ) -> List[Attendance]:
        query = db.query(Attendance)
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        return query.offset(skip).limit(limit).all()

    def create_attendance(self, db: Session, attendance: AttendanceCreate) -> Attendance:
        return self.create(db, obj_in=attendance)

    def bulk_create(self, db: Session, attendance_records: List[Dict]) -> int:
        """
        Bulk create attendance records

        Args:
            db: Database session
            attendance_records: List of dictionaries with attendance data

        Returns:
            Number of records created
        """
        try:
            db_records = [
                Attendance(**record) for record in attendance_records
            ]
            db.bulk_save_objects(db_records)
            db.commit()
            return len(db_records)
        except Exception as e:
            db.rollback()
            raise e

    def delete_attendance_for_month(
        self, db: Session, employee_id: int, month: int, year: int
    ) -> int:
        """
        Delete existing attendance records for an employee for a specific month

        Args:
            db: Database session
            employee_id: Employee database ID
            month: Month (1-12)
            year: Year (e.g., 2024)

        Returns:
            Number of records deleted
        """
        try:
            # Get first and last day of the month
            from calendar import monthrange
            _, last_day = monthrange(year, month)

            start_date = date(year, month, 1)
            end_date = date(year, month, last_day)

            deleted = db.query(Attendance).filter(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).delete()

            db.commit()
            return deleted
        except Exception as e:
            db.rollback()
            raise e

    def delete_attendance_for_month_bulk(
        self, db: Session, employee_ids: List[int], month: int, year: int
    ) -> int:
        """
        Delete existing attendance records for multiple employees for a specific month

        Args:
            db: Database session
            employee_ids: List of employee database IDs
            month: Month (1-12)
            year: Year (e.g., 2024)

        Returns:
            Number of records deleted
        """
        try:
            from calendar import monthrange
            _, last_day = monthrange(year, month)

            start_date = date(year, month, 1)
            end_date = date(year, month, last_day)

            deleted = db.query(Attendance).filter(
                and_(
                    Attendance.employee_id.in_(employee_ids),
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).delete(synchronize_session=False)

            db.commit()
            return deleted
        except Exception as e:
            db.rollback()
            raise e

    def create_upload_record(
        self, db: Session, tenant_id: int, file_name: str, file_path: str,
        uploaded_by: int, total_records: int
    ) -> AttendanceUpload:
        """
        Create an attendance upload tracking record

        Args:
            db: Database session
            tenant_id: Tenant ID
            file_name: Original file name
            file_path: Stored file path
            uploaded_by: User ID who uploaded
            total_records: Total records in file

        Returns:
            AttendanceUpload record
        """
        upload = AttendanceUpload(
            tenant_id=tenant_id,
            file_name=file_name,
            file_path=file_path,
            uploaded_by=uploaded_by,
            total_records=total_records,
            status="pending"
        )
        db.add(upload)
        db.commit()
        db.refresh(upload)
        return upload

    def update_upload_record(
        self, db: Session, upload_id: int,
        successful_records: int, failed_records: int, status: str
    ) -> AttendanceUpload:
        """
        Update attendance upload record with results

        Args:
            db: Database session
            upload_id: Upload record ID
            successful_records: Number of successful records
            failed_records: Number of failed records
            status: Upload status (success, partial, failed)

        Returns:
            Updated AttendanceUpload record
        """
        upload = db.query(AttendanceUpload).filter(AttendanceUpload.id == upload_id).first()
        if upload:
            upload.successful_records = successful_records
            upload.failed_records = failed_records
            upload.status = status
            db.commit()
            db.refresh(upload)
        return upload


attendance = CRUDAttendance(Attendance)
