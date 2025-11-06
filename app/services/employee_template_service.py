"""
Service for generating employee template Excel files

This service creates a downloadable Excel template that employers can use
to fill in employee data and upload back to the system.
"""

from typing import List, Optional
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from sqlalchemy.orm import Session
import os


class EmployeeTemplateService:
    """Service for generating employee Excel templates"""

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def generate_template(self, company_name: str = "Company Name") -> str:
        """
        Generate an employee template Excel file

        Args:
            company_name: Name of the company

        Returns:
            Path to the generated Excel file
        """
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Employee Database"

        # Define styles
        header_font = Font(name='Arial', size=11, bold=True)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font_white = Font(name='Arial', size=11, bold=True, color="FFFFFF")
        sub_header_fill = PatternFill(start_color="B8CCE4", end_color="B8CCE4", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Define column headers based on Employee Database sheet structure
        headers = [
            'Serial No',
            'Service Status',
            'Principal Employer',
            'Business Address Line 1',
            'Business Address Line 2',
            'Business Address Line 3',
            'City/Town/Village',
            'PIN Code',
            'Employee ID',
            'Employee Name',
            'Father/Husband Name',
            'Date of Birth',
            'Gender',
            'Marital Status',
            'Date of Joining',
            'Date of Exit',
            'PAN',
            'Aadhaar',
            'UAN',
            'ESIC Number',
            'Mobile Number',
            'Email Address',
            'Address Line 1',
            'Address Line 2',
            'Address Line 3',
            'City/Town/Village',
            'State',
            'PIN Code',
            'Bank Name',
            'Bank Account Number',
            'Bank IFSC Code',
            'Bank Branch',
            'Designation',
            'Department',
            'Location',
            'Employee Category',
            'Employment Type',
            'PF Applicable',
            'ESIC Applicable',
            'LWF Applicable',
            'PT Applicable',
            'Basic Salary',
            'HRA',
            'Conveyance Allowance',
            'Medical Allowance',
            'Special Allowance',
            'Other Allowance',
            'Gross Salary',
            'PF Employee Contribution',
            'PF Employer Contribution',
            'ESIC Employee Contribution',
            'ESIC Employer Contribution',
            'Professional Tax',
            'Total Deductions',
            'Net Salary',
            'CTC',
            'Remarks'
        ]

        # Row 9: Column headers
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=9, column=col_idx)
            cell.value = header
            cell.font = header_font_white
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = border

        # Row 10: Column numbers
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=10, column=col_idx)
            cell.value = col_idx
            cell.font = Font(name='Arial', size=10, bold=True)
            cell.fill = sub_header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

        # Add sample row (Row 11) with placeholder data
        sample_data = [
            1,  # Serial No
            'Active',  # Service Status
            'Company Name',  # Principal Employer
            'Address Line 1',  # Business Address Line 1
            'Address Line 2',  # Business Address Line 2
            '',  # Business Address Line 3
            'City',  # City/Town/Village
            '123456',  # PIN Code
            'EMP001',  # Employee ID
            'John Doe',  # Employee Name
            'Father Name',  # Father/Husband Name
            '1990-01-01',  # Date of Birth
            'Male',  # Gender
            'Married',  # Marital Status
            '2024-01-01',  # Date of Joining
            '',  # Date of Exit
            'ABCDE1234F',  # PAN
            '123456789012',  # Aadhaar
            '123456789012',  # UAN
            '1234567890',  # ESIC Number
            '9876543210',  # Mobile Number
            'john.doe@example.com',  # Email Address
            'Residence Address Line 1',  # Address Line 1
            'Residence Address Line 2',  # Address Line 2
            '',  # Address Line 3
            'City',  # City/Town/Village
            'State',  # State
            '123456',  # PIN Code
            'Bank Name',  # Bank Name
            '1234567890',  # Bank Account Number
            'BANK0001234',  # Bank IFSC Code
            'Branch Name',  # Bank Branch
            'Software Engineer',  # Designation
            'IT',  # Department
            'Head Office',  # Location
            'Full Time',  # Employee Category
            'Permanent',  # Employment Type
            'Yes',  # PF Applicable
            'Yes',  # ESIC Applicable
            'No',  # LWF Applicable
            'Yes',  # PT Applicable
            15000,  # Basic Salary
            7500,  # HRA
            1600,  # Conveyance Allowance
            1250,  # Medical Allowance
            4650,  # Special Allowance
            0,  # Other Allowance
            30000,  # Gross Salary
            1800,  # PF Employee Contribution
            1800,  # PF Employer Contribution
            450,  # ESIC Employee Contribution
            1050,  # ESIC Employer Contribution
            200,  # Professional Tax
            2450,  # Total Deductions
            27550,  # Net Salary
            360000,  # CTC
            'Sample employee data'  # Remarks
        ]

        for col_idx, value in enumerate(sample_data, start=1):
            cell = ws.cell(row=11, column=col_idx)
            cell.value = value
            cell.alignment = Alignment(horizontal='left' if isinstance(value, str) else 'center', vertical='center')
            cell.border = border

        # Add instructions sheet
        ws_instructions = wb.create_sheet("Instructions")

        instructions = [
            "EMPLOYEE TEMPLATE INSTRUCTIONS",
            "",
            "How to fill the employee template:",
            "",
            "1. Fill in the employee details starting from Row 11",
            "",
            "2. Required fields (marked with *):",
            "   • Employee ID (Column 9) - Unique identifier for each employee",
            "   • Employee Name (Column 10) - Full name of the employee",
            "   • Date of Birth (Column 12) - Format: YYYY-MM-DD",
            "   • Gender (Column 13) - Male/Female/Other",
            "   • Date of Joining (Column 15) - Format: YYYY-MM-DD",
            "",
            "3. Optional but recommended fields:",
            "   • PAN (Column 17) - 10 character PAN number",
            "   • Aadhaar (Column 18) - 12 digit Aadhaar number",
            "   • UAN (Column 19) - 12 digit UAN number",
            "   • Mobile Number (Column 21) - 10 digit mobile number",
            "   • Email Address (Column 22) - Valid email address",
            "",
            "4. Salary fields (Columns 41-55):",
            "   • Basic Salary - Should be at least 50% of Gross Salary",
            "   • Gross Salary - Sum of all allowances",
            "   • Deductions - PF, ESIC, PT as applicable",
            "   • Net Salary - Gross Salary - Total Deductions",
            "",
            "5. Date format: Use YYYY-MM-DD (e.g., 2024-01-15)",
            "",
            "6. Boolean fields (Yes/No):",
            "   • PF Applicable (Column 38)",
            "   • ESIC Applicable (Column 39)",
            "   • LWF Applicable (Column 40)",
            "   • PT Applicable (Column 41)",
            "",
            "7. Do NOT modify:",
            "   • Row 9 (Column Headers)",
            "   • Row 10 (Column Numbers)",
            "   • The structure of the template",
            "",
            "8. After filling, save the file and upload it through the system",
            "",
            "9. The system will validate:",
            "   • All required fields are filled",
            "   • Employee IDs are unique",
            "   • Date formats are correct",
            "   • Email and mobile number formats are valid",
            "   • PAN and Aadhaar formats are correct",
            "",
            "10. If there are any errors during upload, the system will provide detailed error messages",
            "",
            f"Template generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]

        for row_idx, instruction in enumerate(instructions, start=1):
            ws_instructions[f'A{row_idx}'] = instruction
            if row_idx == 1:
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=14, bold=True)
            elif "•" in instruction or instruction.endswith(":"):
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=11, bold=True)
            else:
                ws_instructions[f'A{row_idx}'].font = Font(name='Arial', size=10)

        # Set column widths for Employee Database sheet
        column_widths = [
            8,   # Serial No
            12,  # Service Status
            20,  # Principal Employer
            25,  # Business Address Line 1
            25,  # Business Address Line 2
            25,  # Business Address Line 3
            15,  # City/Town/Village
            10,  # PIN Code
            12,  # Employee ID
            20,  # Employee Name
            20,  # Father/Husband Name
            12,  # Date of Birth
            10,  # Gender
            12,  # Marital Status
            12,  # Date of Joining
            12,  # Date of Exit
            12,  # PAN
            15,  # Aadhaar
            15,  # UAN
            12,  # ESIC Number
            12,  # Mobile Number
            25,  # Email Address
            25,  # Address Line 1
            25,  # Address Line 2
            25,  # Address Line 3
            15,  # City/Town/Village
            12,  # State
            10,  # PIN Code
            20,  # Bank Name
            18,  # Bank Account Number
            15,  # Bank IFSC Code
            15,  # Bank Branch
            20,  # Designation
            15,  # Department
            15,  # Location
            15,  # Employee Category
            15,  # Employment Type
            12,  # PF Applicable
            12,  # ESIC Applicable
            12,  # LWF Applicable
            12,  # PT Applicable
            12,  # Basic Salary
            10,  # HRA
            15,  # Conveyance Allowance
            15,  # Medical Allowance
            15,  # Special Allowance
            15,  # Other Allowance
            12,  # Gross Salary
            18,  # PF Employee Contribution
            18,  # PF Employer Contribution
            20,  # ESIC Employee Contribution
            20,  # ESIC Employer Contribution
            15,  # Professional Tax
            15,  # Total Deductions
            12,  # Net Salary
            12,  # CTC
            20   # Remarks
        ]

        for idx, width in enumerate(column_widths, start=1):
            col_letter = get_column_letter(idx)
            ws.column_dimensions[col_letter].width = width

        ws_instructions.column_dimensions['A'].width = 100

        # Freeze panes at Row 11 (after headers)
        ws.freeze_panes = 'A11'

        # Save the file
        template_dir = "uploads/templates"
        os.makedirs(template_dir, exist_ok=True)

        filename = f"employee_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join(template_dir, filename)

        wb.save(file_path)
        wb.close()

        return file_path

    def get_template_info(self) -> dict:
        """
        Get information about what the template will contain

        Returns:
            Dictionary with template information
        """
        return {
            "template_type": "employee",
            "total_columns": 56,
            "required_fields": [
                "Employee ID",
                "Employee Name",
                "Date of Birth",
                "Gender",
                "Date of Joining"
            ],
            "optional_fields": [
                "PAN", "Aadhaar", "UAN", "ESIC Number",
                "Mobile Number", "Email Address",
                "Bank Details", "Salary Components"
            ],
            "date_format": "YYYY-MM-DD",
            "boolean_format": "Yes/No"
        }
