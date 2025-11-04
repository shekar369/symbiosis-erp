import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime
import re


class ValidationError:
    """Validation error details"""
    def __init__(self, row: int, column: str, value: Any, error: str):
        self.row = row
        self.column = column
        self.value = value
        self.error = error

    def to_dict(self):
        return {
            "row": self.row,
            "column": self.column,
            "value": str(self.value),
            "error": self.error
        }


class ExcelParser:
    """Enhanced Excel parser with validation"""

    @staticmethod
    def validate_employee_code(value: str) -> Tuple[bool, str]:
        """Validate employee code format"""
        if pd.isna(value) or not value:
            return False, "Employee code is required"
        if not isinstance(value, str):
            value = str(value)
        if len(value) < 3:
            return False, "Employee code must be at least 3 characters"
        return True, ""

    @staticmethod
    def validate_email(value: str) -> Tuple[bool, str]:
        """Validate email format"""
        if pd.isna(value) or not value:
            return True, ""  # Email is optional
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, str(value)):
            return False, "Invalid email format"
        return True, ""

    @staticmethod
    def validate_phone(value: str) -> Tuple[bool, str]:
        """Validate phone number"""
        if pd.isna(value) or not value:
            return False, "Phone number is required"
        phone = str(value).replace(" ", "").replace("-", "")
        if not phone.isdigit() or len(phone) != 10:
            return False, "Phone must be 10 digits"
        return True, ""

    @staticmethod
    def validate_date(value: Any, field_name: str) -> Tuple[bool, str]:
        """Validate date format"""
        if pd.isna(value) or not value:
            return False, f"{field_name} is required"
        try:
            if isinstance(value, str):
                # Try multiple date formats
                for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                    try:
                        datetime.strptime(value, fmt)
                        return True, ""
                    except ValueError:
                        continue
                return False, f"Invalid date format. Use DD/MM/YYYY"
            elif isinstance(value, datetime):
                return True, ""
            else:
                return False, f"Invalid date format"
        except Exception:
            return False, f"Invalid date format"

    @staticmethod
    def parse_employee_file(file_path: str, validate: bool = True) -> Tuple[List[Dict[str, Any]], List[ValidationError]]:
        """
        Parse employee Excel file with validation
        Returns: (valid_records, errors)
        """
        try:
            # Read Excel file, skip first 4 rows (title, instructions, empty, headers)
            df = pd.read_excel(file_path, header=3)

            # Remove completely empty rows
            df = df.dropna(how='all')

            # Define required columns (marked with *)
            required_columns = {
                'Employee Code*': 'employee_code',
                'First Name*': 'first_name',
                'Last Name*': 'last_name',
                'Date of Birth (DD/MM/YYYY)*': 'date_of_birth',
                'Date of Joining (DD/MM/YYYY)*': 'date_of_joining',
                'Gender*': 'gender',
                'Mobile Number*': 'phone',
            }

            # Optional columns
            optional_columns = {
                'Father Name': 'father_name',
                'Email': 'email',
                'Address Line 1': 'address_line1',
                'Address Line 2': 'address_line2',
                'City': 'city',
                'State': 'state',
                'Postal Code': 'postal_code',
                'Aadhar Number': 'aadhar_number',
                'PAN Number': 'pan_number',
                'UAN Number': 'uan_number',
                'ESI Number': 'esi_number',
                'Bank Name': 'bank_name',
                'Bank Account Number': 'bank_account_number',
                'IFSC Code': 'ifsc_code',
                'Department': 'department',
                'Designation': 'designation',
                'Grade': 'grade',
                'Basic Salary': 'basic_salary',
                'Status (active/inactive/terminated)': 'status',
            }

            valid_records = []
            errors = []

            # Process each row
            for idx, row in df.iterrows():
                row_num = idx + 5  # Account for header rows
                record = {}
                row_errors = []

                # Validate required fields
                for excel_col, db_field in required_columns.items():
                    value = row.get(excel_col)

                    # Special validation for each field
                    if db_field == 'employee_code':
                        is_valid, error_msg = ExcelParser.validate_employee_code(value)
                        if not is_valid:
                            row_errors.append(ValidationError(row_num, excel_col, value, error_msg))
                        else:
                            record[db_field] = str(value).strip()

                    elif db_field == 'phone':
                        is_valid, error_msg = ExcelParser.validate_phone(value)
                        if not is_valid:
                            row_errors.append(ValidationError(row_num, excel_col, value, error_msg))
                        else:
                            record[db_field] = str(value).strip()

                    elif db_field in ['date_of_birth', 'date_of_joining']:
                        is_valid, error_msg = ExcelParser.validate_date(value, excel_col)
                        if not is_valid:
                            row_errors.append(ValidationError(row_num, excel_col, value, error_msg))
                        else:
                            # Convert to datetime if string
                            if isinstance(value, str):
                                for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                                    try:
                                        record[db_field] = datetime.strptime(value, fmt).date()
                                        break
                                    except ValueError:
                                        continue
                            else:
                                record[db_field] = value

                    elif db_field == 'gender':
                        if pd.isna(value) or not value:
                            row_errors.append(ValidationError(row_num, excel_col, value, "Gender is required"))
                        elif str(value).lower() not in ['male', 'female', 'other']:
                            row_errors.append(ValidationError(row_num, excel_col, value, "Gender must be Male, Female, or Other"))
                        else:
                            record[db_field] = str(value).strip().lower()

                    else:
                        # Other required fields
                        if pd.isna(value) or not value:
                            row_errors.append(ValidationError(row_num, excel_col, value, f"{excel_col} is required"))
                        else:
                            record[db_field] = str(value).strip()

                # Process optional fields
                for excel_col, db_field in optional_columns.items():
                    value = row.get(excel_col)
                    if not pd.isna(value) and value:
                        if db_field == 'email':
                            is_valid, error_msg = ExcelParser.validate_email(value)
                            if not is_valid:
                                row_errors.append(ValidationError(row_num, excel_col, value, error_msg))
                            else:
                                record[db_field] = str(value).strip()
                        elif db_field == 'basic_salary':
                            try:
                                record[db_field] = float(value)
                            except ValueError:
                                row_errors.append(ValidationError(row_num, excel_col, value, "Invalid salary amount"))
                        elif db_field == 'status':
                            status_lower = str(value).lower().strip()
                            if status_lower not in ['active', 'inactive', 'terminated']:
                                row_errors.append(ValidationError(row_num, excel_col, value, "Status must be active, inactive, or terminated"))
                            else:
                                record[db_field] = status_lower
                        else:
                            record[db_field] = str(value).strip()

                # Add row to appropriate list
                if row_errors:
                    errors.extend(row_errors)
                else:
                    valid_records.append(record)

            return valid_records, errors

        except Exception as e:
            raise Exception(f"Error parsing Excel file: {str(e)}")

    @staticmethod
    def parse_attendance_file(file_path: str, validate: bool = True) -> Tuple[List[Dict[str, Any]], List[ValidationError]]:
        """
        Parse attendance Excel file with validation
        Expected columns: Employee Code, Employee Name, Date, Check-In Time, Check-Out Time, Status, Remarks
        Returns: (valid_records, errors)
        """
        try:
            # Read Excel file, skip first 2 rows (title, empty, headers at row 3)
            df = pd.read_excel(file_path, header=2)

            # Remove completely empty rows
            df = df.dropna(how='all')

            valid_records = []
            errors = []

            # Process each row
            for idx, row in df.iterrows():
                row_num = idx + 4  # Account for header rows
                record = {}
                row_errors = []

                # Employee Code - required
                emp_code = row.get('Employee Code')
                if pd.isna(emp_code) or not emp_code:
                    row_errors.append(ValidationError(row_num, 'Employee Code', emp_code, "Employee code is required"))
                else:
                    record['employee_code'] = str(emp_code).strip()

                # Date - required
                date_val = row.get('Date (DD/MM/YYYY)')
                is_valid, error_msg = ExcelParser.validate_date(date_val, 'Date')
                if not is_valid:
                    row_errors.append(ValidationError(row_num, 'Date', date_val, error_msg))
                else:
                    if isinstance(date_val, str):
                        for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                            try:
                                record['date'] = datetime.strptime(date_val, fmt).date()
                                break
                            except ValueError:
                                continue
                    else:
                        record['date'] = date_val

                # Check-in time
                check_in = row.get('Check-In Time (HH:MM)')
                if not pd.isna(check_in) and check_in:
                    record['check_in'] = str(check_in).strip()

                # Check-out time
                check_out = row.get('Check-Out Time (HH:MM)')
                if not pd.isna(check_out) and check_out:
                    record['check_out'] = str(check_out).strip()

                # Status
                status = row.get('Status')
                if not pd.isna(status) and status:
                    status_lower = str(status).lower().strip()
                    if status_lower in ['present', 'absent', 'half-day', 'leave']:
                        record['status'] = status_lower
                    else:
                        row_errors.append(ValidationError(row_num, 'Status', status, "Status must be Present, Absent, Half-day, or Leave"))

                # Remarks
                remarks = row.get('Remarks')
                if not pd.isna(remarks) and remarks:
                    record['remarks'] = str(remarks).strip()

                # Add row to appropriate list
                if row_errors:
                    errors.extend(row_errors)
                else:
                    valid_records.append(record)

            return valid_records, errors

        except Exception as e:
            raise Exception(f"Error parsing attendance file: {str(e)}")
