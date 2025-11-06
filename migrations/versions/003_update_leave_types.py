"""Create leave types and related tables

Revision ID: 003
Revises: 002
Create Date: 2025-11-06

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create leave_types table
    op.create_table(
        'leave_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False, index=True),
        sa.Column('days_per_year', sa.Float(), nullable=False),
        sa.Column('is_paid', sa.Integer(), default=1),
        sa.Column('carry_forward', sa.Integer(), default=0),
        sa.Column('max_carry_forward_days', sa.Float(), default=0),
        sa.Column('is_active', sa.Integer(), default=1),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create leave_balances table
    op.create_table(
        'leave_balances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('leave_type_id', sa.Integer(), sa.ForeignKey('leave_types.id'), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('total_days', sa.Float(), default=0),
        sa.Column('used_days', sa.Float(), default=0),
        sa.Column('balance_days', sa.Float(), default=0),
        sa.PrimaryKeyConstraint('id')
    )

    # Create leave_requests table
    op.create_table(
        'leave_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('leave_type_id', sa.Integer(), sa.ForeignKey('leave_types.id'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('days', sa.Float(), nullable=False),
        sa.Column('reason', sa.String()),
        sa.Column('status', sa.String(), default='PENDING'),
        sa.Column('approved_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('leave_requests')
    op.drop_table('leave_balances')
    op.drop_table('leave_types')
