"""Update attendance status enum to include weekly_off and holiday

Revision ID: 004
Revises: 003
Create Date: 2025-11-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Update attendance table to support new status types: weekly_off and holiday

    Note: SQLite doesn't support direct enum updates, so we're just documenting
    the change here. The application layer (SQLAlchemy model) already has the
    updated AttendanceStatus enum that includes WEEKLY_OFF and HOLIDAY.

    For SQLite, the status column is stored as VARCHAR, so no schema change needed.
    New status values will work automatically.
    """
    # No actual migration needed for SQLite since enum is stored as string
    pass


def downgrade() -> None:
    """
    Downgrade would remove weekly_off and holiday status types.

    Note: This doesn't actually modify the schema for SQLite.
    """
    pass
