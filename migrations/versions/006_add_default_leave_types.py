"""Add default leave types for all tenants

Revision ID: 006
Revises: 005
Create Date: 2025-11-07

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '006'
down_revision: Union[str, None] = '005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get connection to execute raw SQL
    conn = op.get_bind()

    # Get all tenant IDs
    result = conn.execute(sa.text("SELECT id FROM tenants"))
    tenant_ids = [row[0] for row in result.fetchall()]

    # Default leave types to create
    # Using only columns that exist in the current database schema
    default_leave_types = [
        {
            'name': 'Sick Leave',
            'code': 'SL',
            'days_per_year': 12.0,
            'is_paid': 1
        },
        {
            'name': 'Casual Leave',
            'code': 'CL',
            'days_per_year': 10.0,
            'is_paid': 1
        },
        {
            'name': 'Earned Leave',
            'code': 'EL',
            'days_per_year': 15.0,
            'is_paid': 1
        }
    ]

    # Insert default leave types for each tenant
    for tenant_id in tenant_ids:
        for leave_type in default_leave_types:
            # Check if leave type already exists for this tenant
            check_query = sa.text(
                "SELECT COUNT(*) FROM leave_types WHERE tenant_id = :tenant_id AND code = :code"
            )
            result = conn.execute(check_query, {'tenant_id': tenant_id, 'code': f"{leave_type['code']}_{tenant_id}"})
            count = result.fetchone()[0]

            # Only insert if it doesn't exist
            if count == 0:
                insert_query = sa.text("""
                    INSERT INTO leave_types
                    (tenant_id, name, code, days_per_year, is_paid, created_at)
                    VALUES
                    (:tenant_id, :name, :code, :days_per_year, :is_paid, :created_at)
                """)

                conn.execute(insert_query, {
                    'tenant_id': tenant_id,
                    'name': leave_type['name'],
                    'code': f"{leave_type['code']}_{tenant_id}",  # Make code unique per tenant
                    'days_per_year': leave_type['days_per_year'],
                    'is_paid': leave_type['is_paid'],
                    'created_at': datetime.utcnow()
                })


def downgrade() -> None:
    # Remove default leave types (optional - be careful with this in production)
    conn = op.get_bind()

    # Get all tenant IDs
    result = conn.execute(sa.text("SELECT id FROM tenants"))
    tenant_ids = [row[0] for row in result.fetchall()]

    # Delete default leave types
    for tenant_id in tenant_ids:
        for code_prefix in ['SL', 'CL', 'EL']:
            delete_query = sa.text(
                "DELETE FROM leave_types WHERE tenant_id = :tenant_id AND code = :code"
            )
            conn.execute(delete_query, {'tenant_id': tenant_id, 'code': f"{code_prefix}_{tenant_id}"})
