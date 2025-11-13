"""
Create comprehensive test data with Indian employees and multiple stakeholders
"""
import os
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
import random

# Ensure DATABASE_URL is not set in environment
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.models.organization import Department, Designation, Grade
from app.models.employee import (
    Employee, EmployeeBankDetails,
    EmployeeSalaryDetails, EmployeeStatutoryDetails,
    EmployeeStatus
)
from app.core.security import get_password_hash

# Indian employee data
EMPLOYEES_DATA = [
    {
        "first_name": "Rajesh", "last_name": "Kumar", "middle_name": "Singh",
        "email": "rajesh.kumar@techinnovate.com", "phone": "+91-9876543210",
        "dob": date(1988, 3, 15), "gender": "male", "marital_status": "married",
        "father_name": "Suresh Kumar", "blood_group": "O+",
        "department": "Engineering", "designation": "Senior Software Engineer", "grade": "L3",
        "basic_salary": Decimal("85000"), "pan": "ABCDE1234F", "aadhaar": "234567890123",
        "bank": "HDFC Bank", "ifsc": "HDFC0001234", "branch": "Indiranagar, Bangalore"
    },
    {
        "first_name": "Priya", "last_name": "Sharma", "middle_name": "Devi",
        "email": "priya.sharma@techinnovate.com", "phone": "+91-9876543211",
        "dob": date(1992, 7, 22), "gender": "female", "marital_status": "single",
        "father_name": "Rakesh Sharma", "blood_group": "A+",
        "department": "Engineering", "designation": "Software Engineer", "grade": "L2",
        "basic_salary": Decimal("65000"), "pan": "BCDEF2345G", "aadhaar": "345678901234",
        "bank": "ICICI Bank", "ifsc": "ICIC0002345", "branch": "Koramangala, Bangalore"
    },
    {
        "first_name": "Amit", "last_name": "Patel", "middle_name": "Kumar",
        "email": "amit.patel@techinnovate.com", "phone": "+91-9876543212",
        "dob": date(1985, 11, 8), "gender": "male", "marital_status": "married",
        "father_name": "Mahesh Patel", "blood_group": "B+",
        "department": "Engineering", "designation": "Tech Lead", "grade": "L4",
        "basic_salary": Decimal("120000"), "pan": "CDEFG3456H", "aadhaar": "456789012345",
        "bank": "State Bank of India", "ifsc": "SBIN0003456", "branch": "MG Road, Bangalore"
    },
    {
        "first_name": "Sneha", "last_name": "Reddy", "middle_name": "",
        "email": "sneha.reddy@techinnovate.com", "phone": "+91-9876543213",
        "dob": date(1994, 5, 30), "gender": "female", "marital_status": "single",
        "father_name": "Venkat Reddy", "blood_group": "AB+",
        "department": "Human Resources", "designation": "HR Executive", "grade": "L2",
        "basic_salary": Decimal("55000"), "pan": "DEFGH4567I", "aadhaar": "567890123456",
        "bank": "Axis Bank", "ifsc": "UTIB0004567", "branch": "Whitefield, Bangalore"
    },
    {
        "first_name": "Vikram", "last_name": "Singh", "middle_name": "Pratap",
        "email": "vikram.singh@techinnovate.com", "phone": "+91-9876543214",
        "dob": date(1990, 1, 12), "gender": "male", "marital_status": "married",
        "father_name": "Rajendra Singh", "blood_group": "O-",
        "department": "Finance", "designation": "Senior Accountant", "grade": "L3",
        "basic_salary": Decimal("75000"), "pan": "EFGHI5678J", "aadhaar": "678901234567",
        "bank": "HDFC Bank", "ifsc": "HDFC0005678", "branch": "HSR Layout, Bangalore"
    },
    {
        "first_name": "Anjali", "last_name": "Desai", "middle_name": "Rajesh",
        "email": "anjali.desai@techinnovate.com", "phone": "+91-9876543215",
        "dob": date(1993, 9, 18), "gender": "female", "marital_status": "single",
        "father_name": "Rajesh Desai", "blood_group": "A-",
        "department": "Marketing", "designation": "Marketing Executive", "grade": "L2",
        "basic_salary": Decimal("60000"), "pan": "FGHIJ6789K", "aadhaar": "789012345678",
        "bank": "ICICI Bank", "ifsc": "ICIC0006789", "branch": "Jayanagar, Bangalore"
    },
    {
        "first_name": "Karthik", "last_name": "Iyer", "middle_name": "Ramesh",
        "email": "karthik.iyer@techinnovate.com", "phone": "+91-9876543216",
        "dob": date(1987, 4, 25), "gender": "male", "marital_status": "married",
        "father_name": "Ramesh Iyer", "blood_group": "B-",
        "department": "Engineering", "designation": "Senior Software Engineer", "grade": "L3",
        "basic_salary": Decimal("90000"), "pan": "GHIJK7890L", "aadhaar": "890123456789",
        "bank": "Kotak Mahindra Bank", "ifsc": "KKBK0007890", "branch": "Electronic City, Bangalore"
    },
    {
        "first_name": "Divya", "last_name": "Nair", "middle_name": "Krishna",
        "email": "divya.nair@techinnovate.com", "phone": "+91-9876543217",
        "dob": date(1995, 12, 5), "gender": "female", "marital_status": "single",
        "father_name": "Krishna Nair", "blood_group": "O+",
        "department": "Quality Assurance", "designation": "QA Engineer", "grade": "L2",
        "basic_salary": Decimal("58000"), "pan": "HIJKL8901M", "aadhaar": "901234567890",
        "bank": "State Bank of India", "ifsc": "SBIN0008901", "branch": "Marathahalli, Bangalore"
    },
    {
        "first_name": "Arjun", "last_name": "Menon", "middle_name": "Kumar",
        "email": "arjun.menon@techinnovate.com", "phone": "+91-9876543218",
        "dob": date(1989, 6, 14), "gender": "male", "marital_status": "married",
        "father_name": "Kumar Menon", "blood_group": "A+",
        "department": "Operations", "designation": "Operations Manager", "grade": "L4",
        "basic_salary": Decimal("110000"), "pan": "IJKLM9012N", "aadhaar": "012345678901",
        "bank": "Axis Bank", "ifsc": "UTIB0009012", "branch": "Bellandur, Bangalore"
    },
    {
        "first_name": "Pooja", "last_name": "Verma", "middle_name": "Kumari",
        "email": "pooja.verma@techinnovate.com", "phone": "+91-9876543219",
        "dob": date(1991, 8, 20), "gender": "female", "marital_status": "married",
        "father_name": "Ashok Verma", "blood_group": "AB-",
        "department": "Human Resources", "designation": "HR Manager", "grade": "L3",
        "basic_salary": Decimal("80000"), "pan": "JKLMN0123O", "aadhaar": "123456789013",
        "bank": "HDFC Bank", "ifsc": "HDFC0000123", "branch": "Sarjapur Road, Bangalore"
    }
]

