from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import verify_password, create_access_token
from app.crud import user as user_crud

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_username(db, username=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Check if user role is valid
    valid_roles = ["saas_admin", "employer_admin", "employee", "auditor"]
    if user.role not in valid_roles and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user role"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "tenant_id": user.tenant_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "tenant_id": user.tenant_id
        }
    }


from pydantic import BaseModel as _BaseModel, EmailStr


class UserRegisterRequest(_BaseModel):
    username: str
    email: str
    password: str
    full_name: str = None
    tenant_id: int = None
    role: str = "employee"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Self-service registration endpoint.
    Creates an employee-role user by default; higher roles must be set by a SaaS admin.
    """
    from app.crud.user import user as user_crud
    from app.core.security import get_password_hash
    from app.models.user import User as UserModel

    if user_crud.get_user_by_username(db, payload.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )
    if user_crud.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Restrict self-registration to employee and auditor roles only
    allowed_roles = {"employee", "auditor"}
    role = payload.role if payload.role in allowed_roles else "employee"

    new_user = UserModel(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=role,
        tenant_id=payload.tenant_id,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={
            "sub": new_user.username,
            "role": new_user.role,
            "is_superuser": False,
            "tenant_id": new_user.tenant_id,
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
            "tenant_id": new_user.tenant_id,
        },
    }
