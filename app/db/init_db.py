import logging
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
# Import all models so SQLAlchemy registers them before create_all
import app.models  # noqa: F401

logger = logging.getLogger(__name__)


def init_db():
    """Create all database tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialised")


def create_initial_data(db: Session):
    """
    Seed the database with the minimum data required to boot the application:
      - A default SaaS tenant
      - A superuser / SaaS-admin account
    Safe to call multiple times; existing records are skipped.
    """
    from app.models.tenant import Tenant
    from app.models.user import User
    from app.core.security import get_password_hash
    from app.config import settings

    # ── Default tenant ──────────────────────────────────────────────────────
    default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
    if not default_tenant:
        default_tenant = Tenant(
            name="Default Organisation",
            slug="default",
            email=getattr(settings, "FIRST_SUPERUSER_EMAIL", "admin@symbiosis.local"),
            is_active=True,
        )
        db.add(default_tenant)
        db.flush()  # Obtain the id without committing yet
        logger.info("Created default tenant (slug='default')")

    # ── Superuser / SaaS admin ──────────────────────────────────────────────
    superuser_email = getattr(settings, "FIRST_SUPERUSER_EMAIL", "admin@symbiosis.local")
    superuser_username = getattr(settings, "FIRST_SUPERUSER", "admin")
    superuser_password = getattr(settings, "FIRST_SUPERUSER_PASSWORD", "changeme123")

    existing = db.query(User).filter(User.username == superuser_username).first()
    if not existing:
        superuser = User(
            username=superuser_username,
            email=superuser_email,
            hashed_password=get_password_hash(superuser_password),
            role="saas_admin",
            full_name="System Administrator",
            is_active=True,
            is_superuser=True,
            tenant_id=default_tenant.id,
        )
        db.add(superuser)
        logger.info("Created superuser '%s'", superuser_username)

    db.commit()
    logger.info("Initial data seeding complete")
