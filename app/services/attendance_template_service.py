"""
Service for generating attendance template Excel files

This service creates a downloadable Excel template that employers can use
to fill in attendance data and upload back to the system.
"""

from typing import List, Optional, Dict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime, date
from calendar import monthrange
from sqlalchemy.orm import Session
from sqlalchemy import extract
import os

from app.models.employee import Employee
from app.models.holiday import Holiday, WorkingCalendar


class AttendanceTemplateService:
    """Service for generating attendance Excel templates"""

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def get_holidays_for_month(self, month: int, year: int) -> Dict[int, Dict]:
        """
        Get holidays for the specified month

        Returns:
            Dict mapping day number to holiday details
        """
        holidays = self.db.query(Holiday).filter(
            Holiday.tenant_id == self.tenant_id,
            extract('month', Holiday.date) == month,
            extract('year', Holiday.date) == year
        ).all()

        holiday_map = {}
        for holiday in holidays:
            day = holiday.date.day
            holiday_map[day] = {
                'name': holiday.name,
                'is_mandatory': holiday.is_mandatory,
                'description': holiday.description
            }
        return holiday_map

    def get_working_calendar(self) -> Optional[WorkingCalendar]:
        """Get the working calendar configuration for the tenant"""
        return self.db.query(WorkingCalendar).filter(
            WorkingCalendar.tenant_id == self.tenant_id
        ).first()

    def is_weekend(self, date_obj: date, working_calendar: Optional[WorkingCalendar]) -> bool:
        """Check if a date is a weekend based on working calendar"""
        if not working_calendar:
            # Default: Saturday and Sunday are weekends
            return date_obj.weekday() in [5, 6]

        weekday = date_obj.weekday()
        day_mapping = {
            0: working_calendar.monday,
            1: working_calendar.tuesday,
            2: working_calendar.wednesday,
            3: working_calendar.thursday,
            4: working_calendar.friday,
            5: working_calendar.saturday,
            6: working_calendar.sunday
        }

        # If day is marked as False in calendar, it's a weekend
        return not day_mapping.get(weekday, True)

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

        # Get holidays and working calendar
        holidays = self.get_holidays_for_month(month, year)
        working_calendar = self.get_working_calendar()

        # Define styles
        header_font = Font(name='Arial', size=12, bold=True)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font_white = Font(name='Arial', size=11, bold=True, color="FFFFFF")
        sub_header_fill = PatternFill(start_color="B8CCE4", end_color="B8CCE4", fill_type="solid")

        # Color fills for special days
        weekend_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")  # Red-ish for weekends
        mandatory_holiday_fill = PatternFill(start_color="FFD93D", end_color="FFD93D", fill_type="solid")  # Yellow for mandatory holidays
        optional_holiday_fill = PatternFill(start_color="A8E6CF", end_color="A8E6CF", fill_type="solid")  # Light green for optional holidays

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

        # Row 10: Day numbers (1, 2, 3, ..., 31) with color coding
        for day in range(1, days_in_month + 1):
            cell = ws.cell(row=10, column=3 + day)
            cell.value = day
            cell.font = Font(name='Arial', size=10, bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            # Determine the date and apply appropriate color
            current_date = date(year, month, day)

            # Check if it's a holiday first (holidays take precedence)
            if day in holidays:
                holiday_info = holidays[day]
                if holiday_info['is_mandatory']:
                    cell.fill = mandatory_holiday_fill
                    cell.value = f"{day}\n(H)"  # H for Holiday
                else:
                    cell.fill = optional_holiday_fill
                    cell.value = f"{day}\n(OH)"  # OH for Optional Holiday
                # Add comment with holiday name
                cell.comment = f"{holiday_info['name']}"
            # Check if it's a weekend
            elif self.is_weekend(current_date, working_calendar):
                cell.fill = weekend_fill
                cell.value = f"{day}\n(WO)"  # WO for Weekend/Week Off
            else:
                cell.fill = sub_header_fill

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

            # Attendance columns (leave empty for user to fill) with color coding
            for day in range(1, days_in_month + 1):
                cell = ws.cell(row=row_idx, column=3 + day)
                cell.value = ""
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = border

                # Apply same color coding as header
                current_date = date(year, month, day)

                if day in holidays:
                    holiday_info = holidays[day]
                    if holiday_info['is_mandatory']:
                        cell.fill = mandatory_holiday_fill
                    else:
                        cell.fill = optional_holiday_fill
                elif self.is_weekend(current_date, working_calendar):
                    cell.fill = weekend_fill

        # Add attendance codes legend at the bottom of the sheet
        legend_start_row = 10 + len(employees) + 3  # 3 rows gap after employee data

        # Legend title
        legend_title_cell = ws.cell(row=legend_start_row, column=1)
        legend_title_cell.value = "ATTENDANCE CODES REFERENCE"
        legend_title_cell.font = Font(name='Arial', size=12, bold=True, color="FFFFFF")
        legend_title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        legend_title_cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells(start_row=legend_start_row, start_column=1, end_row=legend_start_row, end_column=5)

        # Attendance codes with descriptions
        attendance_codes = [
            ("P", "Present", "Full day work completed"),
            ("A", "Absent", "Absent without approval (unpaid)"),
            ("HD", "Half Day", "Half day present (50% pay)"),
            ("L", "Leave", "Approved paid leave"),
            ("CL", "Casual Leave", "Casual leave (paid)"),
            ("SL", "Sick Leave", "Medical leave (paid)"),
            ("PL", "Privilege Leave", "Earned/privilege leave (paid)"),
            ("LWP", "Leave Without Pay", "Unpaid leave"),
            ("WFH", "Work From Home", "Remote work (counted as present)"),
            ("CO", "Compensatory Off", "Comp off for working on holiday/weekend"),
            ("OD", "On Duty", "Official duty outside office"),
            ("H", "Holiday", "Public/Company holiday (paid) - Auto-marked"),
            ("WO", "Weekly Off", "Weekend day (paid) - Auto-marked"),
        ]

        # Add code headers
        header_row = legend_start_row + 1
        headers = ["Code", "Name", "Description"]
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=header_row, column=col_idx)
            cell.value = header
            cell.font = Font(name='Arial', size=10, bold=True)
            cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

        # Add attendance codes
        for idx, (code, name, description) in enumerate(attendance_codes, start=1):
            row = header_row + idx

            # Code
            code_cell = ws.cell(row=row, column=1)
            code_cell.value = code
            code_cell.font = Font(name='Arial', size=10, bold=True)
            code_cell.alignment = Alignment(horizontal='center', vertical='center')
            code_cell.border = border

            # Name
            name_cell = ws.cell(row=row, column=2)
            name_cell.value = name
            name_cell.font = Font(name='Arial', size=10)
            name_cell.alignment = Alignment(horizontal='left', vertical='center')
            name_cell.border = border

            # Description
            desc_cell = ws.cell(row=row, column=3)
            desc_cell.value = description
            desc_cell.font = Font(name='Arial', size=9)
            desc_cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            desc_cell.border = border

        # Merge description column for better visibility
        ws.merge_cells(start_row=header_row + 1, start_column=3, end_row=header_row + 1, end_column=5)
        for i in range(2, len(attendance_codes) + 1):
            ws.merge_cells(start_row=header_row + i, start_column=3, end_row=header_row + i, end_column=5)

        # Set column widths for legend section
        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 20

        # Add note below legend
        note_row = header_row + len(attendance_codes) + 2
        note_cell = ws.cell(row=note_row, column=1)
        note_cell.value = "NOTE: Codes marked as 'Auto-marked' will be automatically filled by the system for holidays and weekends. You can override them if employee worked on those days."
        note_cell.font = Font(name='Arial', size=9, italic=True)
        note_cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=5)

        # Add instructions sheet
        ws_instructions = wb.create_sheet("Instructions")

        # Count holidays by type
        mandatory_holidays_count = sum(1 for h in holidays.values() if h['is_mandatory'])
        optional_holidays_count = sum(1 for h in holidays.values() if not h['is_mandatory'])

        # Build holiday list for display
        holiday_list = []
        for day, info in sorted(holidays.items()):
            holiday_type = "Mandatory" if info['is_mandatory'] else "Optional"
            holiday_list.append(f"   • {day} - {info['name']} ({holiday_type})")

        instructions = [
            "ATTENDANCE TEMPLATE INSTRUCTIONS",
            "",
            "═══════════════════════════════════════════════════════",
            "COLOR LEGEND",
            "═══════════════════════════════════════════════════════",
            "",
            "🔴 RED CELLS       = Weekends (as per company calendar)",
            "🟡 YELLOW CELLS    = Mandatory Holidays (paid days)",
            "🟢 GREEN CELLS     = Optional Holidays",
            "⬜ GRAY CELLS      = Regular working days",
            "",
            f"NOTE: Weekends and holidays are pre-colored. These days are automatically",
            f"      marked in the system and will be counted as paid days.",
            "",
            "═══════════════════════════════════════════════════════",
            "HOW TO FILL THE TEMPLATE",
            "═══════════════════════════════════════════════════════",
            "",
            "1. Fill in attendance codes ONLY for regular working days (gray cells)",
            "",
            "2. Use the following attendance codes:",
            "   • P   = Present (Full day work)",
            "   • A   = Absent (Unpaid)",
            "   • HD  = Half Day (50% pay)",
            "   • L   = Leave (Approved paid leave)",
            "   • CL  = Casual Leave (Paid)",
            "   • SL  = Sick Leave (Paid)",
            "   • PL  = Privilege Leave (Paid)",
            "   • LWP = Leave Without Pay (Unpaid)",
            "   • WFH = Work From Home (Counted as present)",
            "   • CO  = Compensatory Off",
            "   • OD  = On Duty (Official work outside office)",
            "   • H   = Holiday (Auto-marked by system)",
            "   • WO  = Weekly Off (Auto-marked by system)",
            "",
            "3. For colored cells (weekends/holidays):",
            "   • You can leave them empty - system will auto-mark them",
            "   • OR enter codes if employee worked on weekend/holiday",
            "",
            "4. DO NOT MODIFY:",
            "   • Employee IDs (Column B)",
            "   • Employee Names (Column C)",
            "   • Header rows (Rows 1-10)",
            "   • The template structure",
            "",
            "5. After filling, save and upload through the system",
            "",
            "═══════════════════════════════════════════════════════",
            f"HOLIDAYS FOR {datetime(year, month, 1).strftime('%B %Y').upper()}",
            "═══════════════════════════════════════════════════════",
            "",
        ]

        if holiday_list:
            instructions.extend(holiday_list)
        else:
            instructions.append("   No holidays configured for this month")

        instructions.extend([
            "",
            "═══════════════════════════════════════════════════════",
            "TEMPLATE INFORMATION",
            "═══════════════════════════════════════════════════════",
            "",
            f"Template generated for: {datetime(year, month, 1).strftime('%B %Y')}",
            f"Number of employees: {len(employees)}",
            f"Total days in month: {days_in_month}",
            f"Mandatory holidays: {mandatory_holidays_count}",
            f"Optional holidays: {optional_holidays_count}",
            "",
            "═══════════════════════════════════════════════════════",
            "SYSTEM VALIDATION",
            "═══════════════════════════════════════════════════════",
            "",
            "The system will automatically validate:",
            "  ✓ All employee IDs exist in the database",
            "  ✓ Attendance codes are valid",
            "  ✓ Dates are within the specified month",
            "  ✓ Weekends and holidays are properly marked",
            "",
            "If there are errors, you'll receive detailed error messages.",
        ])

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
            "valid_codes": ["P", "A", "HD", "L", "CL", "SL", "PL", "LWP", "WFH", "CO", "OD", "H", "WO"]
        }
