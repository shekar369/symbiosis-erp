from sqlalchemy.orm import Session
from typing import List

from app.services.payroll_service import PayrollService


async def process_payroll_batch(
    db: Session,
    tenant_id: int,
    month: int,
    year: int,
    employee_ids: List[int] = None
):
    """
    Background task to process payroll for multiple employees
    """
    payroll_service = PayrollService(db)

    # Process payroll
    await payroll_service.process_monthly_payroll(
        tenant_id=tenant_id,
        month=month,
        year=year,
        employee_ids=employee_ids
    )

    # Send notifications
    # Generate reports
    # Update status


async def generate_payslips_batch(db: Session, wage_statement_ids: List[int]):
    """
    Background task to generate PDF payslips for multiple employees
    """
    payroll_service = PayrollService(db)

    for wage_id in wage_statement_ids:
        await payroll_service.generate_payslip_pdf(wage_id)
