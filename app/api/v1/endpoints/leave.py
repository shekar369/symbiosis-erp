from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.leave import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestResponse,
    LeaveBalanceResponse,
    LeaveTypeResponse
)
from app.crud.leave import leave_request, leave_balance, leave_type

router = APIRouter()


@router.get("/requests", response_model=List[LeaveRequestResponse])
async def list_leave_requests(
    skip: int = 0,
    limit: int = 20,
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all leave requests or filter by employee"""
    if employee_id:
        return leave_request.get_by_employee(db=db, employee_id=employee_id, skip=skip, limit=limit)
    return leave_request.get_multi(db=db, skip=skip, limit=limit)


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


@router.get("/balance/{employee_id}", response_model=List[LeaveBalanceResponse])
async def get_leave_balance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get leave balance for an employee"""
    return leave_balance.get_by_employee(db=db, employee_id=employee_id)


@router.get("/types", response_model=List[LeaveTypeResponse])
async def list_leave_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all active leave types"""
    return leave_type.get_active(db=db)
