from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from app.services.wage_calculation_service import WageCalculationService
from app.models.wage import WageStatement, WageStatus
from app.models.employee import Employee


class PayrollService:
    def __init__(self, db: Session):
        self.db = db
        self.wage_calculator = WageCalculationService(db)

    def process_monthly_payroll(
        self,
        tenant_id: int,
        month: int,
        year: int,
        employee_ids: List[int] = None,
    ) -> dict:
        """Calculate wages for all (or selected) active employees in a tenant."""
        query = self.db.query(Employee).filter(
            and_(Employee.tenant_id == tenant_id, Employee.status == "active")
        )
        if employee_ids:
            query = query.filter(Employee.id.in_(employee_ids))
        employees = query.all()

        successful, failed = [], []
        for emp in employees:
            try:
                wage_data = self.wage_calculator.calculate_monthly_wage(
                    emp.id, month, year, create_statement=True
                )
                successful.append(
                    {"employee_id": emp.id, "net_salary": wage_data["net_salary"]}
                )
            except Exception as exc:
                self.db.rollback()
                failed.append({"employee_id": emp.id, "error": str(exc)})

        return {
            "total": len(employees),
            "successful": successful,
            "failed": failed,
        }

    def generate_payslip_pdf(self, wage_statement_id: int) -> bytes:
        """Generate a PDF payslip for the given wage statement and return the bytes."""
        from app.utils.pdf_generator import PDFGenerator
        from app.models.tenant import Tenant

        statement = (
            self.db.query(WageStatement)
            .filter(WageStatement.id == wage_statement_id)
            .first()
        )
        if not statement:
            raise ValueError(f"Wage statement {wage_statement_id} not found")

        employee = (
            self.db.query(Employee)
            .filter(Employee.id == statement.employee_id)
            .first()
        )
        tenant = (
            self.db.query(Tenant).filter(Tenant.id == employee.tenant_id).first()
        )

        generator = PDFGenerator()
        return generator.generate_payslip(employee, statement, tenant)

    def approve_payroll(
        self, month: int, year: int, approved_by: int, tenant_id: int
    ) -> int:
        """Approve all calculated wage statements for the given month/year."""
        statements = (
            self.db.query(WageStatement)
            .join(Employee, WageStatement.employee_id == Employee.id)
            .filter(
                and_(
                    WageStatement.month == month,
                    WageStatement.year == year,
                    WageStatement.status == WageStatus.CALCULATED,
                    Employee.tenant_id == tenant_id,
                )
            )
            .all()
        )
        for stmt in statements:
            stmt.status = WageStatus.APPROVED
            stmt.approved_at = datetime.utcnow()
        self.db.commit()
        return len(statements)

    def mark_as_paid(self, wage_statement_id: int) -> Optional[WageStatement]:
        """Transition a single wage statement to PAID status."""
        stmt = (
            self.db.query(WageStatement)
            .filter(WageStatement.id == wage_statement_id)
            .first()
        )
        if not stmt:
            return None
        stmt.status = WageStatus.PAID
        stmt.paid_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(stmt)
        return stmt
