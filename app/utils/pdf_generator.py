from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional, List


class PDFGenerator:
    """Generate professional PDF documents for payslips and reports"""

    @staticmethod
    def generate_payslip(
        wage_statement: Dict[str, Any],
        employee_details: Dict[str, Any],
        tenant_details: Dict[str, Any],
        logo_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate professional payslip PDF

        Args:
            wage_statement: Wage calculation data with all components
            employee_details: Employee information (name, code, designation, etc.)
            tenant_details: Company/organization details
            logo_path: Optional path to company logo

        Returns:
            BytesIO object containing PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Container for the 'Flowable' objects
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=TA_CENTER,
            spaceAfter=10
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=6
        )

        normal_style = styles['Normal']

        # Add logo if provided
        if logo_path:
            try:
                logo = Image(logo_path, width=2*inch, height=0.8*inch)
                elements.append(logo)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass  # Skip logo if file not found

        # Company Header
        company_name = Paragraph(
            f"<b>{tenant_details.get('name', 'Company Name')}</b>",
            title_style
        )
        elements.append(company_name)

        company_address = Paragraph(
            tenant_details.get('address', 'Company Address'),
            ParagraphStyle('center', parent=normal_style, alignment=TA_CENTER)
        )
        elements.append(company_address)
        elements.append(Spacer(1, 0.3*inch))

        # Payslip Title
        month_year = f"{wage_statement.get('month', 1):02d}/{wage_statement.get('year', 2025)}"
        payslip_title = Paragraph(
            f"<b>SALARY SLIP - {month_year}</b>",
            heading_style
        )
        elements.append(payslip_title)
        elements.append(Spacer(1, 0.2*inch))

        # Employee Details Table
        employee_data = [
            ['Employee Code:', employee_details.get('employee_code', 'N/A'),
             'Employee Name:', f"{employee_details.get('first_name', '')} {employee_details.get('last_name', '')}"],
            ['Designation:', employee_details.get('designation', 'N/A'),
             'Department:', employee_details.get('department', 'N/A')],
            ['Date of Joining:', employee_details.get('date_of_joining', 'N/A'),
             'Bank A/C:', employee_details.get('bank_account', 'N/A')],
            ['PAN:', employee_details.get('pan', 'N/A'),
             'PF Number:', employee_details.get('pf_number', 'N/A')],
        ]

        employee_table = Table(employee_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(employee_table)
        elements.append(Spacer(1, 0.3*inch))

        # Attendance Summary
        attendance_data = [
            ['Total Days', 'Days Worked', 'Days Absent', 'Half Days', 'Effective Days'],
            [
                str(wage_statement.get('total_days', 30)),
                str(wage_statement.get('days_worked', 0)),
                str(wage_statement.get('days_absent', 0)),
                str(wage_statement.get('days_half_day', 0)),
                f"{wage_statement.get('effective_days', 0):.1f}"
            ]
        ]

        attendance_table = Table(attendance_data, colWidths=[1.4*inch]*5)
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(attendance_table)
        elements.append(Spacer(1, 0.3*inch))

        # Earnings and Deductions Table
        salary_data = [
            ['EARNINGS', 'AMOUNT (₹)', 'DEDUCTIONS', 'AMOUNT (₹)']
        ]

        # Earnings rows
        earnings_items = [
            ('Basic Salary', wage_statement.get('basic_salary', 0)),
            ('HRA', wage_statement.get('hra', 0)),
            ('Conveyance Allowance', wage_statement.get('conveyance_allowance', 0)),
            ('Medical Allowance', wage_statement.get('medical_allowance', 0)),
            ('Special Allowance', wage_statement.get('special_allowance', 0)),
            ('Other Allowances', wage_statement.get('other_allowances', 0)),
            ('Overtime', wage_statement.get('overtime_amount', 0)),
        ]

        deductions_items = [
            ('PF (Employee)', wage_statement.get('pf_employee', 0)),
            ('ESI (Employee)', wage_statement.get('esi_employee', 0)),
            ('Professional Tax', wage_statement.get('professional_tax', 0)),
            ('TDS', wage_statement.get('tds', 0)),
            ('Loan Deduction', wage_statement.get('loan_deduction', 0)),
            ('Advance Deduction', wage_statement.get('advance_deduction', 0)),
            ('Other Deductions', wage_statement.get('other_deductions', 0)),
        ]

        # Combine earnings and deductions side by side
        max_rows = max(len(earnings_items), len(deductions_items))

        for i in range(max_rows):
            row = []

            # Earnings
            if i < len(earnings_items):
                row.extend([earnings_items[i][0], f"{earnings_items[i][1]:,.2f}"])
            else:
                row.extend(['', ''])

            # Deductions
            if i < len(deductions_items):
                row.extend([deductions_items[i][0], f"{deductions_items[i][1]:,.2f}"])
            else:
                row.extend(['', ''])

            salary_data.append(row)

        # Totals row
        salary_data.append([
            'GROSS SALARY',
            f"{wage_statement.get('gross_salary', 0):,.2f}",
            'TOTAL DEDUCTIONS',
            f"{wage_statement.get('total_deductions', 0):,.2f}"
        ])

        # Net Salary row (spans all columns)
        net_salary = wage_statement.get('net_salary', 0)
        salary_data.append([
            'NET SALARY (Take Home)',
            '',
            '',
            f"₹ {net_salary:,.2f}"
        ])

        salary_table = Table(salary_data, colWidths=[2.5*inch, 1*inch, 2.5*inch, 1*inch])
        salary_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Body rows
            ('FONTSIZE', (0, 1), (-1, -3), 9),
            ('ALIGN', (1, 1), (1, -3), 'RIGHT'),
            ('ALIGN', (3, 1), (3, -3), 'RIGHT'),
            ('GRID', (0, 0), (-1, -3), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),

            # Totals row
            ('BACKGROUND', (0, -2), (-1, -2), colors.HexColor('#dbeafe')),
            ('FONTNAME', (0, -2), (-1, -2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -2), (-1, -2), 10),
            ('ALIGN', (1, -2), (1, -2), 'RIGHT'),
            ('ALIGN', (3, -2), (3, -2), 'RIGHT'),

            # Net salary row
            ('SPAN', (0, -1), (2, -1)),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('ALIGN', (0, -1), (0, -1), 'LEFT'),
            ('ALIGN', (3, -1), (3, -1), 'RIGHT'),
        ]))
        elements.append(salary_table)
        elements.append(Spacer(1, 0.3*inch))

        # Employer Contributions (Optional info box)
        employer_data = [
            ['Employer Contributions', ''],
            ['PF (Employer)', f"₹ {wage_statement.get('pf_employer', 0):,.2f}"],
            ['ESI (Employer)', f"₹ {wage_statement.get('esi_employer', 0):,.2f}"],
        ]

        employer_table = Table(employer_data, colWidths=[5*inch, 2*inch])
        employer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0e7ff')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(employer_table)
        elements.append(Spacer(1, 0.4*inch))

        # Footer
        footer_text = Paragraph(
            "<i>This is a system-generated payslip and does not require a signature.</i>",
            ParagraphStyle('footer', parent=normal_style, fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
        )
        elements.append(footer_text)

        generated_on = Paragraph(
            f"<i>Generated on: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}</i>",
            ParagraphStyle('footer2', parent=normal_style, fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
        )
        elements.append(generated_on)

        # Build PDF
        doc.build(elements)

        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_salary_register(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        tenant_details: Dict[str, Any]
    ) -> BytesIO:
        """
        Generate consolidated salary register for all employees

        Args:
            wage_statements: List of wage statement dicts
            month: Month number
            year: Year
            tenant_details: Company details

        Returns:
            BytesIO object containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.3*inch,
            leftMargin=0.3*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(
            f"<b>SALARY REGISTER - {month:02d}/{year}</b>",
            ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER)
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Company name
        company = Paragraph(
            tenant_details.get('name', 'Company Name'),
            ParagraphStyle('company', parent=styles['Normal'], alignment=TA_CENTER)
        )
        elements.append(company)
        elements.append(Spacer(1, 0.3*inch))

        # Register table
        register_data = [
            ['S.No', 'Emp Code', 'Name', 'Days', 'Gross', 'PF', 'ESI', 'PT', 'TDS', 'Other', 'Net Salary']
        ]

        total_gross = 0
        total_pf = 0
        total_esi = 0
        total_pt = 0
        total_tds = 0
        total_other = 0
        total_net = 0

        for idx, ws in enumerate(wage_statements, 1):
            gross = ws.get('gross_salary', 0)
            pf = ws.get('pf_employee', 0)
            esi = ws.get('esi_employee', 0)
            pt = ws.get('professional_tax', 0)
            tds = ws.get('tds', 0)
            other = ws.get('loan_deduction', 0) + ws.get('advance_deduction', 0) + ws.get('other_deductions', 0)
            net = ws.get('net_salary', 0)

            register_data.append([
                str(idx),
                ws.get('employee_code', ''),
                ws.get('employee_name', ''),
                f"{ws.get('effective_days', 0):.1f}",
                f"{gross:,.0f}",
                f"{pf:,.0f}",
                f"{esi:,.0f}",
                f"{pt:,.0f}",
                f"{tds:,.0f}",
                f"{other:,.0f}",
                f"{net:,.0f}"
            ])

            total_gross += gross
            total_pf += pf
            total_esi += esi
            total_pt += pt
            total_tds += tds
            total_other += other
            total_net += net

        # Totals row
        register_data.append([
            '', '', 'TOTAL', '',
            f"{total_gross:,.0f}",
            f"{total_pf:,.0f}",
            f"{total_esi:,.0f}",
            f"{total_pt:,.0f}",
            f"{total_tds:,.0f}",
            f"{total_other:,.0f}",
            f"{total_net:,.0f}"
        ])

        register_table = Table(register_data, colWidths=[0.4*inch, 0.8*inch, 1.5*inch, 0.5*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.5*inch, 0.6*inch, 0.6*inch, 1*inch])
        register_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -2), 7),
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dbeafe')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(register_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer
