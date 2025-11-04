# SQLAlchemy models - Import all models here for proper relationship resolution
from app.db.base import Base
from app.models.tenant import Tenant
from app.models.user import User, AuditLog
from app.models.organization import Department, Designation, Grade
from app.models.employee import Employee, EmployeeAddress, EmployeeDocument
from app.models.location import State, Location, EmployeeLocationAssignment
from app.models.leave import LeaveType, LeaveBalance, LeaveRequest
from app.models.holiday import Holiday, WorkingCalendar
from app.models.shift import Shift, ShiftAssignment
from app.models.salary import SalaryComponent, EmployeeSalaryConfig
from app.models.attendance import Attendance, AttendanceUpload
from app.models.wage import WageStatement
from app.models.overtime import Overtime
from app.models.advance_loan import Advance, Loan
from app.models.vendor import Vendor
from app.models.registration import OrganizationRegistration
from app.models.billing import Subscription, BillingInvoice, SubscriptionPlan
from app.models.config import SystemConfig

__all__ = [
    "Base",
    "Tenant",
    "User",
    "AuditLog",
    "Department",
    "Designation",
    "Grade",
    "Employee",
    "EmployeeAddress",
    "EmployeeDocument",
    "State",
    "Location",
    "EmployeeLocationAssignment",
    "LeaveType",
    "LeaveBalance",
    "LeaveRequest",
    "Holiday",
    "WorkingCalendar",
    "Shift",
    "ShiftAssignment",
    "SalaryComponent",
    "EmployeeSalaryConfig",
    "Attendance",
    "AttendanceUpload",
    "WageStatement",
    "Overtime",
    "Advance",
    "Loan",
    "Vendor",
    "OrganizationRegistration",
    "Subscription",
    "BillingInvoice",
    "SubscriptionPlan",
    "SystemConfig",
]
