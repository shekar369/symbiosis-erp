"""
Service for generating attendance template Excel files

This service creates a downloadable Excel template that employers can use
to fill in attendance data and upload back to the system.
"""

from typing import List, Optional
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime, date
from calendar import monthrange
from sqlalchemy.orm import Session
import os

from app.models.employee import Employee


class AttendanceTemplateService:
    """Service for generating attendance Excel templates"""

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def generate_template(
        self, month: int, year: int, company_name: str = "Company Name",
        company_address: str = "Company Address"
    ) -> str:
        """
        Generate an attendance template Excel file

        Args:
            month: Month (1-12)
            year: Year (e.g., 2024)
            company_name: Name of the company
            company_address: Address of the company

        Returns:
            Path to the generated Excel file
        """
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance Data"

        # Get employees for this tenant
        employees = self.db.query(Employee).filter(
            Employee.tenant_id == self.tenant_id
        ).order_by(Employee.employee_code).all()

        # Get number of days in the month
        _, days_in_month = monthrange(year, month)

        # Define styles
        header_font = Font(name='Arial', size=12, bold=True)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font_white = Font(name='Arial', size=11, bold=True, color="FFFFFF")
        sub_header_fill = PatternFill(start_color="B8CCE4", end_color="B8CCE4", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Row 1: Title
        ws['A1'] = "MUSTER ROLL STATEMENT"
        ws['A1'].font = Font(name='Arial', size=14, bold=True)
        ws.merge_cells('A1:E1')

        # Row 3: Company Name
        ws['A3'] = "Name and address of Employer:"
        ws['A3'].font = Font(name='Arial', size=10, bold=True)
        ws['P3'] = company_name
        ws['P3'].font = Font(name='Arial', size=10)

        # Row 4: Company Address
        ws['P4'] = company_address
        ws['P4'].font = Font(name='Arial', size=10)

        # Row 5: Nature and location
        ws['A5'] = "Nature and location of work:"
        ws['A5'].font = Font(name='Arial', size=10, bold=True)
        ws['P5'] = "As per company details"
        ws['P5'].font = Font(name='Arial', size=10)

        # Row 7: Wage period
        ws['A7'] = "Wage period: Monthly"
        ws['A7'].font = Font(name='Arial', size=10, bold=True)
        ws['P7'] = datetime(year, month, 1)
        ws['P7'].number_format = 'YYYY-MM-DD'
        ws['P7'].font = Font(name='Arial', size=10)

        # Row 9: Column headers (S.No, Employee ID, Name, ATTENDANCE)
        headers = ['S.No', 'Employee ID', 'Name of Workman', 'ATTENDANCE']
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=9, column=col_idx)
            cell.value = header
            cell.font = header_font_white
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

        # Merge ATTENDANCE header across all days
        ws.merge_cells(start_row=9, start_column=4, end_row=9, end_column=3 + days_in_month)

        # Row 10: Day numbers (1, 2, 3, ..., 31)
        for day in range(1, days_in_month + 1):
            cell = ws.cell(row=10, column=3 + day)
            cell.value = day
            cell.font = Font(name='Arial', size=10, bold=True)
            cell.fill = sub_header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

        # Data rows: Add employees
        for idx, employee in enumerate(employees, start=1):
            row_idx = 10 + idx

            # S.No
            cell = ws.cell(row=row_idx, column=1)
            cell.value = idx
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            # Employee ID
            cell = ws.cell(row=row_idx, column=2)
            cell.value = employee.employee_code
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            # Name
            cell = ws.cell(row=row_idx, column=3)
            cell.value = f"{employee.first_name} {employee.last_name}"
            cell.alignment = Alignment(horizontal='left', vertical='center')
            cell.border = border

            # Attendance columns (leave empty for user to fill)
            for day in range(1, days_in_month + 1):
                cell = ws.cell(row=row_idx, column=3 + day)
                cell.value = ""
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = border

        # Add instructions sheet
        ws_instructions = wb.create_sheet("Instructions")

        instructions = [
            "ATTENDANCE TEMPLATE INSTRUCTIONS",
            "",
            "How to fill the attendance template:",
            "",
            "1. Fill in the attendance codes for each employee for each day of the month",
            "",
            "2. Use the following attendance codes:",
            "   • P  = Present",
            "   • A  = Absent",
            "   • L  = Leave",
            "   • WO = Weekly Off",
            "   • H  = Holiday",
            "   • HD = Half Day",
            "",
            "3. Leave cells empty for days that don't apply",
            "",
            "4. Do NOT modify:",
            "   • Employee IDs (Column B)",
            "   • Employee Names (Column C)",
            "   • Header rows (Rows 1-10)",
            "   • The structure of the template",
            "",
            "5. After filling, save the file and upload it through the system",
            "",
            "6. The system will validate:",
            "   • All employee IDs exist in the database",
            "   • Attendance codes are valid",
            "   • Dates are within the specified month",
            "",
            "7. If there are any errors during upload, the system will provide detailed error messages",
            "",
            f"Template generated for: {datetime(year, month, 1).strftime('%B %Y')}",
            f"Number of employees: {len(employees)}",
            f"Days in month: {days_in_month}",
        ]

        for row_idx, instruction in enumerate(instructions, start=1):
            ws_instructions[f'A{row_idx}'] = instruction
            if row_idx == 1:
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=14, bold=True)
            elif "•" in instruction or row_idx in [2, 6]:
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=11, bold=True)
            else:
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=10)

        # Set column widths
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 30
        for day in range(1, days_in_month + 1):
            col_letter = get_column_letter(3 + day)
            ws.column_dimensions[col_letter].width = 4

        ws_instructions.column_dimensions['A'].width = 80

        # Save the file
        template_dir = "uploads/templates"
        os.makedirs(template_dir, exist_ok=True)

        filename = f"attendance_template_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join(template_dir, filename)

        wb.save(file_path)
        wb.close()

        return file_path

    def get_template_info(self, month: int, year: int) -> dict:
        """
        Get information about what the template will contain

        Args:
            month: Month (1-12)
            year: Year (e.g., 2024)

        Returns:
            Dictionary with template information
        """
        employee_count = self.db.query(Employee).filter(
            Employee.tenant_id == self.tenant_id
        ).count()

        _, days_in_month = monthrange(year, month)

        return {
            "month": month,
            "year": year,
            "month_name": datetime(year, month, 1).strftime('%B'),
            "employee_count": employee_count,
            "days_in_month": days_in_month,
            "expected_records": employee_count * days_in_month,
            "valid_codes": ["P", "A", "L", "WO", "H", "HD"]
        }
