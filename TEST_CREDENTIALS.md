# HR Payroll System - Test Credentials & Setup

## Company Information
**Company Name:** Tech Innovate Solutions Pvt Ltd
**Company Code:** techinnovate
**Address:** 123, MG Road, Bangalore, Karnataka 560001
**Phone:** +91-80-41234567
**Email:** info@techinnovate.com

---

## Login Credentials

### 1. EMPLOYER ADMIN (Full System Access)
- **Username:** `employer`
- **Password:** `employer123`
- **Email:** employer@techinnovate.com
- **Role:** Employer Admin
- **Full Name:** Ravi Krishnan
- **Access Level:** Complete system access
  - Manage all employees
  - View/edit all employee details
  - Access to reports and analytics
  - Manage payroll
  - System configuration

### 2. HR MANAGER (Human Resources Access)
- **Username:** `hrmanager`
- **Password:** `hr123`
- **Email:** hr@techinnovate.com
- **Role:** HR Manager
- **Full Name:** Meera Lakshmi
- **Access Level:** HR operations
  - Employee management
  - Leave management
  - Attendance tracking
  - Employee onboarding/offboarding
  - HR reports

### 3. EMPLOYEE (Self-Service Access)
- **Username:** `employee`
- **Password:** `employee123`
- **Email:** rajesh.kumar@techinnovate.com
- **Role:** Employee
- **Full Name:** Rajesh Kumar
- **Employee Code:** TIS1001
- **Access Level:** Self-service portal
  - View own details
  - Apply for leave
  - Mark attendance
  - View payslips
  - Update personal information

---

## Test Employee Details

**Primary Test Employee:** Rajesh Kumar (ID: 2)

### Personal Information
- **Employee Code:** TIS1001
- **Email:** rajesh.kumar@techinnovate.com
- **Phone:** +91-9876543210
- **DOB:** March 15, 1988
- **Gender:** Male
- **Marital Status:** Married
- **Blood Group:** O+

### Employment Details
- **Department:** Engineering
- **Designation:** Senior Software Engineer
- **Grade:** L3 (Mid Level)
- **Date of Joining:** Random date in last 3 years
- **Employment Type:** Permanent
- **Status:** ACTIVE

### Bank Details
- **Bank:** HDFC Bank
- **Branch:** Indiranagar, Bangalore
- **IFSC:** HDFC0001234
- **Account Type:** Savings
- **PAN:** ABCDE1234F

### Salary Details
- **Basic Salary:** Rs. 85,000.00
- **HRA (40%):** Rs. 34,000.00
- **Conveyance:** Rs. 1,600.00
- **Medical:** Rs. 1,250.00
- **Special Allowance (20%):** Rs. 17,000.00
- **Gross Salary:** Rs. 138,850.00
- **PF (Employee 12%):** Rs. 10,200.00
- **PF (Employer 12%):** Rs. 10,200.00
- **Professional Tax:** Rs. 200.00
- **TDS:** Rs. 6,942.50
- **Total Deductions:** Rs. 17,342.50
- **Net Salary:** Rs. 121,507.50
- **CTC:** Rs. 149,050.00/month

### Statutory Details
- **PAN:** ABCDE1234F
- **Aadhaar:** 234567890123
- **UAN:** 101302136303
- **PF Applicable:** Yes
- **PT Applicable:** Yes

---

## All 10 Employees

