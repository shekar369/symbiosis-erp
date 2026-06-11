from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, func
from typing import Optional
from datetime import date

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.attendance import Attendance, AttendanceStatus
from app.models.employee import Employee
from app.models.wage import WageStatement, WageStatus

router = APIRouter()


@router.get("/attendance")
async def attendance_report(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, description="Year"),
    employee_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Monthly attendance summary for the authenticated tenant.
    Returns per-employee counts: present, absent, half-day, leave, weekly-off, holiday.
    """
    query = (
        db.query(
            Employee.id.label("employee_id"),
            Employee.employee_code,
            Employee.first_name,
            Employee.last_name,
            func.count(Attendance.id).label("total_recorded"),
            func.sum(
                (Attendance.status == AttendanceStatus.PRESENT).cast(int)
            ).label("present"),
            func.sum(
                (Attendance.status == AttendanceStatus.ABSENT).cast(int)
            ).label("absent"),
            func.sum(
                (Attendance.status == AttendanceStatus.HALF_DAY).cast(int)
            ).label("half_day"),
            func.sum(
                (Attendance.status == AttendanceStatus.LEAVE).cast(int)
            ).label("leave"),
            func.sum(
                (Attendance.status == AttendanceStatus.WEEKLY_OFF).cast(int)
            ).label("weekly_off"),
            func.sum(
                (Attendance.status == AttendanceStatus.HOLIDAY).cast(int)
            ).label("holiday"),
        )
        .join(Attendance, Employee.id == Attendance.employee_id, isouter=True)
        .filter(
            Employee.tenant_id == current_user.tenant_id,
            extract("month", Attendance.date) == month,
            extract("year", Attendance.date) == year,
        )
    )

    if employee_id:
        query = query.filter(Employee.id == employee_id)

    rows = query.group_by(
        Employee.id, Employee.employee_code, Employee.first_name, Employee.last_name
    ).all()

    return {
        "month": month,
        "year": year,
        "records": [
            {
                "employee_id": r.employee_id,
                "employee_code": r.employee_code,
                "name": f"{r.first_name} {r.last_name}",
                "total_recorded": r.total_recorded or 0,
                "present": int(r.present or 0),
                "absent": int(r.absent or 0),
                "half_day": int(r.half_day or 0),
                "leave": int(r.leave or 0),
                "weekly_off": int(r.weekly_off or 0),
                "holiday": int(r.holiday or 0),
            }
            for r in rows
        ],
    }


@router.get("/payroll")
async def payroll_report(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    status: Optional[str] = Query(None, description="Filter by status: calculated|approved|paid"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Monthly payroll summary for the authenticated tenant.
    Returns per-employee net salary, earnings, deductions, and status.
    """
    query = (
        db.query(WageStatement, Employee)
        .join(Employee, WageStatement.employee_id == Employee.id)
        .filter(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
        )
    )
    if status:
        query = query.filter(WageStatement.status == status)

    rows = query.all()

    total_gross = sum(r.WageStatement.total_earnings or 0 for r in rows)
    total_deductions = sum(r.WageStatement.total_deductions or 0 for r in rows)
    total_net = sum(r.WageStatement.net_salary or 0 for r in rows)

    return {
        "month": month,
        "year": year,
        "summary": {
            "total_employees": len(rows),
            "total_gross": round(total_gross, 2),
            "total_deductions": round(total_deductions, 2),
            "total_net": round(total_net, 2),
        },
        "records": [
            {
                "employee_id": r.Employee.id,
                "employee_code": r.Employee.employee_code,
                "name": f"{r.Employee.first_name} {r.Employee.last_name}",
                "basic_salary": r.WageStatement.basic_salary or 0,
                "total_earnings": r.WageStatement.total_earnings or 0,
                "total_deductions": r.WageStatement.total_deductions or 0,
                "net_salary": r.WageStatement.net_salary or 0,
                "present_days": r.WageStatement.present_days or 0,
                "absent_days": r.WageStatement.absent_days or 0,
                "status": r.WageStatement.status,
            }
            for r in rows
        ],
    }


@router.get("/salary-register")
async def salary_register(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Detailed salary register including earnings and deductions breakdown."""
    rows = (
        db.query(WageStatement, Employee)
        .join(Employee, WageStatement.employee_id == Employee.id)
        .filter(
            Employee.tenant_id == current_user.tenant_id,
            WageStatement.month == month,
            WageStatement.year == year,
        )
        .all()
    )

    return {
        "month": month,
        "year": year,
        "records": [
            {
                "employee_id": r.Employee.id,
                "employee_code": r.Employee.employee_code,
                "name": f"{r.Employee.first_name} {r.Employee.last_name}",
                "earnings": r.WageStatement.earnings_breakdown or {},
                "deductions": r.WageStatement.deductions_breakdown or {},
                "net_salary": r.WageStatement.net_salary or 0,
                "status": r.WageStatement.status,
            }
            for r in rows
        ],
    }
