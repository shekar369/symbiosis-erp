"""Initial database migration

Revision ID: 001
Revises: 
Create Date: 2025-10-31

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from app.models.employee import EmployeeStatus
from app.models.location import FacilityType, ActType


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tenants table
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String()),
        sa.Column('address', sa.String()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('full_name', sa.String()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id')),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Create states table
    op.create_table(
        'states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(2), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('code')
    )

    # Create departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create designations table
    op.create_table(
        'designations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create grades table
    op.create_table(
        'grades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('state_id', sa.Integer(), sa.ForeignKey('states.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('facility_type', sa.Enum(FacilityType), default=FacilityType.REGULAR),
        sa.Column('act_type', sa.Enum(ActType), nullable=False),
        sa.Column('address_line1', sa.String(), nullable=False),
        sa.Column('address_line2', sa.String()),
        sa.Column('postal_code', sa.String(6), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('employee_code', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String()),
        sa.Column('date_of_birth', sa.Date()),
        sa.Column('date_of_joining', sa.Date(), nullable=False),
        sa.Column('date_of_leaving', sa.Date()),
        sa.Column('status', sa.Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE),
        sa.Column('department_id', sa.Integer(), sa.ForeignKey('departments.id')),
        sa.Column('designation_id', sa.Integer(), sa.ForeignKey('designations.id')),
        sa.Column('grade_id', sa.Integer(), sa.ForeignKey('grades.id')),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_code'),
        sa.UniqueConstraint('email')
    )

    # Create employee_documents table
    op.create_table(
        'employee_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('document_type', sa.String()),
        sa.Column('document_number', sa.String()),
        sa.Column('file_path', sa.String()),
        sa.Column('uploaded_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create employee_addresses table
    op.create_table(
        'employee_addresses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('address_type', sa.String()),
        sa.Column('address_line1', sa.String()),
        sa.Column('address_line2', sa.String()),
        sa.Column('city', sa.String()),
        sa.Column('state', sa.String()),
        sa.Column('country', sa.String()),
        sa.Column('postal_code', sa.String()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create employee_location_assignments table
    op.create_table(
        'employee_location_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('location_id', sa.Integer(), sa.ForeignKey('locations.id'), nullable=False),
        sa.Column('from_date', sa.DateTime(), nullable=False),
        sa.Column('to_date', sa.DateTime()),
        sa.Column('is_current', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('employee_location_assignments')
    op.drop_table('employee_addresses')
    op.drop_table('employee_documents')
    op.drop_table('employees')
    op.drop_table('locations')
    op.drop_table('grades')
    op.drop_table('designations')
    op.drop_table('departments')
    op.drop_table('states')
    op.drop_table('users')
    op.drop_table('tenants')