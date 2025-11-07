"""Add comprehensive employee details

Revision ID: 005
Revises: 004
Create Date: 2025-11-07

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to employees table directly (no enum types for SQLite)
    op.add_column('employees', sa.Column('middle_name', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('gender', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('marital_status', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('father_husband_name', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('blood_group', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('alternate_phone', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('emergency_contact_name', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('emergency_contact_number', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('emergency_contact_relation', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('employment_type', sa.String(), nullable=True, server_default='permanent'))
    op.add_column('employees', sa.Column('probation_period_months', sa.Integer(), nullable=True))
    op.add_column('employees', sa.Column('confirmation_date', sa.Date(), nullable=True))
    op.add_column('employees', sa.Column('notice_period_days', sa.Integer(), nullable=True))
    op.add_column('employees', sa.Column('reporting_manager_id', sa.Integer(), nullable=True))

    # Create employee_salary_details table
    op.create_table(
        'employee_salary_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),

        # Salary Components
        sa.Column('basic_salary', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('hra', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('conveyance_allowance', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('medical_allowance', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('special_allowance', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('other_allowance', sa.Numeric(10, 2), nullable=True, server_default='0'),

        # Calculated Fields
        sa.Column('gross_salary', sa.Numeric(10, 2), nullable=True, server_default='0'),

        # Deductions
        sa.Column('pf_employee', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('pf_employer', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('esic_employee', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('esic_employer', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('professional_tax', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('tds', sa.Numeric(10, 2), nullable=True, server_default='0'),

        # Final Amounts
        sa.Column('total_deductions', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('net_salary', sa.Numeric(10, 2), nullable=True, server_default='0'),
        sa.Column('ctc', sa.Numeric(10, 2), nullable=True, server_default='0'),

        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_id')
    )

    # Create employee_statutory_details table
    op.create_table(
        'employee_statutory_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),

        # Statutory Numbers
        sa.Column('pan_number', sa.String(), nullable=True),
        sa.Column('aadhaar_number', sa.String(), nullable=True),
        sa.Column('uan_number', sa.String(), nullable=True),
        sa.Column('esic_number', sa.String(), nullable=True),

        # Applicability Flags
        sa.Column('pf_applicable', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('esic_applicable', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('lwf_applicable', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('pt_applicable', sa.Boolean(), nullable=True, server_default='true'),

        # Additional Info
        sa.Column('previous_employer_pf_number', sa.String(), nullable=True),
        sa.Column('date_of_exit_from_previous_pf', sa.Date(), nullable=True),

        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_id')
    )


def downgrade() -> None:
    # Drop tables
    op.drop_table('employee_statutory_details')
    op.drop_table('employee_salary_details')

    # Drop columns from employees table
    op.drop_column('employees', 'reporting_manager_id')
    op.drop_column('employees', 'notice_period_days')
    op.drop_column('employees', 'confirmation_date')
    op.drop_column('employees', 'probation_period_months')
    op.drop_column('employees', 'employment_type')
    op.drop_column('employees', 'emergency_contact_relation')
    op.drop_column('employees', 'emergency_contact_number')
    op.drop_column('employees', 'emergency_contact_name')
    op.drop_column('employees', 'alternate_phone')
    op.drop_column('employees', 'blood_group')
    op.drop_column('employees', 'father_husband_name')
    op.drop_column('employees', 'marital_status')
    op.drop_column('employees', 'gender')
    op.drop_column('employees', 'middle_name')
