from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/logs")
async def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # TODO: Implement audit log listing
    return {"message": "Audit logs - to be implemented"}
