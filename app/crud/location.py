from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.location import Location, State, EmployeeLocationAssignment, FacilityType, ActType
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    StateCreate,
    StateUpdate,
    EmployeeLocationAssignmentCreate,
    EmployeeLocationAssignmentUpdate
)


class CRUDState(CRUDBase[State, StateCreate, StateUpdate]):
    def get_by_code(self, db: Session, code: str) -> Optional[State]:
        """Get a state by its code."""
        return db.query(State).filter(State.code == code).first()
    
    def get_active_states(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[State]:
        """Get list of active states."""
        return (
            db.query(State)
            .filter(State.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        tenant_id: Optional[int] = None,
        state_id: Optional[int] = None,
        facility_type: Optional[FacilityType] = None,
        act_type: Optional[ActType] = None,
        is_active: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Location]:
        """Get locations with filters."""
        query = db.query(self.model)

        if tenant_id is not None:
            query = query.filter(self.model.tenant_id == tenant_id)
        if state_id is not None:
            query = query.filter(self.model.state_id == state_id)
        if facility_type is not None:
            query = query.filter(self.model.facility_type == facility_type)
        if act_type is not None:
            query = query.filter(self.model.act_type == act_type)
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)

        return query.offset(skip).limit(limit).all()
    
    def create_with_tenant(
        self, db: Session, *, obj_in: LocationCreate, tenant_id: int
    ) -> Location:
        """Create new location with tenant ID."""
        obj_in_data = obj_in.dict()
        obj_in_data["tenant_id"] = tenant_id
        db_obj = Location(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDEmployeeLocationAssignment(CRUDBase[
    EmployeeLocationAssignment,
    EmployeeLocationAssignmentCreate,
    EmployeeLocationAssignmentUpdate
]):
    def get_current_assignment(
        self, db: Session, *, employee_id: int
    ) -> Optional[EmployeeLocationAssignment]:
        """Get employee's current location assignment."""
        return (
            db.query(self.model)
            .filter(
                self.model.employee_id == employee_id,
                self.model.is_current == True
            )
            .first()
        )
    
    def get_employee_assignments(
        self,
        db: Session,
        *,
        employee_id: int,
        include_inactive: bool = False
    ) -> List[EmployeeLocationAssignment]:
        """Get employee's location assignment history."""
        query = (
            db.query(self.model)
            .filter(self.model.employee_id == employee_id)
        )
        if not include_inactive:
            query = query.filter(self.model.is_current == True)
        return query.all()
    
    def end_current_assignment(
        self, db: Session, *, employee_id: int
    ) -> Optional[EmployeeLocationAssignment]:
        """End employee's current location assignment."""
        current = self.get_current_assignment(db, employee_id=employee_id)
        if current:
            current.is_current = False
            current.to_date = datetime.utcnow()
            db.add(current)
            db.commit()
            db.refresh(current)
        return current
    
    def create_new_assignment(
        self,
        db: Session,
        *,
        obj_in: EmployeeLocationAssignmentCreate
    ) -> EmployeeLocationAssignment:
        """Create new location assignment and end current one if exists."""
        # End current assignment if any
        self.end_current_assignment(db, employee_id=obj_in.employee_id)
        
        # Create new assignment
        db_obj = EmployeeLocationAssignment(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


state = CRUDState(State)
location = CRUDLocation(Location)
employee_location = CRUDEmployeeLocationAssignment(EmployeeLocationAssignment)