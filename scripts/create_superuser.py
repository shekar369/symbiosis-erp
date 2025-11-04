import sys
sys.path.append(".")

from app.db.session import SessionLocal
from app.crud.user import user as user_crud
from app.core.constants import ROLE_SUPER_ADMIN


def create_superuser():
    db = SessionLocal()

    try:
        # Check if superuser already exists
        existing_user = user_crud.get_user_by_username(db, username="admin")
        if existing_user:
            print("Superuser already exists")
            return

        # Create superuser
        superuser = user_crud.create_user(
            db=db,
            username="admin",
            email="admin@example.com",
            password="admin123",  # Change this in production
            tenant_id=1,
            role=ROLE_SUPER_ADMIN
        )

        print(f"Superuser created: {superuser.username}")

    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()
