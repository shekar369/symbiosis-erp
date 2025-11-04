from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
# Import all models to ensure they're registered with SQLAlchemy
import app.models


def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)


def create_initial_data(db: Session):
    """
    Create initial data for the application
    """
    # TODO: Create superuser
    # TODO: Create default tenant
    # TODO: Create default roles
    pass
