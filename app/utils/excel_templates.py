import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from io import BytesIO
from typing import Optional
from datetime import datetime


class ExcelTemplateGenerator:
    """Generate Excel templates for various HR operations"""

    @staticmethod
    def create_employee_database_template(
        act_type: str = "contract_labour",
        location: Optional[str] = None
    ) -> BytesIO:
        """Generate employee database template based on act type and location"""

        # Define columns based on act type
        base_columns = [
            "Employee Code*",
            "First Name*",
            "Last Name*",
            "Father Name",
            "Date of Birth (DD/MM/YYYY)*",
            "Date of Joining (DD/MM/YYYY)*",
            "Gender*",
            "Mobile Number*",
            "Email",
            "Address Line 1",
            "Address Line 2",
            "City",
            "State",
            "Postal Code",
            "Aadhar Number",
            "PAN Number",
            "UAN Number",
            "ESI Number",
            "Bank Name",
            "Bank Account Number",
            "IFSC Code",
            "Department",
            "Designation",
            "Grade",
            "Basic Salary",
            "Status (active/inactive/terminated)",
        ]

        # Add act-specific columns
        if act_type == "contract_labour":
            additional_columns = [
                "License Number",
                "Principal Employer",
                "Nature of Work",
                "Skilled/Unskilled",
            ]
        elif act_type == "factories":
            additional_columns = [
                "Factory License Number",
                "Workman Category",
                "Hazardous Work (Yes/No)",
            ]
        else:  # shops_establishment
            additional_columns = [
                "Shop Registration Number",
                "Category of Employee",
            ]

        all_columns = base_columns + additional_columns

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Employee Master"

        # Add title row
        title_text = f"Employee Database Template - {act_type.replace('_', ' ').title()}"
        if location:
            title_text += f" - {location}"

        ws.merge_cells('A1:E1')
        title_cell = ws['A1']
        title_cell.value = title_text
        title_cell.font = Font(size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Add instructions row
        ws.merge_cells('A2:E2')
        instruction_cell = ws['A2']
        instruction_cell.value = "Instructions: Fill all columns marked with * (mandatory fields). Date format: DD/MM/YYYY"
        instruction_cell.font = Font(size=10, italic=True)
        instruction_cell.fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")

        # Add header row (row 4)
        header_row = 4
        for col_idx, column_name in enumerate(all_columns, start=1):
            cell = ws.cell(row=header_row, column=col_idx)
            cell.value = column_name
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # Set column width
            ws.column_dimensions[chr(64 + col_idx)].width = 18

        # Add sample data row
        sample_row = 5
        sample_data = [
            "EMP001",
            "John",
            "Doe",
            "Robert Doe",
            "15/01/1990",
            "01/04/2023",
            "Male",
            "9876543210",
            "john.doe@example.com",
            "123 Main Street",
            "Apartment 4B",
            "Hyderabad",
            "Telangana",
            "500001",
            "1234 5678 9012",
            "ABCDE1234F",
            "123456789012",
            "1234567890",
            "ABC Bank",
            "1234567890",
            "ABCD0123456",
            "Engineering",
            "Software Engineer",
            "Mid-Level",
            "50000",
            "active",
        ]

        # Add act-specific sample data
        if act_type == "contract_labour":
            sample_data.extend(["LIC/2023/001", "ABC Corp", "IT Support", "Skilled"])
        elif act_type == "factories":
            sample_data.extend(["FAC/2023/001", "Workman", "No"])
        else:
            sample_data.extend(["SHOP/2023/001", "Regular Employee"])

        for col_idx, value in enumerate(sample_data, start=1):
            cell = ws.cell(row=sample_row, column=col_idx)
            cell.value = value
            cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
            cell.alignment = Alignment(horizontal="left")

        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def create_attendance_template(month: int, year: int, employees: list) -> BytesIO:
        """Generate attendance template for a specific month with employee list"""

        wb = Workbook()
        ws = wb.active
        ws.title = f"Attendance {month:02d}-{year}"

        # Title
        ws.merge_cells('A1:E1')
        title_cell = ws['A1']
        title_cell.value = f"Attendance Sheet - {datetime(year, month, 1).strftime('%B %Y')}"
        title_cell.font = Font(size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Headers
        headers = ["Employee Code", "Employee Name", "Date (DD/MM/YYYY)", "Check-In Time (HH:MM)", "Check-Out Time (HH:MM)", "Status", "Remarks"]
        header_row = 3
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=header_row, column=col_idx)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.column_dimensions[chr(64 + col_idx)].width = 20

        # Add sample rows for each employee
        current_row = header_row + 1
        for emp in employees[:5]:  # Add first 5 employees as examples
            cell = ws.cell(row=current_row, column=1)
            cell.value = emp.get('employee_code', '')
            cell = ws.cell(row=current_row, column=2)
            cell.value = f"{emp.get('first_name', '')} {emp.get('last_name', '')}"
            # Leave other columns empty for data entry
            current_row += 1

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def create_salary_statement_template(
        month: int,
        year: int,
        act_type: str = "contract_labour"
    ) -> BytesIO:
        """Generate salary/wage statement template"""

        wb = Workbook()
        ws = wb.active
        ws.title = f"Salary {month:02d}-{year}"

        # Title
        month_name = datetime(year, month, 1).strftime('%B %Y')
        ws.merge_cells('A1:L1')
        title_cell = ws['A1']
        title_cell.value = f"Wage Statement - {month_name}"
        title_cell.font = Font(size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Headers
        headers = [
            "Employee Code",
            "Employee Name",
            "Days Worked",
            "Basic Salary",
            "HRA",
            "Other Allowances",
            "Gross Salary",
            "PF Deduction",
            "ESI Deduction",
            "TDS",
            "Other Deductions",
            "Net Salary",
        ]

        header_row = 3
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=header_row, column=col_idx)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.column_dimensions[chr(64 + col_idx)].width = 15

        # Sample data
        sample_row = 4
        sample_data = [
            "EMP001", "John Doe", "26", "30000", "12000", "5000",
            "47000", "3600", "705", "2000", "0", "40695"
        ]

        for col_idx, value in enumerate(sample_data, start=1):
            cell = ws.cell(row=sample_row, column=col_idx)
            cell.value = value
            cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def create_leave_register_template() -> BytesIO:
        """Generate leave register template"""

        wb = Workbook()
        ws = wb.active
        ws.title = "Leave Register"

        # Title
        ws.merge_cells('A1:F1')
        title_cell = ws['A1']
        title_cell.value = "Leave Register Template"
        title_cell.font = Font(size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Headers
        headers = [
            "Employee Code",
            "Employee Name",
            "Leave Type",
            "From Date (DD/MM/YYYY)",
            "To Date (DD/MM/YYYY)",
            "Number of Days",
            "Reason",
            "Status",
        ]

        header_row = 3
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=header_row, column=col_idx)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.column_dimensions[chr(64 + col_idx)].width = 18

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output
