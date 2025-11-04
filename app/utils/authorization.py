from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import TypeVar, Optional, Type

from app.models.user import User

T = TypeVar('T')


def verify_tenant_access(
    resource: Optional[T],
    current_user: User,
    resource_name: str = "Resource",
    not_found_message: Optional[str] = None
) -> T:
    """
    Verify that a resource exists and belongs to the current user's tenant

    Args:
        resource: The resource to check (can be None)
        current_user: Current authenticated user
        resource_name: Name of resource type for error messages
        not_found_message: Custom message for 404 error

    Returns:
        The resource if access is granted

    Raises:
        HTTPException: 404 if resource not found, 403 if access denied
    """
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=not_found_message or f"{resource_name} not found"
        )

    # Check if resource has tenant_id attribute
    if hasattr(resource, 'tenant_id'):
        if resource.tenant_id != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied to {resource_name}"
            )

    return resource


def verify_tenant_ownership(
    resource: Optional[T],
    current_user: User,
    owner_id_field: str = "user_id",
    resource_name: str = "Resource"
) -> T:
    """
    Verify that a resource belongs to the current user (not just tenant)

    Args:
        resource: The resource to check
        current_user: Current authenticated user
        owner_id_field: Field name that contains owner user ID
        resource_name: Name of resource for error messages

    Returns:
        The resource if ownership is verified

    Raises:
        HTTPException: 404 if not found, 403 if not owner
    """
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} not found"
        )

    owner_id = getattr(resource, owner_id_field, None)
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: not {resource_name} owner"
        )

    # Also verify tenant access
    return verify_tenant_access(resource, current_user, resource_name)


def require_admin(current_user: User) -> User:
    """
    Verify that current user has admin role

    Args:
        current_user: Current authenticated user

    Returns:
        The user if they are admin

    Raises:
        HTTPException: 403 if not admin
    """
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