| # | Code | Name | Department | Designation | Email | CTC (Monthly) |
|---|------|------|------------|-------------|-------|---------------|
| 1 | TIS1001 | Rajesh Kumar | Engineering | Senior Software Engineer | rajesh.kumar@techinnovate.com | Rs. 149,050.00 |
| 2 | TIS1002 | Priya Sharma | Engineering | Software Engineer | priya.sharma@techinnovate.com | Rs. 114,650.00 |
| 3 | TIS1003 | Amit Patel | Engineering | Tech Lead | amit.patel@techinnovate.com | Rs. 209,250.00 |
| 4 | TIS1004 | Sneha Reddy | Human Resources | HR Executive | sneha.reddy@techinnovate.com | Rs. 97,450.00 |
| 5 | TIS1005 | Vikram Singh | Finance | Senior Accountant | vikram.singh@techinnovate.com | Rs. 131,850.00 |
| 6 | TIS1006 | Anjali Desai | Marketing | Marketing Executive | anjali.desai@techinnovate.com | Rs. 106,050.00 |
| 7 | TIS1007 | Karthik Iyer | Engineering | Senior Software Engineer | karthik.iyer@techinnovate.com | Rs. 157,650.00 |
| 8 | TIS1008 | Divya Nair | Quality Assurance | QA Engineer | divya.nair@techinnovate.com | Rs. 102,610.00 |
| 9 | TIS1009 | Arjun Menon | Operations | Operations Manager | arjun.menon@techinnovate.com | Rs. 192,050.00 |
| 10 | TIS1010 | Pooja Verma | Human Resources | HR Manager | pooja.verma@techinnovate.com | Rs. 140,450.00 |

---

## System Access

### Backend API
- **Base URL:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health

### Frontend (when running)
- **URL:** http://localhost:3000 (or port specified by frontend)
- **Login Page:** http://localhost:3000/login

---

## Testing Instructions

### 1. Test Employer Admin Features
1. Login with `employer` / `employer123`
2. Navigate to Employees section
3. View all 10 employees
4. Click on Rajesh Kumar (TIS1001)
5. View all 6 tabs:
   - Basic Information
   - Contact Information
   - Employment Details
   - Bank Account Details
   - Salary Information
   - Statutory Information
6. Edit any details and save
7. Verify changes persist

### 2. Test HR Manager Features
1. Login with `hrmanager` / `hr123`
2. Access employee management
3. View employee list
4. Test leave management features
5. Test attendance features

### 3. Test Employee Self-Service
1. Login with `employee` / `employee123`
2. View own profile (Rajesh Kumar)
3. View own salary details
4. Apply for leave
5. Mark attendance
6. Update personal information (if allowed)

### 4. Test API Endpoints (via Swagger)
1. Go to http://localhost:8000/docs
2. Click "Authorize"
3. Login with any credentials
4. Test employee detail endpoints:
   - GET /api/v1/employees/{id}
   - GET /api/v1/employees/{id}/bank-details
   - GET /api/v1/employees/{id}/salary-details
   - GET /api/v1/employees/{id}/statutory-details
   - PUT /api/v1/employees/{id}/bank-details
   - PUT /api/v1/employees/{id}/salary-details
   - PUT /api/v1/employees/{id}/statutory-details

---

## Quick API Test

### Get Test Employee Details
```bash
# Login first
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=employer&password=employer123"

# Get employee with all details (replace {token} with actual token)
curl -X GET "http://localhost:8000/api/v1/employees/2" \
  -H "Authorization: Bearer {token}"
```

---

## Database Information

- **Database:** PostgreSQL
- **Database Name:** hr_payroll
- **Host:** localhost:5432
- **User:** postgres
- **Password:** hrpayroll2024

### Connect to Database
```bash
psql -U postgres -d hr_payroll
```

---

## Notes

- All employees have complete details: bank, salary, and statutory information
- Salaries are calculated automatically based on basic salary
- PF is 12% of basic (both employee and employer)
- ESIC applicable if gross < Rs. 21,000
- Professional Tax Rs. 200 if gross > Rs. 15,000
- TDS is 5% of gross if gross > Rs. 50,000
- All employees are in ACTIVE status
- Random joining dates in the last 3 years
- 6 months probation period for all

---

**Generated:** November 12, 2025
**Backend Server:** Running on port 8000
**Database:** PostgreSQL (hr_payroll)
**Status:** All features tested and working ✓
