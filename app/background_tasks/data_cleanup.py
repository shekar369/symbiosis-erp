import os
import glob
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def cleanup_old_audit_logs(db: Session, days: int = 90) -> int:
    """Delete audit logs older than `days` days. Returns count of deleted rows."""
    from app.models.user import AuditLog

    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted = (
        db.query(AuditLog)
        .filter(AuditLog.created_at < cutoff)
        .delete(synchronize_session=False)
    )
    db.commit()
    logger.info("Deleted %d audit log(s) older than %d days", deleted, days)
    return deleted


async def cleanup_old_uploads(db: Session, days: int = 30) -> int:
    """
    Remove attendance upload records and their associated files older than `days` days.
    Returns count of cleaned records.
    """
    from app.models.attendance import AttendanceUpload

    cutoff = datetime.utcnow() - timedelta(days=days)
    old_uploads = (
        db.query(AttendanceUpload)
        .filter(AttendanceUpload.uploaded_at < cutoff)
        .all()
    )

    count = 0
    for upload in old_uploads:
        # Remove file from disk if it still exists
        if upload.file_path and os.path.exists(upload.file_path):
            try:
                os.remove(upload.file_path)
            except OSError as exc:
                logger.warning("Could not remove file %s: %s", upload.file_path, exc)
        db.delete(upload)
        count += 1

    db.commit()
    logger.info("Removed %d upload record(s) older than %d days", count, days)
    return count


async def archive_old_wage_statements(db: Session, months: int = 12) -> int:
    """
    Mark wage statements older than `months` months as archived by setting
    their status to 'archived'. Returns the number of statements updated.
    """
    from app.models.wage import WageStatement, WageStatus
    from datetime import date
    import calendar

    today = date.today()
    # Calculate the cutoff year/month
    cutoff_month = today.month - months
    cutoff_year = today.year
    while cutoff_month <= 0:
        cutoff_month += 12
        cutoff_year -= 1

    statements = (
        db.query(WageStatement)
        .filter(
            and_(
                WageStatement.status == WageStatus.PAID,
                # year < cutoff_year OR (year == cutoff_year AND month < cutoff_month)
                (WageStatement.year < cutoff_year)
                | (
                    (WageStatement.year == cutoff_year)
                    & (WageStatement.month < cutoff_month)
                ),
            )
        )
        .all()
    )

    for stmt in statements:
        # Use a string value; WageStatus enum can be extended to include 'archived'
        stmt.status = "archived"

    db.commit()
    logger.info("Archived %d wage statement(s) older than %d months", len(statements), months)
    return len(statements)
