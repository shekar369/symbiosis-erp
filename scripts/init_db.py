import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine

# Import required models
from app.models.user import User
from app.models.config import SystemConfig

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()