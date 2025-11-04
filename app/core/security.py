from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64

from app.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__rounds=12
)

# Initialize Fernet cipher with key derived from settings
ENCRYPTION_KEY = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
cipher_suite = Fernet(ENCRYPTION_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt. Fails fast if bcrypt is unavailable."""
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # Do NOT fall back to weak hashing - fail fast instead
        import logging
        logging.critical(f"Password hashing failed: {str(e)}")
        raise RuntimeError(
            "Password hashing system is unavailable. "
            "Please check bcrypt installation."
        ) from e


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def encrypt_value(value: str) -> str:
    """Encrypt a string value"""
    if not value:
        return value
    encoded = cipher_suite.encrypt(value.encode())
    return encoded.decode()


def decrypt_value(encrypted_value: str) -> str:
    """Decrypt an encrypted string value"""
    if not encrypted_value:
        return encrypted_value
    try:
        decrypted = cipher_suite.decrypt(encrypted_value.encode())
        return decrypted.decode()
    except Exception as e:
        import logging
        logging.error(f"Failed to decrypt value: {str(e)}")
        return None
