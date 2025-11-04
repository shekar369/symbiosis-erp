from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.registration import OrganizationRegistration
from app.schemas.registration import OrganizationRegistrationCreate, OrganizationRegistrationUpdate, RegistrationStatus


def create_registration(db: Session, registration: OrganizationRegistrationCreate) -> OrganizationRegistration:
    db_registration = OrganizationRegistration(
        **registration.model_dump(),
        status=RegistrationStatus.PENDING
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration


def get_registration(db: Session, registration_id: int) -> Optional[OrganizationRegistration]:
    return db.query(OrganizationRegistration).filter(
        OrganizationRegistration.id == registration_id
    ).first()


def get_registration_by_email(db: Session, email: str) -> Optional[OrganizationRegistration]:
    return db.query(OrganizationRegistration).filter(
        OrganizationRegistration.email == email
    ).first()


def get_registrations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[RegistrationStatus] = None
) -> List[OrganizationRegistration]:
    query = db.query(OrganizationRegistration)
    if status:
        query = query.filter(OrganizationRegistration.status == status)
    return query.offset(skip).limit(limit).all()


def update_registration_status(
    db: Session,
    registration: OrganizationRegistration,
    update_data: OrganizationRegistrationUpdate,
    reviewer_id: int
) -> OrganizationRegistration:
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(registration, field, value)
    
    registration.reviewed_by = reviewer_id
    registration.reviewed_at = datetime.utcnow()
    
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


def get_pending_registrations(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[OrganizationRegistration]:
    return db.query(OrganizationRegistration).filter(
        OrganizationRegistration.status == RegistrationStatus.PENDING
    ).offset(skip).limit(limit).all()


def get_registration_count_by_status(db: Session) -> dict:
    counts = {}
    for status in RegistrationStatus:
        count = db.query(OrganizationRegistration).filter(
            OrganizationRegistration.status == status
        ).count()
        counts[status] = count
    return counts