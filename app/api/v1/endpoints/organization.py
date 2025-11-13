from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.schemas.organization import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    DesignationCreate, DesignationUpdate, DesignationResponse,
    GradeCreate, GradeUpdate, GradeResponse
)
from app.models.organization import Department, Designation, Grade
from app.models.user import User

router = APIRouter()


# ==================== Department Endpoints ====================

@router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all departments for the current tenant"""
    departments = db.query(Department).filter(
        Department.tenant_id == current_user.tenant_id
    ).offset(skip).limit(limit).all()
    return departments


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific department"""
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.tenant_id == current_user.tenant_id
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new department"""
    # Check if code already exists for this tenant
    existing = db.query(Department).filter(
        Department.code == department.code,
        Department.tenant_id == current_user.tenant_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Department code already exists")

    db_department = Department(
        **department.model_dump(),
        tenant_id=current_user.tenant_id
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.put("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a department"""
    db_department = db.query(Department).filter(
        Department.id == department_id,
        Department.tenant_id == current_user.tenant_id
    ).first()

    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = department.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_department, field, value)

    db.commit()
    db.refresh(db_department)
    return db_department


@router.delete("/departments/{department_id}")
async def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a department"""
    db_department = db.query(Department).filter(
        Department.id == department_id,
        Department.tenant_id == current_user.tenant_id
    ).first()

    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(db_department)
    db.commit()
    return {"message": "Department deleted successfully"}


# ==================== Designation Endpoints ====================

@router.get("/designations", response_model=List[DesignationResponse])
async def list_designations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all designations for the current tenant"""
    designations = db.query(Designation).filter(
        Designation.tenant_id == current_user.tenant_id
    ).offset(skip).limit(limit).all()
    return designations


@router.get("/designations/{designation_id}", response_model=DesignationResponse)
async def get_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific designation"""
    designation = db.query(Designation).filter(
        Designation.id == designation_id,
        Designation.tenant_id == current_user.tenant_id
    ).first()

    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    return designation


@router.post("/designations", response_model=DesignationResponse)
async def create_designation(
    designation: DesignationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new designation"""
    # Check if code already exists for this tenant
    existing = db.query(Designation).filter(
        Designation.code == designation.code,
        Designation.tenant_id == current_user.tenant_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Designation code already exists")

    db_designation = Designation(
        **designation.model_dump(),
        tenant_id=current_user.tenant_id
    )
    db.add(db_designation)
    db.commit()
    db.refresh(db_designation)
    return db_designation


@router.put("/designations/{designation_id}", response_model=DesignationResponse)
async def update_designation(
    designation_id: int,
    designation: DesignationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a designation"""
    db_designation = db.query(Designation).filter(
        Designation.id == designation_id,
        Designation.tenant_id == current_user.tenant_id
    ).first()

    if not db_designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    update_data = designation.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_designation, field, value)

    db.commit()
    db.refresh(db_designation)
    return db_designation


@router.delete("/designations/{designation_id}")
async def delete_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a designation"""
    db_designation = db.query(Designation).filter(
        Designation.id == designation_id,
        Designation.tenant_id == current_user.tenant_id
    ).first()

    if not db_designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    db.delete(db_designation)
    db.commit()
    return {"message": "Designation deleted successfully"}


# ==================== Grade Endpoints ====================

@router.get("/grades", response_model=List[GradeResponse])
async def list_grades(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all grades for the current tenant"""
    grades = db.query(Grade).filter(
        Grade.tenant_id == current_user.tenant_id
    ).offset(skip).limit(limit).all()
    return grades


@router.get("/grades/{grade_id}", response_model=GradeResponse)
async def get_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific grade"""
    grade = db.query(Grade).filter(
        Grade.id == grade_id,
        Grade.tenant_id == current_user.tenant_id
    ).first()

    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    return grade


@router.post("/grades", response_model=GradeResponse)
async def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new grade"""
    # Check if code already exists for this tenant
    existing = db.query(Grade).filter(
        Grade.code == grade.code,
        Grade.tenant_id == current_user.tenant_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Grade code already exists")

    db_grade = Grade(
        **grade.model_dump(),
        tenant_id=current_user.tenant_id
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a grade"""
    db_grade = db.query(Grade).filter(
        Grade.id == grade_id,
        Grade.tenant_id == current_user.tenant_id
    ).first()

    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    update_data = grade.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_grade, field, value)

    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.delete("/grades/{grade_id}")
async def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a grade"""
    db_grade = db.query(Grade).filter(
        Grade.id == grade_id,
        Grade.tenant_id == current_user.tenant_id
    ).first()

    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    db.delete(db_grade)
    db.commit()
    return {"message": "Grade deleted successfully"}
