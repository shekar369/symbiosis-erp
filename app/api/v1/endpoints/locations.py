from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api.dependencies import get_db, get_current_active_user, check_role_access
from app.models.user import User
from app.models.location import Location, State, EmployeeLocationAssignment, FacilityType, ActType
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationResponse,
    StateCreate,
    StateResponse,
    EmployeeLocationAssignmentCreate,
    EmployeeLocationAssignmentUpdate,
    EmployeeLocationAssignmentResponse,
)

router = APIRouter()


# State Endpoints
@router.get("/states", response_model=List[StateResponse])
def get_states(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin", "saas_admin")),
    is_active: bool = True,
    skip: int = 0,
    limit: int = 100
):
    """Get all states with optional filters"""
    query = db.query(State)
    if is_active:
        query = query.filter(State.is_active == True)
    return query.offset(skip).limit(limit).all()


@router.post("/states", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
def create_state(
    state_in: StateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("saas_admin")),
):
    """Create a new state (SaaS Admin only)"""
    # Check if state already exists
    existing = db.query(State).filter(
        (State.code == state_in.code) | (State.name == state_in.name)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="State with this code or name already exists"
        )

    state = State(**state_in.dict())
    db.add(state)
    db.commit()
    db.refresh(state)
    return state
    return state


# Location Endpoints
@router.get("/", response_model=List[LocationResponse])
def get_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin", "saas_admin")),
    state_id: Optional[int] = None,
    facility_type: Optional[FacilityType] = None,
    act_type: Optional[ActType] = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 100
):
    """Get locations with filters"""
    query = db.query(Location)
    
    # Apply role-based filtering
    if current_user.role != "saas_admin":
        query = query.filter(Location.tenant_id == current_user.tenant_id)

    # Apply filters
    if state_id:
        query = query.filter(Location.state_id == state_id)
    if facility_type:
        query = query.filter(Location.facility_type == facility_type)
    if act_type:
        query = query.filter(Location.act_type == act_type)
    if is_active is not None:
        query = query.filter(Location.is_active == is_active)

    return query.offset(skip).limit(limit).all()


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin", "saas_admin"))
):
    """Get a specific location"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    # Check access
    if current_user.role != "saas_admin" and location.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return location


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location_in: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin")),
):
    """Create a new location"""
    # Verify tenant_id matches current user's tenant
    if location_in.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create location for another tenant"
        )

    # Verify state exists
    state = db.query(State).filter(State.id == location_in.state_id).first()
    if not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state_id"
        )

    # Create location
    location = Location(**location_in.dict())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    *,
    location_id: int,
    location_in: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin"))
):
    """Update a location"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    # Check permissions
    if location.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Update location
    for field, value in location_in.dict(exclude_unset=True).items():
        setattr(location, field, value)
    
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    *,
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin"))
):
    """Soft delete a location by marking it inactive"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )

    # Check permissions
    if location.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Soft delete
    location.is_active = False
    db.add(location)
    db.commit()


# Employee Location Assignment Endpoints
@router.post("/assignments", response_model=EmployeeLocationAssignmentResponse)
def create_employee_assignment(
    *,
    assignment_in: EmployeeLocationAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin"))
):
    """Assign an employee to a location"""
    # Verify location belongs to current tenant
    location = db.query(Location).filter(Location.id == assignment_in.location_id).first()
    if not location or location.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid location"
        )

    # End any current assignment
    current = (
        db.query(EmployeeLocationAssignment)
        .filter(
            EmployeeLocationAssignment.employee_id == assignment_in.employee_id,
            EmployeeLocationAssignment.is_current == True
        )
        .first()
    )
    if current:
        current.is_current = False
        current.to_date = datetime.utcnow()
        db.add(current)

    # Create new assignment
    assignment = EmployeeLocationAssignment(**assignment_in.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get(
    "/assignments/employee/{employee_id}",
    response_model=List[EmployeeLocationAssignmentResponse]
)
def get_employee_assignments(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role_access("employer_admin")),
    include_inactive: bool = False
):
    """Get location assignment history for an employee"""
    query = (
        db.query(EmployeeLocationAssignment)
        .join(Location)
        .filter(
            EmployeeLocationAssignment.employee_id == employee_id,
            Location.tenant_id == current_user.tenant_id
        )
    )
    
    if not include_inactive:
        query = query.filter(EmployeeLocationAssignment.is_current == True)
    
    return query.all()
    location_data["tenant_id"] = current_user.tenant_id

    location = Location(**location_data)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific location"""
    location = db.query(Location).filter(
        Location.id == location_id,
        Location.tenant_id == current_user.tenant_id
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location_in: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a location"""
    location = db.query(Location).filter(
        Location.id == location_id,
        Location.tenant_id == current_user.tenant_id
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Update only provided fields
    update_data = location_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a location (soft delete by marking inactive)"""
    location = db.query(Location).filter(
        Location.id == location_id,
        Location.tenant_id == current_user.tenant_id
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    location.is_active = False
    db.commit()
    return None


# Employee Location Assignment Endpoints
@router.post("/assignments", response_model=EmployeeLocationAssignmentResponse)
def assign_employee_to_location(
    assignment_in: EmployeeLocationAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Assign an employee to a location"""
    # Mark previous assignments as not current
    if assignment_in.is_current:
        previous_assignments = db.query(EmployeeLocationAssignment).filter(
            EmployeeLocationAssignment.employee_id == assignment_in.employee_id,
            EmployeeLocationAssignment.is_current == True
        ).all()

        for prev in previous_assignments:
            prev.is_current = False

    assignment = EmployeeLocationAssignment(**assignment_in.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/assignments/employee/{employee_id}", response_model=List[EmployeeLocationAssignmentResponse])
def get_employee_location_history(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get location assignment history for an employee"""
    assignments = db.query(EmployeeLocationAssignment).filter(
        EmployeeLocationAssignment.employee_id == employee_id
    ).all()
    return assignments
