import sys
sys.path.append(".")

from app.db.init_db import init_db


def initialize_database():
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
