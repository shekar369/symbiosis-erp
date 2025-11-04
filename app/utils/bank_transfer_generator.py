import csv
from io import StringIO, BytesIO
from datetime import datetime
from typing import List, Dict, Any


class BankTransferGenerator:
    """Generate bank transfer files in various formats (NEFT, RTGS, CSV)"""

    @staticmethod
    def generate_neft_file(
        wage_statements: List[Dict[str, Any]],
        company_details: Dict[str, Any],
        month: int,
        year: int
    ) -> StringIO:
        """
        Generate NEFT format text file for bank upload

        Format: Fixed-width format commonly used by Indian banks

        Args:
            wage_statements: List of wage statement dicts with employee bank details
            company_details: Company bank account details
            month: Month number
            year: Year

        Returns:
            StringIO object containing NEFT format text
        """
        buffer = StringIO()

        # Header record (H)
        header = BankTransferGenerator._create_neft_header(company_details, len(wage_statements))
        buffer.write(header + '\n')

        # Detail records (D)
        total_amount = 0
        for idx, statement in enumerate(wage_statements, 1):
            detail = BankTransferGenerator._create_neft_detail(statement, idx)
            buffer.write(detail + '\n')
            total_amount += statement.get('net_salary', 0)

        # Trailer record (T)
        trailer = BankTransferGenerator._create_neft_trailer(len(wage_statements), total_amount)
        buffer.write(trailer + '\n')

        buffer.seek(0)
        return buffer

    @staticmethod
    def _create_neft_header(company_details: Dict[str, Any], record_count: int) -> str:
        """Create NEFT header record"""
        # Format: H|CompanyCode|CompanyName|PaymentDate|RecordCount|TotalAmount
        payment_date = datetime.now().strftime('%Y%m%d')
        company_code = company_details.get('company_code', '0000').ljust(10)
        company_name = company_details.get('name', 'Company')[:40].ljust(40)

        header = (
            f"H|"
            f"{company_code}|"
            f"{company_name}|"
            f"{payment_date}|"
            f"{record_count:06d}|"
        )

        return header

    @staticmethod
    def _create_neft_detail(statement: Dict[str, Any], seq_no: int) -> str:
        """Create NEFT detail record for each employee"""
        # Format: D|SeqNo|BeneficiaryName|AccountNo|IFSCCode|Amount|BeneficiaryCode
        beneficiary_name = statement.get('employee_name', '')[:40].ljust(40)
        account_no = statement.get('bank_account', '')[:20].ljust(20)
        ifsc_code = statement.get('ifsc_code', '')[:11].ljust(11)
        amount = f"{statement.get('net_salary', 0):.2f}".rjust(15)
        employee_code = statement.get('employee_code', '')[:20].ljust(20)

        detail = (
            f"D|"
            f"{seq_no:06d}|"
            f"{beneficiary_name}|"
            f"{account_no}|"
            f"{ifsc_code}|"
            f"{amount}|"
            f"{employee_code}|"
        )

        return detail

    @staticmethod
    def _create_neft_trailer(record_count: int, total_amount: float) -> str:
        """Create NEFT trailer record"""
        # Format: T|RecordCount|TotalAmount
        amount_str = f"{total_amount:.2f}".rjust(15)

        trailer = (
            f"T|"
            f"{record_count:06d}|"
            f"{amount_str}|"
        )

        return trailer

    @staticmethod
    def generate_csv_file(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        format_type: str = "standard"
    ) -> StringIO:
        """
        Generate CSV file for bank transfer

        Args:
            wage_statements: List of wage statement dicts
            month: Month number
            year: Year
            format_type: CSV format type (standard, hdfc, icici, sbi)

        Returns:
            StringIO object containing CSV data
        """
        buffer = StringIO()

        if format_type == "hdfc":
            return BankTransferGenerator._generate_hdfc_csv(wage_statements, buffer)
        elif format_type == "icici":
            return BankTransferGenerator._generate_icici_csv(wage_statements, buffer)
        elif format_type == "sbi":
            return BankTransferGenerator._generate_sbi_csv(wage_statements, buffer)
        else:
            return BankTransferGenerator._generate_standard_csv(wage_statements, buffer)

    @staticmethod
    def _generate_standard_csv(
        wage_statements: List[Dict[str, Any]],
        buffer: StringIO
    ) -> StringIO:
        """Generate standard CSV format"""
        writer = csv.writer(buffer)

        # Header row
        writer.writerow([
            'S.No',
            'Employee Code',
            'Employee Name',
            'Bank Account Number',
            'IFSC Code',
            'Bank Name',
            'Branch',
            'Net Salary',
            'Payment Date',
            'Remarks'
        ])

        # Data rows
        payment_date = datetime.now().strftime('%d-%m-%Y')
        for idx, statement in enumerate(wage_statements, 1):
            writer.writerow([
                idx,
                statement.get('employee_code', ''),
                statement.get('employee_name', ''),
                statement.get('bank_account', ''),
                statement.get('ifsc_code', ''),
                statement.get('bank_name', 'N/A'),
                statement.get('branch', 'N/A'),
                f"{statement.get('net_salary', 0):.2f}",
                payment_date,
                f"Salary for {statement.get('month', 1):02d}/{statement.get('year', 2025)}"
            ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def _generate_hdfc_csv(
        wage_statements: List[Dict[str, Any]],
        buffer: StringIO
    ) -> StringIO:
        """Generate HDFC Bank specific CSV format"""
        writer = csv.writer(buffer)

        # HDFC Format: Account No, Beneficiary Name, Amount, Payment Mode, IFSC, Narration
        writer.writerow([
            'Account No',
            'Beneficiary Name',
            'Amount',
            'Payment Mode',
            'IFSC Code',
            'Narration'
        ])

        for statement in wage_statements:
            writer.writerow([
                statement.get('bank_account', ''),
                statement.get('employee_name', ''),
                f"{statement.get('net_salary', 0):.2f}",
                'NEFT',
                statement.get('ifsc_code', ''),
                f"Salary {statement.get('month', 1):02d}/{statement.get('year', 2025)} - {statement.get('employee_code', '')}"
            ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def _generate_icici_csv(
        wage_statements: List[Dict[str, Any]],
        buffer: StringIO
    ) -> StringIO:
        """Generate ICICI Bank specific CSV format"""
        writer = csv.writer(buffer)

        # ICICI Format
        writer.writerow([
            'Beneficiary Code',
            'Beneficiary Account Number',
            'Beneficiary Name',
            'Amount',
            'Payment Mode',
            'IFSC Code',
            'Payment Details'
        ])

        for statement in wage_statements:
            writer.writerow([
                statement.get('employee_code', ''),
                statement.get('bank_account', ''),
                statement.get('employee_name', ''),
                f"{statement.get('net_salary', 0):.2f}",
                'NEFT',
                statement.get('ifsc_code', ''),
                f"Salary Payment {statement.get('month', 1):02d}/{statement.get('year', 2025)}"
            ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def _generate_sbi_csv(
        wage_statements: List[Dict[str, Any]],
        buffer: StringIO
    ) -> StringIO:
        """Generate SBI Bank specific CSV format"""
        writer = csv.writer(buffer)

        # SBI Format
        writer.writerow([
            'Sr No',
            'Beneficiary A/c No',
            'Beneficiary Name',
            'Amount',
            'Beneficiary IFSC',
            'Remarks'
        ])

        for idx, statement in enumerate(wage_statements, 1):
            writer.writerow([
                idx,
                statement.get('bank_account', ''),
                statement.get('employee_name', ''),
                f"{statement.get('net_salary', 0):.2f}",
                statement.get('ifsc_code', ''),
                f"Salary {statement.get('employee_code', '')} {statement.get('month', 1):02d}/{statement.get('year', 2025)}"
            ])

        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_payment_summary(
        wage_statements: List[Dict[str, Any]],
        month: int,
        year: int,
        company_details: Dict[str, Any]
    ) -> StringIO:
        """
        Generate payment summary text file

        Args:
            wage_statements: List of wage statements
            month: Month number
            year: Year
            company_details: Company information

        Returns:
            StringIO with summary text
        """
        buffer = StringIO()

        # Header
        buffer.write("=" * 80 + "\n")
        buffer.write(f"{company_details.get('name', 'Company Name').center(80)}\n")
        buffer.write("SALARY PAYMENT SUMMARY\n".center(80))
        buffer.write(f"Period: {month:02d}/{year}\n".center(80))
        buffer.write(f"Generated on: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}\n".center(80))
        buffer.write("=" * 80 + "\n\n")

        # Summary statistics
        total_employees = len(wage_statements)
        total_amount = sum(s.get('net_salary', 0) for s in wage_statements)

        buffer.write(f"Total Employees: {total_employees}\n")
        buffer.write(f"Total Amount: ₹ {total_amount:,.2f}\n\n")

        # Bank-wise breakdown
        bank_summary = {}
        for statement in wage_statements:
            bank = statement.get('bank_name', 'Unknown Bank')
            if bank not in bank_summary:
                bank_summary[bank] = {'count': 0, 'amount': 0}
            bank_summary[bank]['count'] += 1
            bank_summary[bank]['amount'] += statement.get('net_salary', 0)

        buffer.write("Bank-wise Breakdown:\n")
        buffer.write("-" * 80 + "\n")
        buffer.write(f"{'Bank Name':<40} {'Employees':>15} {'Total Amount':>20}\n")
        buffer.write("-" * 80 + "\n")

        for bank, data in sorted(bank_summary.items()):
            buffer.write(f"{bank:<40} {data['count']:>15} ₹ {data['amount']:>18,.2f}\n")

        buffer.write("-" * 80 + "\n")
        buffer.write(f"{'TOTAL':<40} {total_employees:>15} ₹ {total_amount:>18,.2f}\n")
        buffer.write("=" * 80 + "\n\n")

        # Detailed list
        buffer.write("Detailed Payment List:\n")
        buffer.write("-" * 80 + "\n")
        buffer.write(f"{'S.No':<6} {'Emp Code':<12} {'Name':<30} {'Net Salary':>18}\n")
        buffer.write("-" * 80 + "\n")

        for idx, statement in enumerate(wage_statements, 1):
            buffer.write(
                f"{idx:<6} "
                f"{statement.get('employee_code', ''):<12} "
                f"{statement.get('employee_name', '')[:30]:<30} "
                f"₹ {statement.get('net_salary', 0):>16,.2f}\n"
            )

        buffer.write("=" * 80 + "\n")

        # Footer
        buffer.write("\n\nAuthorized Signatory: _____________________\n")
        buffer.write(f"Date: {datetime.now().strftime('%d-%b-%Y')}\n")

        buffer.seek(0)
        return buffer
