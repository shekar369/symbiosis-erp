from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import date, datetime
from typing import Dict, Any, Optional
from calendar import monthrange

from app.models.wage import WageStatement
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.overtime import Overtime
from app.models.advance_loan import Advance, Loan
from app.models.salary import EmployeeSalaryConfig


class WageCalculationService:
    """Service for calculating employee wages and statutory deductions"""

    # Statutory rates (can be moved to config/database)
    PF_RATE = 0.12  # 12% of basic
    PF_CEILING = 15000  # PF applicable only if basic <= 15000
    ESI_RATE = 0.0075  # 0.75% of gross
    ESI_CEILING = 21000  # ESI applicable only if gross <= 21000

    # Professional Tax slabs (Maharashtra - can be state-specific)
    PT_SLABS = [
        (0, 10000, 0),
        (10001, 25000, 175),
        (25001, float('inf'), 200)
    ]

    def __init__(self, db: Session):
        self.db = db

    def calculate_monthly_wage(
        self,
        employee_id: int,
        month: int,
        year: int,
        create_statement: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate complete monthly wage for an employee
        Returns wage calculation details
        """
        # Get employee details
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise ValueError(f"Employee {employee_id} not found")

        # Get salary configuration
        salary_config = self.db.query(EmployeeSalaryConfig).filter(
            EmployeeSalaryConfig.employee_id == employee_id
        ).first()

        if not salary_config:
            raise ValueError(f"Salary configuration not found for employee {employee_id}")

        # Calculate working days
        total_days = monthrange(year, month)[1]

        # Get attendance data
        attendance_data = self.get_attendance_data(employee_id, month, year)
        days_worked = attendance_data['days_present']
        days_absent = attendance_data['days_absent']
        days_half = attendance_data['days_half_day']

        # Calculate effective working days (half day = 0.5)
        effective_days = days_worked + (days_half * 0.5)

        # Calculate earnings
        earnings = self.calculate_earnings(
            salary_config,
            effective_days,
            total_days,
            employee_id,
            month,
            year
        )

        # Calculate deductions
        deductions = self.calculate_deductions(
            earnings['gross_salary'],
            earnings['basic_salary'],
            employee_id,
            month,
            year
        )

        # Calculate net salary
        net_salary = earnings['gross_salary'] - deductions['total_deductions']

        wage_data = {
            'employee_id': employee_id,
            'month': month,
            'year': year,
            'days_worked': days_worked,
            'days_absent': days_absent,
            'days_half_day': days_half,
            'effective_days': effective_days,
            'total_days': total_days,
            **earnings,
            **deductions,
            'net_salary': round(net_salary, 2),
            'status': 'calculated'
        }

        # Create wage statement if requested
        if create_statement:
            self.create_wage_statement(wage_data)

        return wage_data

    def get_attendance_data(self, employee_id: int, month: int, year: int) -> Dict[str, int]:
        """Get attendance summary for the month"""
        attendances = self.db.query(Attendance).filter(
            and_(
                Attendance.employee_id == employee_id,
                extract('month', Attendance.date) == month,
                extract('year', Attendance.date) == year
            )
        ).all()

        days_present = sum(1 for a in attendances if a.status == 'present')
        days_absent = sum(1 for a in attendances if a.status == 'absent')
        days_half_day = sum(1 for a in attendances if a.status == 'half-day')
        days_leave = sum(1 for a in attendances if a.status == 'leave')

        return {
            'days_present': days_present,
            'days_absent': days_absent,
            'days_half_day': days_half_day,
            'days_leave': days_leave,
            'total_recorded': len(attendances)
        }

    def calculate_earnings(
        self,
        salary_config: EmployeeSalaryConfig,
        effective_days: float,
        total_days: int,
        employee_id: int,
        month: int,
        year: int
    ) -> Dict[str, float]:
        """Calculate all earning components"""

        # Get monthly salary components from config JSON
        components = salary_config.components or {}

        # Basic salary (pro-rated based on days worked)
        basic_monthly = components.get('basic', 0)
        basic_salary = (basic_monthly / total_days) * effective_days

        # HRA (House Rent Allowance) - typically 40-50% of basic
        hra_monthly = components.get('hra', basic_monthly * 0.4)
        hra = (hra_monthly / total_days) * effective_days

        # Conveyance Allowance
        conveyance_monthly = components.get('conveyance', 1600)
        conveyance = (conveyance_monthly / total_days) * effective_days

        # Medical Allowance
        medical_monthly = components.get('medical', 1250)
        medical = (medical_monthly / total_days) * effective_days

        # Special Allowance
        special_monthly = components.get('special', 0)
        special = (special_monthly / total_days) * effective_days

        # Other Allowances
        other_monthly = components.get('other', 0)
        other = (other_monthly / total_days) * effective_days

        # Overtime calculation
        overtime_amount = self.calculate_overtime(employee_id, month, year, basic_monthly)

        # Gross salary
        gross_salary = (
            basic_salary + hra + conveyance + medical +
            special + other + overtime_amount
        )

        return {
            'basic_salary': round(basic_salary, 2),
            'hra': round(hra, 2),
            'conveyance_allowance': round(conveyance, 2),
            'medical_allowance': round(medical, 2),
            'special_allowance': round(special, 2),
            'other_allowances': round(other, 2),
            'overtime_amount': round(overtime_amount, 2),
            'gross_salary': round(gross_salary, 2)
        }

    def calculate_overtime(
        self,
        employee_id: int,
        month: int,
        year: int,
        basic_monthly: float
    ) -> float:
        """Calculate overtime amount"""
        overtimes = self.db.query(Overtime).filter(
            and_(
                Overtime.employee_id == employee_id,
                extract('month', Overtime.date) == month,
                extract('year', Overtime.date) == year,
                Overtime.status == 'approved'
            )
        ).all()

        # Calculate hourly rate (basic / 26 days / 8 hours)
        hourly_rate = basic_monthly / (26 * 8)

        total_overtime = 0
        for ot in overtimes:
            # Overtime rate is typically 2x hourly rate
            rate_multiplier = ot.rate_multiplier if hasattr(ot, 'rate_multiplier') else 2.0
            total_overtime += ot.hours * hourly_rate * rate_multiplier

        return total_overtime

    def calculate_deductions(
        self,
        gross_salary: float,
        basic_salary: float,
        employee_id: int,
        month: int,
        year: int
    ) -> Dict[str, float]:
        """Calculate all deduction components"""

        # Statutory deductions
        statutory = self.calculate_statutory_deductions(gross_salary, basic_salary)

        # Loan deductions
        loan_deduction = self.process_loan_deductions(employee_id, month, year)

        # Advance deductions
        advance_deduction = self.process_advance_deductions(employee_id, month, year)

        # TDS (simplified - should use tax slabs)
        tds = self.calculate_tds(gross_salary)

        # Other deductions (can be extended)
        other_deductions = 0

        total_deductions = (
            statutory['pf_employee'] +
            statutory['esi_employee'] +
            statutory['professional_tax'] +
            loan_deduction +
            advance_deduction +
            tds +
            other_deductions
        )

        return {
            'pf_employee': statutory['pf_employee'],
            'pf_employer': statutory['pf_employer'],
            'esi_employee': statutory['esi_employee'],
            'esi_employer': statutory['esi_employer'],
            'professional_tax': statutory['professional_tax'],
            'tds': round(tds, 2),
            'loan_deduction': round(loan_deduction, 2),
            'advance_deduction': round(advance_deduction, 2),
            'other_deductions': round(other_deductions, 2),
            'total_deductions': round(total_deductions, 2)
        }

    def calculate_statutory_deductions(
        self,
        gross_salary: float,
        basic_salary: float
    ) -> Dict[str, float]:
        """Calculate PF, ESI, and PT"""

        # PF calculation (12% of basic, applicable if basic <= 15000)
        if basic_salary <= self.PF_CEILING:
            pf_employee = basic_salary * self.PF_RATE
            pf_employer = basic_salary * self.PF_RATE
        else:
            pf_employee = 0
            pf_employer = 0

        # ESI calculation (0.75% of gross, applicable if gross <= 21000)
        if gross_salary <= self.ESI_CEILING:
            esi_employee = gross_salary * self.ESI_RATE
            esi_employer = gross_salary * 0.0325  # 3.25% employer contribution
        else:
            esi_employee = 0
            esi_employer = 0

        # Professional Tax (state-specific slabs)
        professional_tax = self.calculate_professional_tax(gross_salary)

        return {
            'pf_employee': round(pf_employee, 2),
            'pf_employer': round(pf_employer, 2),
            'esi_employee': round(esi_employee, 2),
            'esi_employer': round(esi_employer, 2),
            'professional_tax': round(professional_tax, 2)
        }

    def calculate_professional_tax(self, gross_salary: float) -> float:
        """Calculate professional tax based on slabs"""
        for min_val, max_val, tax in self.PT_SLABS:
            if min_val <= gross_salary <= max_val:
                return tax
        return 0

    def calculate_tds(self, gross_salary: float) -> float:
        """Simplified TDS calculation (should use proper tax slabs)"""
        annual_salary = gross_salary * 12

        # Simplified calculation - actual should use IT slabs
        if annual_salary <= 250000:
            return 0
        elif annual_salary <= 500000:
            tds_annual = (annual_salary - 250000) * 0.05
        elif annual_salary <= 1000000:
            tds_annual = 12500 + (annual_salary - 500000) * 0.20
        else:
            tds_annual = 112500 + (annual_salary - 1000000) * 0.30

        # Monthly TDS
        return tds_annual / 12

    def process_loan_deductions(
        self,
        employee_id: int,
        month: int,
        year: int
    ) -> float:
        """Calculate total loan EMI deductions"""
        loans = self.db.query(Loan).filter(
            and_(
                Loan.employee_id == employee_id,
                Loan.status == 'active'
            )
        ).all()

        total_deduction = 0
        for loan in loans:
            # Deduct EMI if loan is still active
            if loan.emi_amount and loan.remaining_amount > 0:
                total_deduction += loan.emi_amount

        return total_deduction

    def process_advance_deductions(
        self,
        employee_id: int,
        month: int,
        year: int
    ) -> float:
        """Calculate advance recovery amount"""
        advances = self.db.query(Advance).filter(
            and_(
                Advance.employee_id == employee_id,
                Advance.status == 'approved',
                Advance.recovery_amount > 0
            )
        ).all()

        total_deduction = 0
        for advance in advances:
            if advance.remaining_amount > 0:
                # Recover in installments
                installment = min(advance.recovery_amount, advance.remaining_amount)
                total_deduction += installment

        return total_deduction

    def create_wage_statement(self, wage_data: Dict[str, Any]) -> WageStatement:
        """Create or update wage statement record"""

        # Check if statement already exists
        existing = self.db.query(WageStatement).filter(
            and_(
                WageStatement.employee_id == wage_data['employee_id'],
                WageStatement.month == wage_data['month'],
                WageStatement.year == wage_data['year']
            )
        ).first()

        if existing:
            # Update existing statement
            for key, value in wage_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            statement = existing
        else:
            # Create new statement
            statement = WageStatement(**wage_data)
            self.db.add(statement)

        self.db.commit()
        self.db.refresh(statement)

        return statement

    def process_bulk_payroll(
        self,
        tenant_id: int,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """Process payroll for all active employees in a tenant"""

        employees = self.db.query(Employee).filter(
            and_(
                Employee.tenant_id == tenant_id,
                Employee.status == 'active'
            )
        ).all()

        successful = []
        failed = []

        for employee in employees:
            try:
                wage_data = self.calculate_monthly_wage(
                    employee.id,
                    month,
                    year,
                    create_statement=True
                )
                successful.append({
                    'employee_id': employee.id,
                    'employee_code': employee.employee_code,
                    'net_salary': wage_data['net_salary']
                })
            except Exception as e:
                failed.append({
                    'employee_id': employee.id,
                    'employee_code': employee.employee_code,
                    'error': str(e)
                })

        return {
            'total_employees': len(employees),
            'successful': len(successful),
            'failed': len(failed),
            'successful_records': successful,
            'failed_records': failed
        }
