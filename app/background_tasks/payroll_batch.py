import logging
from sqlalchemy.orm import Session
from typing import List, Optional

from app.services.payroll_service import PayrollService

logger = logging.getLogger(__name__)


async def process_payroll_batch(
    db: Session,
    tenant_id: int,
    month: int,
    year: int,
    employee_ids: Optional[List[int]] = None,
) -> dict:
    """
    Background task: calculate wages for a tenant's employees and
    persist wage statements.  Returns a summary dict.
    """
    payroll_service = PayrollService(db)
    result = payroll_service.process_monthly_payroll(
        tenant_id=tenant_id,
        month=month,
        year=year,
        employee_ids=employee_ids,
    )

    logger.info(
        "Payroll batch complete — tenant=%d month=%d/%d total=%d ok=%d fail=%d",
        tenant_id,
        month,
        year,
        result["total"],
        len(result["successful"]),
        len(result["failed"]),
    )
    return result


async def generate_payslips_batch(
    db: Session,
    wage_statement_ids: List[int],
) -> dict:
    """
    Background task: generate PDF payslips for a list of wage statement IDs.
    Returns counts of successes and failures.
    """
    payroll_service = PayrollService(db)
    successful, failed = [], []

    for wage_id in wage_statement_ids:
        try:
            payroll_service.generate_payslip_pdf(wage_id)
            successful.append(wage_id)
        except Exception as exc:
            logger.warning("Failed to generate payslip for statement %d: %s", wage_id, exc)
            failed.append({"id": wage_id, "error": str(exc)})

    logger.info(
        "Payslip generation complete — %d succeeded, %d failed",
        len(successful),
        len(failed),
    )
    return {"successful": successful, "failed": failed}
