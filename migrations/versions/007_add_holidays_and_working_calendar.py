"""Add holidays and working calendar tables

Revision ID: 007
Revises: 006
Create Date: 2025-11-14

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create holidays table
    op.create_table(
        'holidays',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('is_mandatory', sa.Boolean(), default=True),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_holidays_tenant_id', 'holidays', ['tenant_id'])
    op.create_index('ix_holidays_date', 'holidays', ['date'])

    # Create working_calendars table
    op.create_table(
        'working_calendars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('monday', sa.Boolean(), default=True),
        sa.Column('tuesday', sa.Boolean(), default=True),
        sa.Column('wednesday', sa.Boolean(), default=True),
        sa.Column('thursday', sa.Boolean(), default=True),
        sa.Column('friday', sa.Boolean(), default=True),
        sa.Column('saturday', sa.Boolean(), default=False),
        sa.Column('sunday', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_working_calendars_tenant_id', 'working_calendars', ['tenant_id'])


def downgrade() -> None:
    # Drop working_calendars table
    op.drop_index('ix_working_calendars_tenant_id')
    op.drop_table('working_calendars')

    # Drop holidays table
    op.drop_index('ix_holidays_date')
    op.drop_index('ix_holidays_tenant_id')
    op.drop_table('holidays')
