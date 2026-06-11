from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.models.user import AuditLog


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        tenant_id: int,
        user_id: int,
        action: str,
        resource_type: str = None,
        resource_id: int = None,
        changes: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None
    ) -> AuditLog:
        """Persist a user action to the audit trail."""
        log = AuditLog(
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_audit_logs(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        action: Optional[str] = None,
    ) -> List[AuditLog]:
        """Return audit logs for a tenant with optional column-level filters."""
        query = self.db.query(AuditLog).filter(AuditLog.tenant_id == tenant_id)
        if user_id is not None:
            query = query.filter(AuditLog.user_id == user_id)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if action:
            query = query.filter(AuditLog.action == action)
        return (
            query.order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_audit_logs(self, tenant_id: int) -> int:
        return self.db.query(AuditLog).filter(AuditLog.tenant_id == tenant_id).count()
