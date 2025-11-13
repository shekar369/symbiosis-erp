from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.leave import LeaveRequest, LeaveBalance, LeaveType
from app.schemas.leave import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestResponse,
    LeaveBalanceResponse,
    LeaveTypeResponse,
    LeaveTypeCreate,
    LeaveTypeUpdate
)
from app.crud.leave import leave_request, leave_balance, leave_type

router = APIRouter()


@router.get("/requests", response_model=List[LeaveRequestResponse], response_model_exclude_none=False)
async def list_leave_requests(
    skip: int = 0,
    limit: int = 20,
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all leave requests or filter by employee"""
    # Fetch leave requests with leave_type relationship
    query = db.query(LeaveRequest).options(joinedload(LeaveRequest.leave_type))

    if employee_id:
        query = query.filter(LeaveRequest.employee_id == employee_id)

    requests = query.offset(skip).limit(limit).all()

    # Manually construct response with leave_type_name
    result = []
    for req in requests:
        result.append({
            "id": req.id,
            "employee_id": req.employee_id,
            "leave_type_id": req.leave_type_id,
            "leave_type_name": req.leave_type.name if req.leave_type else None,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "days": req.days,
            "reason": req.reason,
            "status": req.status,
            "approved_by": req.approved_by,
            "created_at": req.created_at,
            "updated_at": req.updated_at
        })

    return result


@router.get("/requests/pending", response_model=List[LeaveRequestResponse])
async def list_pending_requests(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all pending leave requests for approval"""
    return leave_request.get_pending_requests(db=db, skip=skip, limit=limit)


@router.get("/requests/{request_id}", response_model=LeaveRequestResponse)
async def get_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific leave request"""
    db_request = leave_request.get(db=db, id=request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return db_request


@router.post("/requests", response_model=LeaveRequestResponse)
async def create_leave_request(
    request_data: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new leave request"""
    # Calculate days
    start_date = request_data.start_date
    end_date = request_data.end_date
    days = (end_date - start_date).days + 1

    # Check leave balance
    balance = leave_balance.get_balance(
        db=db,
        employee_id=request_data.employee_id,
        leave_type_id=request_data.leave_type_id
    )

    if not balance or balance.balance_days < days:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient leave balance. Available: {balance.balance_days if balance else 0} days, Requested: {days} days"
        )

    # Create leave request with calculated days
    from app.models.leave import LeaveRequest, LeaveStatus
    new_request = LeaveRequest(
        employee_id=request_data.employee_id,
        leave_type_id=request_data.leave_type_id,
        start_date=start_date,
        end_date=end_date,
        days=days,
        reason=request_data.reason,
        status=LeaveStatus.PENDING
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


@router.put("/requests/{request_id}/approve")
async def approve_leave_request(
    request_id: int,
    remarks: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Approve a leave request"""
    result = leave_request.approve_request(
        db=db,
        request_id=request_id,
        approved_by=current_user.id,
        remarks=remarks
    )
    if not result:
        raise HTTPException(status_code=404, detail="Leave request not found or already processed")
    return {"message": "Leave request approved", "request": result}


@router.put("/requests/{request_id}/reject")
async def reject_leave_request(
    request_id: int,
    remarks: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reject a leave request"""
    result = leave_request.reject_request(
        db=db,
        request_id=request_id,
        rejected_by=current_user.id,
        remarks=remarks
    )
    if not result:
        raise HTTPException(status_code=404, detail="Leave request not found or already processed")
    return {"message": "Leave request rejected", "request": result}


@router.delete("/requests/{request_id}")
async def cancel_leave_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancel a leave request"""
    # Get the leave request
    db_request = db.query(leave_request.model).filter(leave_request.model.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    # Only allow cancellation of pending requests
    if db_request.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending leave requests can be cancelled")

    # Delete the request
    db.delete(db_request)
    db.commit()

    return {"message": "Leave request cancelled successfully"}


@router.get("/balance/{employee_id}", response_model=List[LeaveBalanceResponse], response_model_exclude_none=False)
async def get_leave_balance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get leave balance for an employee"""
    # Fetch leave balances with leave_type relationship
    balances = db.query(LeaveBalance).options(
        joinedload(LeaveBalance.leave_type)
    ).filter(LeaveBalance.employee_id == employee_id).all()

    # Manually construct response with leave_type_name and aliased fields
    result = []
    for bal in balances:
        result.append({
            "id": bal.id,
            "employee_id": bal.employee_id,
            "leave_type_id": bal.leave_type_id,
            "leave_type_name": bal.leave_type.name if bal.leave_type else None,
            "year": bal.year,
            "total_days": bal.total_days,
            "used_days": bal.used_days,
            "balance_days": bal.balance_days,
            "balance": bal.balance_days,  # Alias for frontend
            "used": bal.used_days  # Alias for frontend
        })

    return result


@router.get("/types", response_model=List[LeaveTypeResponse])
async def list_leave_types(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all leave types (active by default, or all if include_inactive=True)"""
    if include_inactive:
        return leave_type.get_all(db=db, tenant_id=current_user.tenant_id)
    return leave_type.get_active(db=db, tenant_id=current_user.tenant_id)


@router.get("/types/{leave_type_id}", response_model=LeaveTypeResponse)
async def get_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific leave type"""
    db_leave_type = leave_type.get_by_id(db=db, leave_type_id=leave_type_id, tenant_id=current_user.tenant_id)
    if not db_leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return db_leave_type


@router.post("/types", response_model=LeaveTypeResponse)
async def create_leave_type(
    leave_type_data: LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new leave type (admin/employer only)"""
    # Check if leave type code already exists
    existing = leave_type.get_by_code(db=db, code=leave_type_data.code, tenant_id=current_user.tenant_id)
    if existing:
        raise HTTPException(status_code=400, detail="Leave type with this code already exists")

    return leave_type.create(db=db, leave_type=leave_type_data, tenant_id=current_user.tenant_id)


@router.put("/types/{leave_type_id}", response_model=LeaveTypeResponse)
async def update_leave_type(
    leave_type_id: int,
    leave_type_data: LeaveTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a leave type (admin/employer only)"""
    updated = leave_type.update(
        db=db,
        leave_type_id=leave_type_id,
        leave_type_update=leave_type_data,
        tenant_id=current_user.tenant_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return updated


@router.delete("/types/{leave_type_id}")
async def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete (soft delete) a leave type (admin/employer only)"""
    success = leave_type.delete(db=db, leave_type_id=leave_type_id, tenant_id=current_user.tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return {"message": "Leave type deactivated successfully"}
