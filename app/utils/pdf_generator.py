from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional, List
import calendar


def number_to_words(num):
    """Convert number to words for Indian currency"""
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
            'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
            'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

    if num == 0:
        return 'Zero'

    def convert_less_than_thousand(n):
        if n < 20:
            return ones[n]
        elif n < 100:
            return tens[n // 10] + ('' if n % 10 == 0 else '-' + ones[n % 10])
        else:
            return ones[n // 100] + ' Hundred' + ('' if n % 100 == 0 else ' ' + convert_less_than_thousand(n % 100))

    def convert_indian(n):
        if n < 1000:
            return convert_less_than_thousand(n)
        elif n < 100000:
            return convert_less_than_thousand(n // 1000) + ' Thousand' + ('' if n % 1000 == 0 else ' ' + convert_less_than_thousand(n % 1000))
        elif n < 10000000:
            return convert_less_than_thousand(n // 100000) + ' Lakh' + ('' if n % 100000 == 0 else ' ' + convert_indian(n % 100000))
        else:
            return convert_less_than_thousand(n // 10000000) + ' Crore' + ('' if n % 10000000 == 0 else ' ' + convert_indian(n % 10000000))

    # Handle rupees and paise
    rupees = int(num)
    paise = int(round((num - rupees) * 100))

    result = convert_indian(rupees) + ' Rupees'
    if paise > 0:
        result += ' and ' + convert_indian(paise) + ' Paise'
    result += ' Only'

    return result


def create_logo_placeholder(width=60, height=40):
    """Create a simple placeholder logo drawing"""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#f5f5f5'), strokeColor=colors.black, strokeWidth=0.5))
    d.add(String(width/2, height/2 - 5, "LOGO", fontSize=10, fillColor=colors.black, textAnchor='middle'))
    return d


class PDFGenerator:
    """Generate professional PDF documents for payslips and reports"""

    # Color scheme - only two colors
    DARK_BLUE = colors.HexColor('#003366')
    LIGHT_GRAY = colors.HexColor('#f5f5f5')
    WHITE = colors.white
    BLACK = colors.black

    @staticmethod
    def get_month_name(month: int) -> str:
        """Get month name from month number"""
        return calendar.month_name[month]

    @staticmethod
    def generate_payslip(
        wage_statement: Dict[str, Any],
        employee_details: Dict[str, Any],
        tenant_details: Dict[str, Any],
        leave_details: Optional[Dict[str, Any]] = None,
        logo_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate professional payslip PDF matching industry standard layout

        Args:
            wage_statement: Wage calculation data with all components
            employee_details: Employee information (name, code, designation, etc.)
            tenant_details: Company/organization details
            leave_details: Leave balance information (accumulated, availed, balance)
            logo_path: Optional path to company logo

        Returns:
            BytesIO object containing PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )

        elements = []
        styles = getSampleStyleSheet()

        # Get month and year
        month = wage_statement.get('month', 1)
        year = wage_statement.get('year', 2026)
        month_name = PDFGenerator.get_month_name(month)

        # Calculate days in month
        days_in_month = calendar.monthrange(year, month)[1]
        days_payable = wage_statement.get('present_days', 0) + wage_statement.get('leave_days', 0)

        # ========================
        # ROW 1: LOGO + COMPANY NAME (same row)
        # ========================
        company_name = tenant_details.get('name', 'Company Name')

        # Create logo or placeholder
        if logo_path:
            try:
                logo = Image(logo_path, width=60, height=40)
            except:
                logo = create_logo_placeholder(60, 40)
        else:
            logo = create_logo_placeholder(60, 40)

        company_style = ParagraphStyle(
            'CompanyName',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=PDFGenerator.BLACK,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        header_data = [[logo, Paragraph(f"<b>{company_name}</b>", company_style)]]
        header_table = Table(header_data, colWidths=[1*inch, 6.5*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)

        # ========================
        # ROW 2: ADDRESS (centered)
        # ========================
        company_address = tenant_details.get('address', 'Company Address')
        address_style = ParagraphStyle(
            'Address',
            parent=styles['Normal'],
            fontSize=10,
            textColor=PDFGenerator.BLACK,
            alignment=TA_CENTER
        )
        address_table = Table([[Paragraph(company_address, address_style)]], colWidths=[7.5*inch])
        address_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(address_table)

        # ========================
        # ROW 3: PAYSLIP TITLE (light gray background, bold black text)
        # ========================
        title_style = ParagraphStyle(
            'PayslipTitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=PDFGenerator.BLACK,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        title_text = f"Payslip For the Month of {month_name} {year}"
        title_table = Table([[Paragraph(f"<b>{title_text}</b>", title_style)]], colWidths=[7.5*inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PDFGenerator.LIGHT_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, PDFGenerator.BLACK),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(title_table)

        elements.append(Spacer(1, 0.15*inch))

        # ========================
        # EMPLOYEE INFO: 2-column bordered table
        # ========================
        # Get employee details
        emp_code = employee_details.get('employee_code', 'N/A')
        emp_name = f"{employee_details.get('first_name', '')} {employee_details.get('middle_name', '')} {employee_details.get('last_name', '')}".strip()
        emp_name = ' '.join(emp_name.split())  # Remove extra spaces
        department = employee_details.get('department', 'N/A')
        designation = employee_details.get('designation', 'N/A')

        # Bank details
        bank_name = employee_details.get('bank_name', 'N/A')
        if employee_details.get('branch_name'):
            bank_name = f"{bank_name}, {employee_details.get('branch_name')}"
        account_no = employee_details.get('bank_account', 'N/A')

        # Statutory details
        pan_card = employee_details.get('pan', 'N/A')
        uan_no = employee_details.get('uan_number', employee_details.get('pf_number', ''))
        esi_no = employee_details.get('esi_number', '')

        # CTC
        ctc_monthly = employee_details.get('ctc', wage_statement.get('total_earnings', 0))

        # Create 2-column employee info table
        emp_info_data = [
            ['Employee ID', emp_code, 'Bank Name', bank_name],
            ['Employee Name', emp_name, 'Account No.', account_no],
            ['Department', department, 'PAN Card No.', pan_card],
            ['Designation', designation, 'UAN No.', uan_no if uan_no else 'N/A'],
            ['Days in Month', str(days_in_month), 'ESI No.', esi_no if esi_no else 'N/A'],
            ['Days Payable', str(days_payable), 'CTC per Month', f"Rs. {float(ctc_monthly):,.0f}"],
        ]

        emp_table = Table(emp_info_data, colWidths=[1.4*inch, 2.2*inch, 1.4*inch, 2.5*inch])
        emp_table.setStyle(TableStyle([
            # Alternating row colors
            ('BACKGROUND', (0, 0), (-1, 0), PDFGenerator.LIGHT_GRAY),
            ('BACKGROUND', (0, 2), (-1, 2), PDFGenerator.LIGHT_GRAY),
            ('BACKGROUND', (0, 4), (-1, 4), PDFGenerator.LIGHT_GRAY),
            # Bold labels
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Borders
            ('BOX', (0, 0), (-1, -1), 1, PDFGenerator.BLACK),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, PDFGenerator.BLACK),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(emp_table)

        elements.append(Spacer(1, 0.1*inch))

        # ========================
        # LEAVES ROW: single row with 3 cells
        # ========================
        if leave_details:
            total_leaves = leave_details.get('total_accumulated', 15)
            leaves_availed = leave_details.get('leaves_availed', 0)
            balance_leaves = leave_details.get('balance_leaves', total_leaves - leaves_availed)
        else:
            total_leaves = 15
            leaves_availed = wage_statement.get('leave_days', 0)
            balance_leaves = total_leaves - leaves_availed

        leave_data = [[
            f"Total Leaves Accumulated: {int(total_leaves)}",
            f"Leaves Availed: {int(leaves_availed)}",
            f"Balance Leaves: {int(balance_leaves)}"
        ]]

        leave_table = Table(leave_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        leave_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PDFGenerator.LIGHT_GRAY),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, PDFGenerator.BLACK),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, PDFGenerator.BLACK),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(leave_table)

        elements.append(Spacer(1, 0.1*inch))

        # ========================
        # EARNINGS & DEDUCTIONS: side-by-side table
        # ========================
        # Get earnings breakdown
        earnings_breakdown = wage_statement.get('earnings_breakdown', {})
        deductions_breakdown = wage_statement.get('deductions_breakdown', {})

        # Standard earnings
        basic_salary = float(wage_statement.get('basic_salary', 0))
        hra = float(earnings_breakdown.get('hra', 0))
        conveyance = float(earnings_breakdown.get('conveyance_allowance', 0))
        medical = float(earnings_breakdown.get('medical_allowance', 0))
        special = float(earnings_breakdown.get('special_allowance', 0))
        other_allowance = float(earnings_breakdown.get('other_allowance', 0))

        # Calculate earned amounts based on days payable
        attendance_factor = days_payable / days_in_month if days_in_month > 0 else 1

        earned_basic = basic_salary * attendance_factor
        earned_hra = hra * attendance_factor
        earned_conveyance = conveyance * attendance_factor
        earned_medical = medical * attendance_factor
        earned_special = special * attendance_factor
        earned_other = other_allowance * attendance_factor

        gross_salary = basic_salary + hra + conveyance + medical + special + other_allowance
        earned_gross = earned_basic + earned_hra + earned_conveyance + earned_medical + earned_special + earned_other

        # Deductions
        epf_contribution = float(deductions_breakdown.get('pf_employee', 0))
        esi_contribution = float(deductions_breakdown.get('esi_employee', 0))
        pt = float(deductions_breakdown.get('professional_tax', 0))
        tds = float(deductions_breakdown.get('tds', 0))
        advance = float(deductions_breakdown.get('advance_deduction', 0))
        other_deductions = float(deductions_breakdown.get('other_deductions', 0) +
                                 deductions_breakdown.get('loan_deduction', 0))

        total_deductions = epf_contribution + esi_contribution + pt + tds + advance + other_deductions

        # Header row
        salary_data = [
            ['EARNINGS', 'Actual Amount (Rs.)', 'Earned Amount (Rs.)', 'DEDUCTIONS', 'Amount (Rs.)']
        ]

        # Data rows
        salary_rows = [
            ['Basic Salary', f"{basic_salary:,.0f}", f"{earned_basic:,.0f}", 'EPF Contribution', f"{epf_contribution:,.0f}"],
            ['HRA', f"{hra:,.0f}", f"{earned_hra:,.0f}", 'ESI Contribution', f"{esi_contribution:,.0f}"],
            ['Conveyance Allowance', f"{conveyance:,.0f}", f"{earned_conveyance:,.0f}", 'Professional Tax', f"{pt:,.0f}"],
            ['Medical Allowance', f"{medical:,.0f}", f"{earned_medical:,.0f}", 'TDS', f"{tds:,.0f}"],
            ['Special Allowance', f"{special:,.0f}", f"{earned_special:,.0f}", 'Advance', f"{advance:,.0f}"],
            ['Other Allowance', f"{other_allowance:,.0f}", f"{earned_other:,.0f}", 'Other Deductions', f"{other_deductions:,.0f}"],
        ]

        # Bottom totals row
        totals_row = ['Gross Salary', f"{gross_salary:,.0f}", f"{earned_gross:,.0f}", 'Total Deductions', f"{total_deductions:,.0f}"]

        salary_data.extend(salary_rows)
        salary_data.append(totals_row)

        salary_table = Table(salary_data, colWidths=[2.0*inch, 1.3*inch, 1.3*inch, 1.6*inch, 1.3*inch])

        # Build style for salary table - light gray labels, white values, bold black text only
        salary_style = [
            # Header row - light gray, bold black
            ('BACKGROUND', (0, 0), (-1, 0), PDFGenerator.LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, 0), PDFGenerator.BLACK),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Label columns (component names) - light gray bg
            ('BACKGROUND', (0, 1), (0, -2), PDFGenerator.LIGHT_GRAY),
            ('BACKGROUND', (3, 1), (3, -2), PDFGenerator.LIGHT_GRAY),

            # Value columns - white bg
            ('BACKGROUND', (1, 1), (2, -2), PDFGenerator.WHITE),
            ('BACKGROUND', (4, 1), (4, -2), PDFGenerator.WHITE),

            # Totals row - light gray, bold black
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), PDFGenerator.LIGHT_GRAY),
            ('TEXTCOLOR', (0, -1), (-1, -1), PDFGenerator.BLACK),

            # Text alignment
            ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Borders
            ('BOX', (0, 0), (-1, -1), 1, PDFGenerator.BLACK),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, PDFGenerator.BLACK),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]

        salary_table.setStyle(TableStyle(salary_style))
        elements.append(salary_table)

        elements.append(Spacer(1, 0.1*inch))

        # ========================
        # NET SALARY + IN WORDS: one unified 2-row table
        # ========================
        net_salary = float(wage_statement.get('net_salary', 0))
        net_salary_words = number_to_words(net_salary)

        label_style = ParagraphStyle(
            'NetLabel',
            parent=styles['Normal'],
            fontSize=10,
            textColor=PDFGenerator.BLACK,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        net_val_style = ParagraphStyle(
            'NetValue',
            parent=styles['Normal'],
            fontSize=11,
            textColor=PDFGenerator.BLACK,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        )
        words_style = ParagraphStyle(
            'NetWords',
            parent=styles['Normal'],
            fontSize=9,
            textColor=PDFGenerator.BLACK,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique'
        )

        net_combined_data = [
            [
                Paragraph("<b>Net Salary</b>", label_style),
                Paragraph(f"<b>Rs. {net_salary:,.2f}</b>", net_val_style)
            ],
            [
                Paragraph("<b>Net Salary in Words</b>", label_style),
                Paragraph(net_salary_words, words_style)
            ],
        ]
        net_combined_table = Table(net_combined_data, colWidths=[2.0*inch, 5.5*inch])
        net_combined_table.setStyle(TableStyle([
            # Label column - light gray
            ('BACKGROUND', (0, 0), (0, -1), PDFGenerator.LIGHT_GRAY),
            # Value column - white
            ('BACKGROUND', (1, 0), (1, -1), PDFGenerator.WHITE),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('ALIGN', (1, 1), (1, 1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, PDFGenerator.BLACK),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, PDFGenerator.BLACK),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(net_combined_table)

        elements.append(Spacer(1, 0.2*inch))

        # ========================
        # FOOTER
        # ========================
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique'
        )

        footer_text = Paragraph(
            "<i>Note: This is a computer generated document, hence no signature is required.</i>",
            footer_style
        )
        elements.append(footer_text)

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
        month_name = PDFGenerator.get_month_name(month)
        title = Paragraph(
            f"<b>SALARY REGISTER - {month_name} {year}</b>",
            ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER, textColor=PDFGenerator.WHITE)
        )

        title_table = Table([[title]], colWidths=[7.9*inch])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PDFGenerator.DARK_BLUE),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(title_table)
        elements.append(Spacer(1, 0.1*inch))

        # Company name
        company = Paragraph(
            tenant_details.get('name', 'Company Name'),
            ParagraphStyle('company', parent=styles['Normal'], alignment=TA_CENTER, fontName='Helvetica-Bold')
        )
        elements.append(company)
        elements.append(Spacer(1, 0.2*inch))

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
            gross = ws.get('total_earnings', 0)
            deductions_breakdown = ws.get('deductions_breakdown', {})

            pf = deductions_breakdown.get('pf_employee', 0) if isinstance(deductions_breakdown, dict) else 0
            esi = deductions_breakdown.get('esi_employee', 0) if isinstance(deductions_breakdown, dict) else 0
            pt = deductions_breakdown.get('professional_tax', 0) if isinstance(deductions_breakdown, dict) else 0
            tds = deductions_breakdown.get('tds', 0) if isinstance(deductions_breakdown, dict) else 0
            other = 0
            if isinstance(deductions_breakdown, dict):
                other = deductions_breakdown.get('loan_deduction', 0) + deductions_breakdown.get('advance_deduction', 0) + deductions_breakdown.get('other_deductions', 0)
            net = ws.get('net_salary', 0)

            register_data.append([
                str(idx),
                ws.get('employee_code', ''),
                ws.get('employee_name', ''),
                f"{ws.get('present_days', 0)}",
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

        # Build style with alternating rows
        register_style = [
            ('BACKGROUND', (0, 0), (-1, 0), PDFGenerator.DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), PDFGenerator.WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -2), 7),
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, PDFGenerator.BLACK),
            ('BACKGROUND', (0, -1), (-1, -1), PDFGenerator.DARK_BLUE),
            ('TEXTCOLOR', (0, -1), (-1, -1), PDFGenerator.WHITE),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Add alternating row colors
        for i in range(2, len(register_data) - 1, 2):
            register_style.append(('BACKGROUND', (0, i), (-1, i), PDFGenerator.LIGHT_GRAY))

        register_table.setStyle(TableStyle(register_style))
        elements.append(register_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer
