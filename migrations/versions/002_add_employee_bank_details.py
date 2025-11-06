"""Add employee bank details table

Revision ID: 002
Revises: 001
Create Date: 2025-11-06

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create employee_bank_details table
    op.create_table(
        'employee_bank_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('account_holder_name', sa.String(), nullable=False),
        sa.Column('account_number', sa.String(), nullable=False),
        sa.Column('bank_name', sa.String(), nullable=False),
        sa.Column('branch_name', sa.String()),
        sa.Column('ifsc_code', sa.String(), nullable=False),
        sa.Column('account_type', sa.String()),
        sa.Column('pan_number', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_id')
    )


def downgrade() -> None:
    op.drop_table('employee_bank_details')
