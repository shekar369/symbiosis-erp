"""Utility functions for leave management setup"""
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.leave import LeaveType
from app.schemas.leave import LeaveTypeCreate


def get_default_leave_types() -> List[dict]:
    """Returns the default leave types configuration"""
    return [
        {
            'name': 'Sick Leave',
            'code': 'SL',
            'days_per_year': 12.0,
            'is_paid': True
        },
        {
            'name': 'Casual Leave',
            'code': 'CL',
            'days_per_year': 10.0,
            'is_paid': True
        },
        {
            'name': 'Earned Leave',
            'code': 'EL',
            'days_per_year': 15.0,
            'is_paid': True
        }
    ]


def initialize_default_leave_types(db: Session, tenant_id: int) -> List[LeaveType]:
    """
    Initialize default leave types for a new tenant.

    Args:
        db: Database session
        tenant_id: ID of the tenant to create leave types for

    Returns:
        List of created LeaveType objects
    """
    default_types = get_default_leave_types()
    created_types = []

    for leave_type_data in default_types:
        # Check if leave type already exists for this tenant
        code = f"{leave_type_data['code']}_{tenant_id}"
        existing = db.query(LeaveType).filter(
            LeaveType.tenant_id == tenant_id,
            LeaveType.code == code
        ).first()

        if not existing:
            # Create new leave type
            db_leave_type = LeaveType(
                tenant_id=tenant_id,
                name=leave_type_data['name'],
                code=code,
                days_per_year=leave_type_data['days_per_year'],
                is_paid=1 if leave_type_data['is_paid'] else 0,
                created_at=datetime.utcnow()
            )
            db.add(db_leave_type)
            created_types.append(db_leave_type)

    if created_types:
        db.commit()
        for leave_type in created_types:
            db.refresh(leave_type)

    return created_types
