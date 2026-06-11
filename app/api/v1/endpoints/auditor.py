from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User, AuditLog
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("/logs")
async def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    user_id: Optional[int] = Query(None, description="Filter by user"),
    resource_type: Optional[str] = Query(None, description="e.g. employee, payroll"),
    action: Optional[str] = Query(None, description="e.g. CREATE, UPDATE, DELETE"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List audit logs for the current tenant.
    Accessible by auditors, employer admins, and SaaS admins.
    """
    # Resolve which tenant's logs to show
    tenant_id = current_user.tenant_id
    if current_user.is_superuser or current_user.role == "saas_admin":
        # Super/SaaS admin may inspect any tenant; default to own
        tenant_id = current_user.tenant_id

    audit_service = AuditService(db)
    logs = audit_service.get_audit_logs(
        tenant_id=tenant_id,
        skip=skip,
        limit=limit,
        user_id=user_id,
        resource_type=resource_type,
        action=action,
    )
    total = audit_service.count_audit_logs(tenant_id)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "changes": log.changes,
                "ip_address": log.ip_address,
                "created_at": str(log.created_at),
            }
            for log in logs
        ],
    }


@router.get("/logs/{log_id}")
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Return a single audit log entry."""
    log = (
        db.query(AuditLog)
        .filter(
            and_(
                AuditLog.id == log_id,
                AuditLog.tenant_id == current_user.tenant_id,
            )
        )
        .first()
    )
    if not log:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit log not found")

    return {
        "id": log.id,
        "tenant_id": log.tenant_id,
        "user_id": log.user_id,
        "action": log.action,
        "resource_type": log.resource_type,
        "resource_id": log.resource_id,
        "changes": log.changes,
        "ip_address": log.ip_address,
        "user_agent": log.user_agent,
        "created_at": str(log.created_at),
    }
