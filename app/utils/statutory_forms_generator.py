import csv
from io import StringIO, BytesIO
from datetime import datetime
from typing import List, Dict, Any
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class StatutoryFormsGenerator:
    """Generate statutory compliance forms for Indian payroll"""

    @staticmethod
    def generate_epf_ecr(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        establishment_details: Dict[str, Any]
    ) -> StringIO:
        """
        Generate EPF-ECR (Electronic Challan Cum Return) CSV file

        Format: As per EPFO specifications

        Args:
            wage_statements: List of wage statement dicts with PF details
            month: Month number
            year: Year
            establishment_details: Company PF registration details

        Returns:
            StringIO object containing EPF-ECR CSV
        """
        buffer = StringIO()
        writer = csv.writer(buffer)

        # Header row as per EPFO format
        writer.writerow([
            'UAN',
            'Member Name',
            'Gross Wages',
            'EPF Wages',
            'EPS Wages',
            'EDLI Wages',
            'EPF Contribution (EE)',
            'EPS Contribution (ER)',
            'EPF Contribution (ER)',
            'NCP Days',
            'Refund of Advances'
        ])

        total_epf_ee = 0
        total_eps_er = 0
        total_epf_er = 0

        for ws in wage_statements:
            # Only include if PF applicable
            pf_employee = ws.get('pf_employee', 0)
            if pf_employee > 0:
                basic = ws.get('basic_salary', 0)

                # PF wages (capped at 15,000)
                epf_wages = min(basic, 15000)

                # EPS wages (capped at 15,000)
                eps_wages = min(basic, 15000)

                # EDLI wages (capped at 15,000)
                edli_wages = min(basic, 15000)

                # Employee contribution (12% of basic)
                epf_ee = round(epf_wages * 0.12, 2)

                # Employer EPS contribution (8.33% of basic)
                eps_er = round(eps_wages * 0.0833, 2)

                # Employer EPF contribution (3.67% of basic)
                epf_er = round(epf_wages * 0.0367, 2)

                # NCP days
                ncp_days = ws.get('days_absent', 0)

                writer.writerow([
                    ws.get('uan', ''),  # UAN number
                    ws.get('employee_name', ''),
                    f"{ws.get('gross_salary', 0):.2f}",
                    f"{epf_wages:.2f}",
                    f"{eps_wages:.2f}",
                    f"{edli_wages:.2f}",
                    f"{epf_ee:.2f}",
                    f"{eps_er:.2f}",
                    f"{epf_er:.2f}",
                    str(ncp_days),
                    "0.00"
                ])

                total_epf_ee += epf_ee
                total_eps_er += eps_er
                total_epf_er += epf_er

        # Totals row
        writer.writerow([
            '',
            'TOTAL',
            '',
            '',
            '',
            '',
            f"{total_epf_ee:.2f}",
            f"{total_eps_er:.2f}",
            f"{total_epf_er:.2f}",
            '',
            '0.00'
        ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_esi_return(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        establishment_details: Dict[str, Any]
    ) -> StringIO:
        """
        Generate ESI monthly return CSV

        Args:
            wage_statements: List of wage statements with ESI details
            month: Month number
            year: Year
            establishment_details: Company ESI registration details

        Returns:
            StringIO object containing ESI return CSV
        """
        buffer = StringIO()
        writer = csv.writer(buffer)

        # Header
        writer.writerow([
            'IP Number',
            'IP Name',
            'Number of Days for which Wages Paid/Payable',
            'Total Monthly Wages',
            'Reason Code for Zero Working Days',
            'Last Working Day'
        ])

        for ws in wage_statements:
            # Only include if ESI applicable (gross <= 21,000)
            if ws.get('esi_employee', 0) > 0:
                writer.writerow([
                    ws.get('esic_ip_number', ''),
                    ws.get('employee_name', ''),
                    str(ws.get('days_worked', 0)),
                    f"{ws.get('gross_salary', 0):.2f}",
                    '',  # Reason code (if zero days)
                    ''   # Last working day (if left)
                ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_pt_form_v(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        state: str,
        establishment_details: Dict[str, Any]
    ) -> BytesIO:
        """
        Generate Professional Tax Form V (Maharashtra format)

        Args:
            wage_statements: List of wage statements
            month: Month number
            year: Year
            state: State name
            establishment_details: Company details

        Returns:
            BytesIO object containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(
            f"<b>PROFESSIONAL TAX RETURN - FORM V</b>",
            ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER)
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Company details
        company_info = Paragraph(
            f"<b>Employer:</b> {establishment_details.get('name', 'Company Name')}<br/>"
            f"<b>Registration No:</b> {establishment_details.get('pt_registration', 'N/A')}<br/>"
            f"<b>Period:</b> {month:02d}/{year}<br/>"
            f"<b>State:</b> {state}",
            styles['Normal']
        )
        elements.append(company_info)
        elements.append(Spacer(1, 0.3*inch))

        # PT deduction table
        pt_data = [
            ['S.No', 'Employee Name', 'Employee Code', 'Gross Salary', 'PT Deducted']
        ]

        total_pt = 0
        for idx, ws in enumerate(wage_statements, 1):
            pt_amount = ws.get('professional_tax', 0)
            if pt_amount > 0:
                pt_data.append([
                    str(idx),
                    ws.get('employee_name', ''),
                    ws.get('employee_code', ''),
                    f"₹ {ws.get('gross_salary', 0):,.2f}",
                    f"₹ {pt_amount:,.2f}"
                ])
                total_pt += pt_amount

        # Totals
        pt_data.append([
            '', '', 'TOTAL', '', f"₹ {total_pt:,.2f}"
        ])

        pt_table = Table(pt_data, colWidths=[0.6*inch, 2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        pt_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dbeafe')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (3, 1), (4, -1), 'RIGHT'),
        ]))
        elements.append(pt_table)
        elements.append(Spacer(1, 0.3*inch))

        # Summary
        summary = Paragraph(
            f"<b>Total Professional Tax Deducted:</b> ₹ {total_pt:,.2f}<br/>"
            f"<b>Number of Employees:</b> {len([ws for ws in wage_statements if ws.get('professional_tax', 0) > 0])}",
            styles['Normal']
        )
        elements.append(summary)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_form_xiii(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        establishment_details: Dict[str, Any]
    ) -> BytesIO:
        """
        Generate Form-XIII (Workmen Register under Contract Labour Act)

        Args:
            wage_statements: List of wage statements
            month: Month number
            year: Year
            establishment_details: Company details

        Returns:
            BytesIO object containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(
            f"<b>FORM XIII - REGISTER OF WORKMEN</b><br/>"
            f"<font size=10>(Under Rule 78(1)(a)(i) of the Contract Labour Act, 1970)</font>",
            ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=14)
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Company details
        company_info = Paragraph(
            f"<b>Name and Address of Establishment:</b> {establishment_details.get('name', 'Company Name')}<br/>"
            f"<b>Registration No:</b> {establishment_details.get('contract_labour_reg', 'N/A')}<br/>"
            f"<b>Period:</b> {month:02d}/{year}",
            styles['Normal']
        )
        elements.append(company_info)
        elements.append(Spacer(1, 0.3*inch))

        # Workmen register table
        register_data = [
            ['S.No', 'Name', 'Father/Husband', 'Age', 'Designation', 'Wages', 'Days Worked']
        ]

        for idx, ws in enumerate(wage_statements, 1):
            register_data.append([
                str(idx),
                ws.get('employee_name', ''),
                ws.get('father_name', 'N/A'),
                str(ws.get('age', 'N/A')),
                ws.get('designation', ''),
                f"₹ {ws.get('net_salary', 0):,.0f}",
                str(ws.get('days_worked', 0))
            ])

        register_table = Table(register_data, colWidths=[0.5*inch, 1.8*inch, 1.5*inch, 0.6*inch, 1.5*inch, 1*inch, 0.8*inch])
        register_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(register_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_monthly_pf_challan_summary(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        establishment_details: Dict[str, Any]
    ) -> BytesIO:
        """
        Generate monthly PF challan summary PDF

        Args:
            wage_statements: List of wage statements
            month: Month number
            year: Year
            establishment_details: Company PF details

        Returns:
            BytesIO object containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(
            f"<b>EPF CHALLAN SUMMARY</b><br/>"
            f"<font size=10>Month: {month:02d}/{year}</font>",
            ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER)
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Company details
        company_info = Paragraph(
            f"<b>Establishment:</b> {establishment_details.get('name', 'Company Name')}<br/>"
            f"<b>EPF Code:</b> {establishment_details.get('epf_code', 'N/A')}<br/>"
            f"<b>EPF Registration:</b> {establishment_details.get('epf_registration', 'N/A')}",
            styles['Normal']
        )
        elements.append(company_info)
        elements.append(Spacer(1, 0.3*inch))

        # Calculate totals
        total_employees = len([ws for ws in wage_statements if ws.get('pf_employee', 0) > 0])
        total_wages = sum(min(ws.get('basic_salary', 0), 15000) for ws in wage_statements if ws.get('pf_employee', 0) > 0)
        total_epf_ee = sum(ws.get('pf_employee', 0) for ws in wage_statements)
        total_eps_er = sum(min(ws.get('basic_salary', 0), 15000) * 0.0833 for ws in wage_statements if ws.get('pf_employee', 0) > 0)
        total_epf_er = sum(min(ws.get('basic_salary', 0), 15000) * 0.0367 for ws in wage_statements if ws.get('pf_employee', 0) > 0)

        # Summary table
        summary_data = [
            ['Particulars', 'Amount (₹)'],
            ['Number of Employees', str(total_employees)],
            ['Total PF Wages', f"{total_wages:,.2f}"],
            ['Employee Share (EE) - 12%', f"{total_epf_ee:,.2f}"],
            ['Employer Share (EPS) - 8.33%', f"{total_eps_er:,.2f}"],
            ['Employer Share (EPF) - 3.67%', f"{total_epf_er:,.2f}"],
            ['Admin Charges - 0.5%', f"{total_wages * 0.005:,.2f}"],
            ['EDLI Charges - 0.5%', f"{total_wages * 0.005:,.2f}"],
            ['Total EPF Contribution', f"{total_epf_ee + total_epf_er:,.2f}"],
            ['Total Employer Contribution', f"{total_eps_er + total_epf_er + (total_wages * 0.01):,.2f}"],
            ['GRAND TOTAL', f"{total_epf_ee + total_eps_er + total_epf_er + (total_wages * 0.01):,.2f}"]
        ]

        summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
        ]))
        elements.append(summary_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer
