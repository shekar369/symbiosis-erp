from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, dict, dict]):
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, username: str, email: str, password: str, tenant_id: int, role: str) -> User:
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            tenant_id=tenant_id,
            role=role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user = CRUDUser(User)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return user.get_user_by_username(db, username)