def calculate_salary_components(basic):
    """Calculate salary components based on basic salary"""
    hra = basic * Decimal("0.40")  # 40% of basic
    conveyance = Decimal("1600")
    medical = Decimal("1250")
    special = basic * Decimal("0.20")  # 20% of basic

    gross = basic + hra + conveyance + medical + special

    # Deductions
    pf_emp = basic * Decimal("0.12")
    pf_empr = basic * Decimal("0.12")

    # ESIC applicable if gross < 21000
    if gross < 21000:
        esic_emp = gross * Decimal("0.0075")
        esic_empr = gross * Decimal("0.0325")
    else:
        esic_emp = Decimal("0")
        esic_empr = Decimal("0")

    pt = Decimal("200") if gross > 15000 else Decimal("0")
    tds = gross * Decimal("0.05") if gross > 50000 else Decimal("0")

    total_ded = pf_emp + esic_emp + pt + tds
    net = gross - total_ded
    ctc = gross + pf_empr + esic_empr

    return {
        "basic_salary": basic,
        "hra": hra,
        "conveyance_allowance": conveyance,
        "medical_allowance": medical,
        "special_allowance": special,
        "other_allowance": Decimal("0"),
        "gross_salary": gross,
        "pf_employee": pf_emp,
        "pf_employer": pf_empr,
        "esic_employee": esic_emp,
        "esic_employer": esic_empr,
        "professional_tax": pt,
        "tds": tds,
        "total_deductions": total_ded,
        "net_salary": net,
        "ctc": ctc
    }

