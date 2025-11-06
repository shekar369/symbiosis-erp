from typing import Dict, List, Tuple, Optional
from datetime import datetime, date, time
from openpyxl import load_workbook
from sqlalchemy.orm import Session
import logging

from app.models.attendance import AttendanceStatus
from app.models.employee import Employee

logger = logging.getLogger(__name__)


class AttendanceUploadService:
    """Service for parsing and processing attendance Excel uploads"""

    # Mapping of Excel codes to AttendanceStatus enum
    STATUS_MAPPING = {
        "P": AttendanceStatus.PRESENT,
        "WO": AttendanceStatus.WEEKLY_OFF,
        "H": AttendanceStatus.HOLIDAY,
        "A": AttendanceStatus.ABSENT,
        "L": AttendanceStatus.LEAVE,
        "HD": AttendanceStatus.HALF_DAY,
    }

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id
        self.errors = []
        self.warnings = []

    def parse_attendance_file(self, file_path: str) -> Tuple[List[Dict], Dict]:
        """
        Parse attendance Excel file and extract attendance records

        Returns:
            Tuple of (attendance_records, metadata)
            - attendance_records: List of dicts with employee_id, date, status, check_in, check_out
            - metadata: Dict with month, year, total_records, employee_count, etc.
        """
        try:
            wb = load_workbook(file_path, data_only=True)
            ws = wb["Attendance Data"]

            # Extract month/year from Row 7
            month_year = self._extract_month_year(ws)
            if not month_year:
                raise ValueError("Could not extract month/year from attendance sheet")

            # Get employee data and attendance records
            attendance_records = []
            employee_ids_in_file = set()

            # Start from row 11 (first data row)
            for row_idx in range(11, ws.max_row + 1):
                employee_id_cell = ws.cell(row=row_idx, column=2).value  # Column B: Employee ID
                employee_name_cell = ws.cell(row=row_idx, column=3).value  # Column C: Name

                # Skip empty rows
                if not employee_id_cell:
                    continue

                # Extract employee ID (handle both direct values and formula references)
                employee_id = self._extract_employee_id(employee_id_cell)
                if not employee_id:
                    self.warnings.append(f"Row {row_idx}: Could not extract employee ID")
                    continue

                employee_ids_in_file.add(employee_id)

                # Validate employee exists in database for this tenant
                employee = self._get_employee(employee_id)
                if not employee:
                    self.errors.append(f"Row {row_idx}: Employee ID {employee_id} not found in database")
                    continue

                # Process each day in the month (columns 4 onwards, representing days 1-31)
                records = self._process_employee_attendance(
                    ws, row_idx, employee_id, month_year
                )
                attendance_records.extend(records)

            wb.close()

            metadata = {
                "month": month_year["month"],
                "year": month_year["year"],
                "total_records": len(attendance_records),
                "employee_count": len(employee_ids_in_file),
                "errors": self.errors,
                "warnings": self.warnings
            }

            return attendance_records, metadata

        except Exception as e:
            logger.error(f"Error parsing attendance file: {str(e)}")
            raise

    def _extract_month_year(self, ws) -> Optional[Dict]:
        """Extract month and year from Row 7, Column 16 (based on Excel structure)"""
        # Row 7, Column 16 contains the wage period date
        cell_value = ws.cell(row=7, column=16).value

        if cell_value:
            if isinstance(cell_value, datetime):
                return {
                    "month": cell_value.month,
                    "year": cell_value.year
                }
            elif isinstance(cell_value, date):
                return {
                    "month": cell_value.month,
                    "year": cell_value.year
                }
            elif isinstance(cell_value, str):
                # Try to parse string date
                try:
                    parsed_date = datetime.strptime(cell_value.split()[0], "%Y-%m-%d")
                    return {
                        "month": parsed_date.month,
                        "year": parsed_date.year
                    }
                except (ValueError, IndexError):
                    pass

        # Fallback: search in row 7 for any date value
        for col in range(1, min(20, ws.max_column + 1)):
            cell_value = ws.cell(row=7, column=col).value
            if cell_value:
                if isinstance(cell_value, datetime):
                    return {
                        "month": cell_value.month,
                        "year": cell_value.year
                    }
                elif isinstance(cell_value, date):
                    return {
                        "month": cell_value.month,
                        "year": cell_value.year
                    }

        return None

    def _extract_employee_id(self, cell_value) -> Optional[str]:
        """Extract employee ID from cell (handles both values and formulas)"""
        if cell_value is None:
            return None

        # If it's already a simple value, return it
        if isinstance(cell_value, (int, str)):
            return str(cell_value).strip()

        return None

    def _get_employee(self, employee_code: str) -> Optional[Employee]:
        """Get employee from database by employee code and tenant"""
        return self.db.query(Employee).filter(
            Employee.employee_code == employee_code,
            Employee.tenant_id == self.tenant_id
        ).first()

    def _process_employee_attendance(
        self, ws, row_idx: int, employee_id: str, month_year: Dict
    ) -> List[Dict]:
        """Process attendance for one employee for the entire month"""
        records = []
        year = month_year["year"]
        month = month_year["month"]

        # Determine number of days in the month
        import calendar
        days_in_month = calendar.monthrange(year, month)[1]

        # Process each day (columns start from 4, representing day 1)
        for day in range(1, days_in_month + 1):
            col_idx = 3 + day  # Column 4 is day 1, column 5 is day 2, etc.

            if col_idx > ws.max_column:
                break

            cell_value = ws.cell(row=row_idx, column=col_idx).value

            # Skip empty cells
            if not cell_value:
                continue

            # Map Excel code to AttendanceStatus
            status_code = str(cell_value).strip().upper()
            status = self.STATUS_MAPPING.get(status_code)

            if not status:
                self.warnings.append(
                    f"Row {row_idx}, Day {day}: Unknown status code '{status_code}', skipping"
                )
                continue

            # Create attendance record
            attendance_date = date(year, month, day)

            # Set check_in and check_out times based on status
            check_in_time = None
            check_out_time = None
            hours_worked = 0

            if status == AttendanceStatus.PRESENT:
                # Default work hours (9 AM to 6 PM)
                check_in_time = time(9, 0, 0)
                check_out_time = time(18, 0, 0)
                hours_worked = 8
            elif status == AttendanceStatus.HALF_DAY:
                # Half day (9 AM to 1 PM)
                check_in_time = time(9, 0, 0)
                check_out_time = time(13, 0, 0)
                hours_worked = 4

            records.append({
                "employee_id": employee_id,
                "date": attendance_date,
                "check_in": check_in_time,
                "check_out": check_out_time,
                "status": status.value,
                "hours_worked": hours_worked
            })

        return records

    def validate_records(self, records: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """
        Validate attendance records before insertion

        Returns:
            Tuple of (valid_records, validation_errors)
        """
        valid_records = []
        validation_errors = []

        for idx, record in enumerate(records):
            try:
                # Validate employee exists
                employee = self._get_employee(record["employee_id"])
                if not employee:
                    validation_errors.append(
                        f"Record {idx + 1}: Employee {record['employee_id']} not found"
                    )
                    continue

                # Update employee_id to database ID (not employee_id string)
                record["employee_id"] = employee.id

                # Validate date
                if not isinstance(record["date"], date):
                    validation_errors.append(
                        f"Record {idx + 1}: Invalid date format"
                    )
                    continue

                # Validate status
                if record["status"] not in [s.value for s in AttendanceStatus]:
                    validation_errors.append(
                        f"Record {idx + 1}: Invalid status '{record['status']}'"
                    )
                    continue

                valid_records.append(record)

            except Exception as e:
                validation_errors.append(f"Record {idx + 1}: {str(e)}")

        return valid_records, validation_errors
