"""
Service for generating wage data Excel templates
"""

from typing import List, Optional, Dict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from sqlalchemy.orm import Session
import os

from app.models.employee import Employee
from app.models.tenant import Tenant


class WageTemplateService:
    """Service for generating wage Excel templates"""

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def generate_template(
        self, company_name: str = "Company Name", company_address: str = "Company Address"
    ) -> str:
        """
        Generate a wage data template Excel file

        Args:
            company_name: Name of the company
            company_address: Address of the company

        Returns:
            Path to the generated Excel file
        """
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Wage Data"

        # Get employees for this tenant
        employees = self.db.query(Employee).filter(
            Employee.tenant_id == self.tenant_id,
            Employee.status == "active"
        ).order_by(Employee.employee_code).all()

        # Define styles
        header_font = Font(name='Arial', size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Row 1: Title
        ws['A1'] = "WAGES STATEMENT"
        ws['A1'].font = Font(name='Arial', size=14, bold=True)
        ws.merge_cells('A1:E1')

        # Row 3: Company Name
        ws['A3'] = "Name and address of Employer:"
        ws['A3'].font = Font(name='Arial', size=10, bold=True)
        ws['F3'] = company_name
        ws['F3'].font = Font(name='Arial', size=10)

        # Row 5: Column headers
        headers = [
            'S.No', 
            'Employee Code', 
            'Employee Name', 
            'Basic Salary', 
            'HRA', 
            'Conveyance', 
            'Special Allowance', 
            'Other Allowance',
            'PF Employee',
            'PF Employer',
            'ESI Employee',
            'ESI Employer',
            'PT',
            'TDS',
            'Net Salary'
        ]

        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=5, column=col_idx)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

        # Data rows: Add employees
        for idx, employee in enumerate(employees, start=1):
            row_idx = 5 + idx

            # S.No
            cell = ws.cell(row=row_idx, column=1)
            cell.value = idx
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            # Employee Code
            cell = ws.cell(row=row_idx, column=2)
            cell.value = employee.employee_code
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

            # Employee Name
            cell = ws.cell(row=row_idx, column=3)
            cell.value = f"{employee.first_name} {employee.last_name}"
            cell.alignment = Alignment(horizontal='left', vertical='center')
            cell.border = border

            # Pre-fill current salary details if available
            salary = employee.salary_details
            
            # Basic Salary
            cell = ws.cell(row=row_idx, column=4)
            cell.value = float(salary.basic_salary) if salary else 0
            cell.border = border

            # HRA
            cell = ws.cell(row=row_idx, column=5)
            cell.value = float(salary.hra) if salary else 0
            cell.border = border

            # Conveyance
            cell = ws.cell(row=row_idx, column=6)
            cell.value = float(salary.conveyance_allowance) if salary else 0
            cell.border = border

            # Special Allowance
            cell = ws.cell(row=row_idx, column=7)
            cell.value = float(salary.special_allowance) if salary else 0
            cell.border = border

            # Other Allowance
            cell = ws.cell(row=row_idx, column=8)
            cell.value = float(salary.other_allowance) if salary else 0
            cell.border = border

            # PF Employee
            cell = ws.cell(row=row_idx, column=9)
            cell.value = float(salary.pf_employee) if salary else 0
            cell.border = border

            # PF Employer
            cell = ws.cell(row=row_idx, column=10)
            cell.value = float(salary.pf_employer) if salary else 0
            cell.border = border

            # ESI Employee
            cell = ws.cell(row=row_idx, column=11)
            cell.value = float(salary.esic_employee) if salary else 0
            cell.border = border

            # ESI Employer
            cell = ws.cell(row=row_idx, column=12)
            cell.value = float(salary.esic_employer) if salary else 0
            cell.border = border

            # PT
            cell = ws.cell(row=row_idx, column=13)
            cell.value = float(salary.professional_tax) if salary else 0
            cell.border = border

            # TDS
            cell = ws.cell(row=row_idx, column=14)
            cell.value = float(salary.tds) if salary else 0
            cell.border = border

            # Net Salary
            cell = ws.cell(row=row_idx, column=15)
            cell.value = float(salary.net_salary) if salary else 0
            cell.border = border

        # Set column widths
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 30
        for i in range(4, 16):
            ws.column_dimensions[get_column_letter(i)].width = 15

        # Save the file
        template_dir = "uploads/templates"
        os.makedirs(template_dir, exist_ok=True)

        filename = f"wage_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join(template_dir, filename)

        wb.save(file_path)
        wb.close()

        return file_path