def create_comprehensive_test_data():
    db: Session = SessionLocal()

    try:
        print("=" * 80)
        print("CREATING COMPREHENSIVE TEST DATA - TECH INNOVATE SOLUTIONS")
        print("=" * 80)

        # 1. Create/Get Tenant (Company)
        print("\n1. Setting up Company (Tenant)...")
        tenant = db.query(Tenant).filter(Tenant.slug == "techinnovate").first()
        if not tenant:
            tenant = Tenant(
                name="Tech Innovate Solutions Pvt Ltd",
                slug="techinnovate",
                email="info@techinnovate.com",
                phone="+91-80-41234567",
                address="123, MG Road, Bangalore, Karnataka 560001",
                is_active=True
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(f"   [CREATED] Company: {tenant.name}")
        else:
            print(f"   [EXISTS] Company: {tenant.name}")

        # 2. Create Employer Admin User
        print("\n2. Setting up Employer Admin...")
        employer_admin = db.query(User).filter(User.username == "employer").first()
        if not employer_admin:
            employer_admin = User(
                username="employer",
                email="employer@techinnovate.com",
                hashed_password=get_password_hash("employer123"),
                role="employer",
                full_name="Ravi Krishnan (Employer)",
                is_active=True,
                is_superuser=True,
                tenant_id=tenant.id
            )
            db.add(employer_admin)
            db.commit()
            db.refresh(employer_admin)
            print(f"   [CREATED] Employer Admin: {employer_admin.full_name}")
        else:
            print(f"   [EXISTS] Employer Admin: {employer_admin.full_name}")

        # 3. Create HR Manager User
        print("\n3. Setting up HR Manager...")
        hr_manager = db.query(User).filter(User.username == "hrmanager").first()
        if not hr_manager:
            hr_manager = User(
                username="hrmanager",
                email="hr@techinnovate.com",
                hashed_password=get_password_hash("hr123"),
                role="hr_manager",
                full_name="Meera Lakshmi (HR Manager)",
                is_active=True,
                is_superuser=False,
                tenant_id=tenant.id
            )
            db.add(hr_manager)
            db.commit()
            db.refresh(hr_manager)
            print(f"   [CREATED] HR Manager: {hr_manager.full_name}")
        else:
            print(f"   [EXISTS] HR Manager: {hr_manager.full_name}")

        # 4. Create Organization Structure
        print("\n4. Setting up Organization Structure...")

        departments = [
            {"name": "Engineering", "code": "TIS-ENG", "desc": "Engineering & Development"},
            {"name": "Human Resources", "code": "TIS-HR", "desc": "Human Resources"},
            {"name": "Finance", "code": "TIS-FIN", "desc": "Finance & Accounts"},
            {"name": "Marketing", "code": "TIS-MKT", "desc": "Marketing & Sales"},
            {"name": "Quality Assurance", "code": "TIS-QA", "desc": "Quality Assurance"},
            {"name": "Operations", "code": "TIS-OPS", "desc": "Operations"}
        ]

        dept_objects = {}
        for dept_data in departments:
            dept = db.query(Department).filter(
                Department.name == dept_data["name"],
                Department.tenant_id == tenant.id
            ).first()
            if not dept:
                dept = Department(
                    name=dept_data["name"],
                    code=dept_data["code"],
                    description=dept_data["desc"],
                    tenant_id=tenant.id
                )
                db.add(dept)
                db.commit()
                db.refresh(dept)
                print(f"   [CREATED] Department: {dept.name} ({dept.code})")
            else:
                print(f"   [EXISTS] Department: {dept.name} ({dept.code})")
            dept_objects[dept.name] = dept

        designations = [
            {"name": "Tech Lead", "code": "TIS-TL", "desc": "Technical Lead"},
            {"name": "Senior Software Engineer", "code": "TIS-SSE", "desc": "Senior Software Engineer"},
            {"name": "Software Engineer", "code": "TIS-SE", "desc": "Software Engineer"},
            {"name": "HR Manager", "code": "TIS-HRM", "desc": "HR Manager"},
            {"name": "HR Executive", "code": "TIS-HRE", "desc": "HR Executive"},
            {"name": "Senior Accountant", "code": "TIS-SAC", "desc": "Senior Accountant"},
            {"name": "Marketing Executive", "code": "TIS-MKE", "desc": "Marketing Executive"},
            {"name": "QA Engineer", "code": "TIS-QAE", "desc": "QA Engineer"},
            {"name": "Operations Manager", "code": "TIS-OPM", "desc": "Operations Manager"}
        ]

        desig_objects = {}
        for desig_data in designations:
            desig = db.query(Designation).filter(
                Designation.name == desig_data["name"],
                Designation.tenant_id == tenant.id
            ).first()
            if not desig:
                desig = Designation(
                    name=desig_data["name"],
                    code=desig_data["code"],
                    description=desig_data["desc"],
                    tenant_id=tenant.id
                )
                db.add(desig)
                db.commit()
                db.refresh(desig)
                print(f"   [CREATED] Designation: {desig.name} ({desig.code})")
            else:
                print(f"   [EXISTS] Designation: {desig.name} ({desig.code})")
            desig_objects[desig.name] = desig

        grades = [
            {"name": "L2", "code": "TIS-L2", "desc": "Level 2 - Junior"},
            {"name": "L3", "code": "TIS-L3", "desc": "Level 3 - Mid Level"},
            {"name": "L4", "code": "TIS-L4", "desc": "Level 4 - Senior"}
        ]

        grade_objects = {}
        for grade_data in grades:
            grade = db.query(Grade).filter(
                Grade.name == grade_data["name"],
                Grade.tenant_id == tenant.id
            ).first()
            if not grade:
                grade = Grade(
                    name=grade_data["name"],
                    code=grade_data["code"],
                    description=grade_data["desc"],
                    tenant_id=tenant.id
                )
                db.add(grade)
                db.commit()
                db.refresh(grade)
                print(f"   [CREATED] Grade: {grade.name} ({grade.code})")
            else:
                print(f"   [EXISTS] Grade: {grade.name} ({grade.code})")
            grade_objects[grade.name] = grade

        # 5. Create 10 Employees with complete details
        print("\n5. Creating 10 Employees with Complete Details...")
        print("-" * 80)

        employee_ids = []
        base_date = date(2020, 1, 1)

        for idx, emp_data in enumerate(EMPLOYEES_DATA, 1):
            print(f"\n   Employee {idx}/10: {emp_data['first_name']} {emp_data['last_name']}")

            # Check if employee exists
            employee = db.query(Employee).filter(
                Employee.email == emp_data['email']
            ).first()

            if employee:
                print(f"   [EXISTS] Employee already exists")
                employee_ids.append(employee.id)
                continue

            # Random joining date in last 3 years
            days_ago = random.randint(30, 1095)
            joining_date = base_date + timedelta(days=days_ago)
            confirmation_date = joining_date + timedelta(days=180)  # 6 months probation

            # Create employee
            employee = Employee(
                tenant_id=tenant.id,
                employee_code=f"TIS{1000 + idx}",
                first_name=emp_data["first_name"],
                last_name=emp_data["last_name"],
                middle_name=emp_data["middle_name"],
                email=emp_data["email"],
                phone=emp_data["phone"],
                alternate_phone=f"+91-98765432{20 + idx}",
                date_of_birth=emp_data["dob"],
                gender=emp_data["gender"],
                marital_status=emp_data["marital_status"],
                father_husband_name=emp_data["father_name"],
                blood_group=emp_data["blood_group"],
                emergency_contact_name=f"{emp_data['father_name']}",
                emergency_contact_number=f"+91-98765432{30 + idx}",
                emergency_contact_relation="Father",
                date_of_joining=joining_date,
                employment_type="permanent",
                probation_period_months=6,
                confirmation_date=confirmation_date,
                notice_period_days=60,
                department_id=dept_objects[emp_data["department"]].id,
                designation_id=desig_objects[emp_data["designation"]].id,
                grade_id=grade_objects[emp_data["grade"]].id,
                status="ACTIVE"
            )
            db.add(employee)
            db.commit()
            db.refresh(employee)
            print(f"   [CREATED] Employee: {employee.employee_code}")
            employee_ids.append(employee.id)

            # Create Bank Details
            account_number = f"{random.randint(100000000000, 999999999999):012d}"
            bank_details = EmployeeBankDetails(
                employee_id=employee.id,
                account_holder_name=f"{emp_data['first_name']} {emp_data['middle_name']} {emp_data['last_name']}".replace("  ", " "),
                account_number=account_number,
                bank_name=emp_data["bank"],
                branch_name=emp_data["branch"],
                ifsc_code=emp_data["ifsc"],
                account_type="savings",
                pan_number=emp_data["pan"]
            )
            db.add(bank_details)
            print(f"   [CREATED] Bank Details: {emp_data['bank']}")

            # Create Salary Details
            salary_components = calculate_salary_components(emp_data["basic_salary"])
            salary_details = EmployeeSalaryDetails(
                employee_id=employee.id,
                **salary_components
            )
            db.add(salary_details)
            print(f"   [CREATED] Salary: Basic Rs. {emp_data['basic_salary']:,.2f}, CTC Rs. {salary_components['ctc']:,.2f}")

            # Create Statutory Details
            uan = f"10{random.randint(1000000000, 9999999999):010d}"
            statutory = EmployeeStatutoryDetails(
                employee_id=employee.id,
                pan_number=emp_data["pan"],
                aadhaar_number=emp_data["aadhaar"],
                uan_number=uan,
                esic_number="",
                pf_applicable=True,
                esic_applicable=(salary_components["gross_salary"] < 21000),
                lwf_applicable=False,
                pt_applicable=True,
                previous_employer_pf_number="",
                date_of_exit_from_previous_pf=None
            )
            db.add(statutory)
            print(f"   [CREATED] Statutory: PAN {emp_data['pan']}, UAN {uan}")

            db.commit()

        # 6. Create Employee User Accounts (for first employee as test)
        print("\n6. Creating Employee User Account (Test Employee)...")
        test_employee = db.query(Employee).filter(Employee.id == employee_ids[0]).first()
        emp_user = db.query(User).filter(User.username == "employee").first()
        if not emp_user and test_employee:
            emp_user = User(
                username="employee",
                email=test_employee.email,
                hashed_password=get_password_hash("employee123"),
                role="employee",
                full_name=f"{test_employee.first_name} {test_employee.last_name}",
                is_active=True,
                is_superuser=False,
                tenant_id=tenant.id
            )
            db.add(emp_user)
            db.commit()
            db.refresh(emp_user)
            print(f"   [CREATED] Employee User: {emp_user.full_name}")
        else:
            print(f"   [EXISTS] Employee User: {emp_user.full_name if emp_user else 'N/A'}")

        # Summary
        print("\n" + "=" * 80)
        print("TEST DATA CREATION COMPLETE!")
        print("=" * 80)

        print(f"\nCompany: {tenant.name}")
        print(f"Total Employees Created: {len(employee_ids)}")
        print(f"Test Employee: {test_employee.first_name} {test_employee.last_name} (ID: {test_employee.id})")

        print("\n" + "=" * 80)
        print("LOGIN CREDENTIALS")
        print("=" * 80)

        print("\n1. EMPLOYER ADMIN (Full Access)")
        print("   Username: employer")
        print("   Password: employer123")
        print("   Email: employer@techinnovate.com")
        print("   Access: All features, manage all employees, view reports")

        print("\n2. HR MANAGER (HR Access)")
        print("   Username: hrmanager")
        print("   Password: hr123")
        print("   Email: hr@techinnovate.com")
        print("   Access: Employee management, leave management, attendance")

        print("\n3. EMPLOYEE (Self-Service)")
        print("   Username: employee")
        print("   Password: employee123")
        print(f"   Email: {test_employee.email}")
        print("   Access: View own details, apply leave, mark attendance")

        print("\n" + "=" * 80)
        print("EMPLOYEE LIST")
        print("=" * 80)

        for idx, emp_id in enumerate(employee_ids, 1):
            emp = db.query(Employee).filter(Employee.id == emp_id).first()
            salary = db.query(EmployeeSalaryDetails).filter(
                EmployeeSalaryDetails.employee_id == emp_id
            ).first()
            print(f"\n{idx:2d}. {emp.employee_code} - {emp.first_name} {emp.last_name}")
            print(f"    Email: {emp.email}")
            print(f"    Department: {dept_objects[emp.department.name if emp.department else 'N/A'].name}")
            print(f"    Designation: {emp.designation.name if emp.designation else 'N/A'}")
            print(f"    CTC: Rs. {salary.ctc:,.2f}/month" if salary else "    CTC: N/A")

        print("\n" + "=" * 80)
        print("API ENDPOINTS")
        print("=" * 80)
        print("\nBackend API: http://localhost:8000")
        print("Swagger Docs: http://localhost:8000/docs")
        print(f"\nTest Employee ID: {test_employee.id}")
        print(f"Test Employee API: http://localhost:8000/api/v1/employees/{test_employee.id}")

        print("\n" + "=" * 80)

        return employee_ids

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    employee_ids = create_comprehensive_test_data()
    if employee_ids:
        print(f"\n[SUCCESS] Created {len(employee_ids)} employees!")
        print("\nYou can now:")
        print("1. Start the backend (already running on port 8000)")
        print("2. Login with any of the credentials above")
        print("3. Test all employee features")
    else:
        print("\n[FAILED] Failed to create test data. Please check the errors above.")
        sys.exit(1)
