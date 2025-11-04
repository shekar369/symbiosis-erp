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


@router.post("/register")
async def register(db: Session = Depends(get_db)):
    # TODO: Implement user registration
    return {"message": "Registration endpoint - to be implemented"}
