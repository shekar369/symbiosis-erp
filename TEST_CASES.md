# HR Payroll System - Test Cases by Stakeholder

## Test Environment
- **Frontend URL**: http://127.0.0.1:5174
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Test Credentials

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| SaaS Admin | saasadmin | admin123 | System-wide administration |
| Employer Admin | employer | employer123 | Company HR management |
| Employee | employee1 | employee123 | Employee self-service |

---

## 1. SAAS ADMIN TEST CASES

**Role**: System administrator with access to all tenants and system configuration

### 1.1 Authentication & Authorization

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| SA-001 | SaaS Admin Login | 1. Navigate to login page<br>2. Enter username: saasadmin<br>3. Enter password: admin123<br>4. Click Sign In | Login successful, redirected to dashboard | ☐ |
| SA-002 | SaaS Admin Session Persistence | 1. Login as saasadmin<br>2. Refresh browser | User remains logged in, no redirect to login | ☐ |
| SA-003 | SaaS Admin Logout | 1. Login as saasadmin<br>2. Click logout | Logged out, redirected to login page | ☐ |
| SA-004 | Invalid Credentials | 1. Enter username: saasadmin<br>2. Enter password: wrongpass<br>3. Click Sign In | Error message displayed, login fails | ☐ |

### 1.2 Dashboard Access

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| SA-010 | Dashboard View | 1. Login as saasadmin<br>2. Verify dashboard loads | Dashboard displays with system-wide statistics | ☐ |
| SA-011 | Navigation Menu Access | 1. Login as saasadmin<br>2. Check sidebar menu | All admin menu items visible and accessible | ☐ |

### 1.3 System Configuration

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| SA-020 | Access System Config | 1. Login as saasadmin<br>2. Navigate to Admin > System Config | System configuration page loads | ☐ |
| SA-021 | View Configuration Settings | 1. Go to System Config<br>2. Check all tabs (General, Email, Security, etc.) | All configuration tabs display correctly | ☐ |
| SA-022 | Update System Settings | 1. Go to System Config<br>2. Modify a setting<br>3. Click Save | Settings updated, success message shown | ☐ |

### 1.4 Multi-Tenant Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| SA-030 | View All Tenants | 1. Login as saasadmin<br>2. Navigate to tenants section | List of all tenants displayed | ☐ |
| SA-031 | Access Cross-Tenant Data | 1. Login as saasadmin<br>2. Switch between different tenants | Can view data from multiple tenants | ☐ |

---

## 2. EMPLOYER ADMIN TEST CASES

**Role**: Company HR administrator managing employees, payroll, and attendance

### 2.1 Authentication & Authorization

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-001 | Employer Admin Login | 1. Navigate to login page<br>2. Enter username: employer<br>3. Enter password: employer123<br>4. Click Sign In | Login successful, redirected to employer dashboard | ☐ |
| EA-002 | Session Persistence | 1. Login as employer<br>2. Refresh browser | User remains logged in | ☐ |
| EA-003 | Logout | 1. Login as employer<br>2. Click logout | Logged out successfully | ☐ |
| EA-004 | Tenant Data Isolation | 1. Login as employer<br>2. View employees list | Only sees employees from own tenant | ☐ |

### 2.2 Dashboard & Overview

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-010 | Dashboard Statistics | 1. Login as employer<br>2. View dashboard | Shows total employees, active, exited, attendance % | ☐ |
| EA-011 | Location Filter | 1. On dashboard<br>2. Select different location from dropdown | Statistics update based on selected location | ☐ |
| EA-012 | Recent Activities | 1. View dashboard<br>2. Check activities section | Recent HR activities displayed | ☐ |

### 2.3 Employee Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-020 | View Employees List | 1. Login as employer<br>2. Navigate to Employees | List of all employees displayed with filters | ☐ |
| EA-021 | Search Employee | 1. Go to Employees<br>2. Enter employee name in search | Matching employees displayed | ☐ |
| EA-022 | Filter Employees | 1. Go to Employees<br>2. Apply filters (status, location, department) | Filtered results displayed | ☐ |
| EA-023 | Add New Employee | 1. Go to Employees<br>2. Click Add Employee<br>3. Fill all required fields<br>4. Click Save | Employee created, success message shown | ☐ |
| EA-024 | View Employee Details | 1. Go to Employees<br>2. Click on an employee | Employee details page displayed | ☐ |
| EA-025 | Edit Employee | 1. View employee details<br>2. Click Edit<br>3. Modify fields<br>4. Click Save | Employee updated successfully | ☐ |
| EA-026 | Delete Employee | 1. Go to Employees<br>2. Select employee<br>3. Click Delete<br>4. Confirm deletion | Employee deleted (or archived) | ☐ |
| EA-027 | Bulk Upload Employees | 1. Go to Employees<br>2. Click Upload/Import<br>3. Select Excel file<br>4. Upload | Employees imported from Excel file | ☐ |
| EA-028 | Export Employees | 1. Go to Employees<br>2. Click Export<br>3. Select format (Excel/CSV) | Employee data exported successfully | ☐ |

### 2.4 Location Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-030 | View Locations | 1. Login as employer<br>2. Navigate to Locations | List of locations displayed | ☐ |
| EA-031 | Add New Location | 1. Go to Locations<br>2. Click Add Location<br>3. Fill details (name, address, etc.)<br>4. Click Save | Location created successfully | ☐ |
| EA-032 | Edit Location | 1. Go to Locations<br>2. Click Edit on a location<br>3. Modify details<br>4. Save | Location updated successfully | ☐ |
| EA-033 | Delete Location | 1. Go to Locations<br>2. Select location<br>3. Click Delete<br>4. Confirm | Location deleted (if no employees assigned) | ☐ |

### 2.5 Attendance Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-040 | View Attendance | 1. Login as employer<br>2. Navigate to Attendance | Attendance records displayed with filters | ☐ |
| EA-041 | Filter by Date Range | 1. Go to Attendance<br>2. Select date range<br>3. Apply filter | Attendance for selected period displayed | ☐ |
| EA-042 | Filter by Location | 1. Go to Attendance<br>2. Select location<br>3. Apply filter | Attendance for selected location shown | ☐ |
| EA-043 | Mark Attendance | 1. Go to Attendance<br>2. Select date<br>3. Mark employees present/absent | Attendance marked successfully | ☐ |
| EA-044 | Bulk Upload Attendance | 1. Go to Attendance<br>2. Click Upload<br>3. Select Excel file<br>4. Upload | Attendance imported from Excel | ☐ |
| EA-045 | Export Attendance | 1. Go to Attendance<br>2. Select date range<br>3. Click Export | Attendance data exported | ☐ |
| EA-046 | View Attendance Summary | 1. Go to Attendance<br>2. View summary section | Shows present/absent/leave counts | ☐ |

### 2.6 Wages Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-050 | View Wage Structure | 1. Login as employer<br>2. Navigate to Wages | Wage components and structures displayed | ☐ |
| EA-051 | Define Wage Components | 1. Go to Wages<br>2. Click Add Component<br>3. Define (Basic, DA, HRA, etc.)<br>4. Save | Wage component created | ☐ |
| EA-052 | Assign Wages to Employee | 1. Go to Wages<br>2. Select employee<br>3. Assign wage structure<br>4. Save | Wages assigned to employee | ☐ |
| EA-053 | Update Wage Structure | 1. Go to Wages<br>2. Edit existing structure<br>3. Modify values<br>4. Save | Wage structure updated | ☐ |

### 2.7 Leave Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-060 | View Leave Requests | 1. Login as employer<br>2. Navigate to Leaves | List of leave requests displayed | ☐ |
| EA-061 | Filter Leave Requests | 1. Go to Leaves<br>2. Filter by status (pending/approved/rejected) | Filtered leave requests shown | ☐ |
| EA-062 | Approve Leave Request | 1. Go to Leaves<br>2. Click on pending request<br>3. Click Approve<br>4. Add comments (optional) | Leave approved, employee notified | ☐ |
| EA-063 | Reject Leave Request | 1. Go to Leaves<br>2. Click on pending request<br>3. Click Reject<br>4. Add reason | Leave rejected with reason | ☐ |
| EA-064 | View Leave Balance | 1. Go to Leaves<br>2. Select employee<br>3. View balance | Shows leave balance for each type | ☐ |
| EA-065 | Configure Leave Types | 1. Go to Leaves<br>2. Click Leave Settings<br>3. Add/Edit leave types<br>4. Set entitlements | Leave types configured | ☐ |

### 2.8 Payroll Processing

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-070 | View Payroll Dashboard | 1. Login as employer<br>2. Navigate to Payroll | Payroll processing dashboard displayed | ☐ |
| EA-071 | Process Monthly Payroll | 1. Go to Payroll<br>2. Select month/year<br>3. Click Process Payroll<br>4. Review calculations | Payroll processed for all employees | ☐ |
| EA-072 | View Payroll Details | 1. Go to Payroll<br>2. Select processed month<br>3. Click on employee | Detailed salary slip with all components | ☐ |
| EA-073 | Apply Deductions | 1. Go to Payroll<br>2. Select employee<br>3. Add deduction (advance, loans)<br>4. Save | Deduction applied to salary | ☐ |
| EA-074 | Generate Pay Slips | 1. Go to Payroll<br>2. Select processed month<br>3. Click Generate Pay Slips | Pay slips generated for all employees | ☐ |
| EA-075 | Download Pay Slips | 1. Go to Payroll<br>2. Select month<br>3. Click Download<br>4. Select format (PDF/Excel) | Pay slips downloaded successfully | ☐ |
| EA-076 | Reprocess Payroll | 1. Go to Payroll<br>2. Select month<br>3. Make corrections<br>4. Click Reprocess | Payroll recalculated with changes | ☐ |

### 2.9 Statutory Compliance

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-080 | View Statutory Reports | 1. Login as employer<br>2. Navigate to Statutory | Statutory compliance dashboard displayed | ☐ |
| EA-081 | Generate PF Report | 1. Go to Statutory<br>2. Select PF Report<br>3. Choose date range<br>4. Generate | PF contribution report generated | ☐ |
| EA-082 | Generate ESI Report | 1. Go to Statutory<br>2. Select ESI Report<br>3. Choose date range<br>4. Generate | ESI contribution report generated | ☐ |
| EA-083 | Generate PT Report | 1. Go to Statutory<br>2. Select Professional Tax<br>3. Choose period<br>4. Generate | PT report generated | ☐ |
| EA-084 | Download Statutory Forms | 1. Go to Statutory<br>2. Select form type<br>3. Click Download | Statutory form downloaded | ☐ |

### 2.10 Bank Transfer

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-090 | View Bank Transfer | 1. Login as employer<br>2. Navigate to Bank Transfer | Bank transfer dashboard displayed | ☐ |
| EA-091 | Generate Bank File | 1. Go to Bank Transfer<br>2. Select month<br>3. Choose bank format<br>4. Generate | Bank transfer file generated | ☐ |
| EA-092 | Download Bank File | 1. Generate bank file<br>2. Click Download<br>3. Choose format (CSV/Excel/TXT) | Bank file downloaded in selected format | ☐ |
| EA-093 | Preview Bank Transfer | 1. Go to Bank Transfer<br>2. Select month<br>3. Click Preview | Shows list of transfers with amounts | ☐ |

### 2.11 Reports

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EA-100 | View Reports Dashboard | 1. Login as employer<br>2. Navigate to Reports | Reports dashboard with categories | ☐ |
| EA-101 | Employee Report | 1. Go to Reports<br>2. Select Employee Report<br>3. Choose filters<br>4. Generate | Employee report generated | ☐ |
| EA-102 | Attendance Report | 1. Go to Reports<br>2. Select Attendance Report<br>3. Choose date range<br>4. Generate | Attendance report generated | ☐ |
| EA-103 | Payroll Summary Report | 1. Go to Reports<br>2. Select Payroll Summary<br>3. Choose period<br>4. Generate | Payroll summary report generated | ☐ |
| EA-104 | Leave Report | 1. Go to Reports<br>2. Select Leave Report<br>3. Choose filters<br>4. Generate | Leave report with balances generated | ☐ |
| EA-105 | Custom Report | 1. Go to Reports<br>2. Select Custom Report<br>3. Choose fields<br>4. Apply filters<br>5. Generate | Custom report generated as per selection | ☐ |
| EA-106 | Export Report | 1. Generate any report<br>2. Click Export<br>3. Choose format | Report exported in selected format | ☐ |
| EA-107 | Schedule Report | 1. Go to Reports<br>2. Select report<br>3. Click Schedule<br>4. Set frequency | Report scheduled for auto-generation | ☐ |

---

## 3. EMPLOYEE TEST CASES

**Role**: Individual employee accessing self-service portal

### 3.1 Authentication & Authorization

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-001 | Employee Login | 1. Navigate to login page<br>2. Enter username: employee1<br>3. Enter password: employee123<br>4. Click Sign In | Login successful, redirected to employee dashboard | ☐ |
| EM-002 | Session Persistence | 1. Login as employee1<br>2. Refresh browser | User remains logged in | ☐ |
| EM-003 | Logout | 1. Login as employee1<br>2. Click logout | Logged out successfully | ☐ |
| EM-004 | Restricted Access | 1. Login as employee1<br>2. Try to access employer pages | Access denied, only employee menu visible | ☐ |

### 3.2 Employee Dashboard

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-010 | View Dashboard | 1. Login as employee1<br>2. View dashboard | Shows personal stats, attendance, leaves | ☐ |
| EM-011 | Quick Actions | 1. View dashboard<br>2. Check quick action buttons | Shows apply leave, view payslip buttons | ☐ |
| EM-012 | Notifications | 1. View dashboard<br>2. Check notifications section | Shows pending actions, announcements | ☐ |

### 3.3 Profile Management

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-020 | View Profile | 1. Login as employee1<br>2. Navigate to Profile | Complete profile information displayed | ☐ |
| EM-021 | Update Personal Info | 1. Go to Profile<br>2. Click Edit<br>3. Update allowed fields (phone, address)<br>4. Save | Personal information updated | ☐ |
| EM-022 | Upload Profile Photo | 1. Go to Profile<br>2. Click upload photo<br>3. Select image<br>4. Upload | Profile photo updated | ☐ |
| EM-023 | View Employment Details | 1. Go to Profile<br>2. View employment tab | Shows designation, department, joining date | ☐ |
| EM-024 | View Bank Details | 1. Go to Profile<br>2. View bank details section | Bank account information displayed (masked) | ☐ |
| EM-025 | Change Password | 1. Go to Profile<br>2. Click Change Password<br>3. Enter old and new password<br>4. Submit | Password changed successfully | ☐ |

### 3.4 Attendance & Leave

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-030 | View Attendance | 1. Login as employee1<br>2. Navigate to My Attendance | Personal attendance records displayed | ☐ |
| EM-031 | View Attendance Calendar | 1. Go to My Attendance<br>2. View calendar | Calendar shows present/absent/leave days | ☐ |
| EM-032 | View Attendance Summary | 1. Go to My Attendance<br>2. View summary | Shows total days, present, absent, leave count | ☐ |
| EM-033 | Apply for Leave | 1. Go to Leave<br>2. Click Apply Leave<br>3. Select type, dates<br>4. Add reason<br>5. Submit | Leave application submitted | ☐ |
| EM-034 | View Leave Balance | 1. Go to Leave<br>2. View balance section | Shows available leave balance by type | ☐ |
| EM-035 | View Leave History | 1. Go to Leave<br>2. View history tab | Shows all past leave requests with status | ☐ |
| EM-036 | Cancel Leave Request | 1. Go to Leave<br>2. Select pending request<br>3. Click Cancel | Leave request cancelled (if still pending) | ☐ |

### 3.5 Payslips

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-040 | View Payslips | 1. Login as employee1<br>2. Navigate to Payslips | List of payslips by month displayed | ☐ |
| EM-041 | View Payslip Details | 1. Go to Payslips<br>2. Click on a month | Detailed payslip with all components shown | ☐ |
| EM-042 | Download Payslip | 1. Go to Payslips<br>2. Select month<br>3. Click Download PDF | Payslip downloaded as PDF | ☐ |
| EM-043 | View Salary Breakdown | 1. View payslip<br>2. Check breakdown section | Shows earnings, deductions, net pay | ☐ |
| EM-044 | View YTD Summary | 1. Go to Payslips<br>2. View year-to-date section | Shows cumulative salary, tax deducted | ☐ |

### 3.6 Documents

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| EM-050 | View Documents | 1. Login as employee1<br>2. Navigate to Documents | Personal documents list displayed | ☐ |
| EM-051 | Download Document | 1. Go to Documents<br>2. Click on document<br>3. Click Download | Document downloaded successfully | ☐ |
| EM-052 | Upload Document | 1. Go to Documents<br>2. Click Upload<br>3. Select file<br>4. Choose category<br>5. Upload | Document uploaded (if allowed by admin) | ☐ |

---

## 4. CROSS-FUNCTIONAL TEST CASES

**Test cases that involve multiple roles or system-wide features**

### 4.1 Multi-User Scenarios

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| CF-001 | Concurrent User Access | 1. Login as employer in browser 1<br>2. Login as employee in browser 2<br>3. Perform actions simultaneously | Both users can work without conflicts | ☐ |
| CF-002 | Data Isolation | 1. Login as employer<br>2. Add employee data<br>3. Logout<br>4. Login as employee from same tenant<br>5. Check if data visible | Employee sees only their own data | ☐ |
| CF-003 | Leave Approval Flow | 1. Login as employee, apply leave<br>2. Logout<br>3. Login as employer<br>4. Approve leave<br>5. Login as employee<br>6. Check status | Leave status updated across both roles | ☐ |

### 4.2 Security & Data Privacy

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| CF-010 | Token Expiration | 1. Login as any user<br>2. Wait for token expiry (or manipulate)<br>3. Try to perform action | Redirected to login, session expired message | ☐ |
| CF-011 | SQL Injection Prevention | 1. Login as any user<br>2. Try SQL injection in search/input fields<br>3. Submit | Input sanitized, no SQL execution | ☐ |
| CF-012 | XSS Prevention | 1. Login as any user<br>2. Enter script tags in form fields<br>3. Submit | Scripts escaped, not executed | ☐ |
| CF-013 | CSRF Protection | 1. Attempt CSRF attack on API endpoints | Request blocked, CSRF token validation works | ☐ |
| CF-014 | Password Security | 1. Create new user<br>2. Check password in database | Password stored as hash, not plaintext | ☐ |

### 4.3 Performance & Load

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| CF-020 | Large Dataset Handling | 1. Upload 1000+ employees<br>2. Navigate to employee list | Page loads within acceptable time with pagination | ☐ |
| CF-021 | Bulk Operations | 1. Select 100+ employees<br>2. Perform bulk action (export) | Operation completes without timeout | ☐ |
| CF-022 | Report Generation Speed | 1. Generate large report (1 year data)<br>2. Time the operation | Report generates within 30 seconds | ☐ |

### 4.4 Error Handling

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| CF-030 | API Failure Handling | 1. Stop backend server<br>2. Try to perform action in UI | User-friendly error message displayed | ☐ |
| CF-031 | Network Error | 1. Disconnect internet<br>2. Try to perform action | Appropriate error message shown | ☐ |
| CF-032 | Invalid File Upload | 1. Try to upload invalid file type<br>2. Submit | Error message, file rejected | ☐ |
| CF-033 | Required Field Validation | 1. Try to submit form with empty required fields | Validation errors shown for each field | ☐ |

---

## 5. INTEGRATION TEST CASES

### 5.1 API Integration

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| INT-001 | API Authentication | 1. Call any protected endpoint without token | 401 Unauthorized returned | ☐ |
| INT-002 | API with Valid Token | 1. Login to get token<br>2. Call protected endpoint with token | 200 OK, data returned | ☐ |
| INT-003 | API Response Format | 1. Call any endpoint<br>2. Check response structure | Consistent JSON format with proper fields | ☐ |
| INT-004 | API Error Responses | 1. Call API with invalid data<br>2. Check error response | Proper error code and message returned | ☐ |

### 5.2 Database Operations

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| INT-010 | Data Persistence | 1. Add employee<br>2. Restart server<br>3. Check employee exists | Data persists across server restart | ☐ |
| INT-011 | Transaction Rollback | 1. Perform operation that fails mid-transaction<br>2. Check database | Partial data not saved, rollback successful | ☐ |
| INT-012 | Referential Integrity | 1. Try to delete location with assigned employees<br>2. Check result | Deletion prevented or employees unassigned | ☐ |

---

## 6. UI/UX TEST CASES

| TC ID | Test Case | Steps | Expected Result | Status |
|-------|-----------|-------|-----------------|--------|
| UI-001 | Responsive Design - Desktop | 1. Open on desktop browser (1920x1080)<br>2. Navigate through pages | UI displays properly, no overflow | ☐ |
| UI-002 | Responsive Design - Tablet | 1. Open on tablet (768x1024)<br>2. Navigate through pages | UI adapts to tablet screen | ☐ |
| UI-003 | Responsive Design - Mobile | 1. Open on mobile (375x667)<br>2. Navigate through pages | Mobile-optimized layout displayed | ☐ |
| UI-004 | Browser Compatibility - Chrome | 1. Open in Chrome<br>2. Test all features | All features work correctly | ☐ |
| UI-005 | Browser Compatibility - Firefox | 1. Open in Firefox<br>2. Test all features | All features work correctly | ☐ |
| UI-006 | Browser Compatibility - Edge | 1. Open in Edge<br>2. Test all features | All features work correctly | ☐ |
| UI-007 | Loading States | 1. Perform any async operation<br>2. Observe UI | Loading indicator shown during operation | ☐ |
| UI-008 | Success Messages | 1. Perform successful operation<br>2. Check feedback | Success message/toast displayed | ☐ |
| UI-009 | Error Messages | 1. Trigger validation error<br>2. Check feedback | Clear error message displayed | ☐ |
| UI-010 | Form Validation | 1. Fill form with invalid data<br>2. Submit | Inline validation errors shown | ☐ |

---

## 7. REGRESSION TEST SUITE

**Critical paths to test after any changes**

### 7.1 Smoke Test Checklist

| TC ID | Test Case | Expected Result | Status |
|-------|-----------|-----------------|--------|
| REG-001 | Application Starts | Frontend and backend servers start without errors | ☐ |
| REG-002 | Login Works | Can login with all three roles | ☐ |
| REG-003 | Dashboard Loads | Dashboard displays for each role | ☐ |
| REG-004 | Navigation Works | Can navigate between all pages | ☐ |
| REG-005 | Logout Works | Logout successful for all roles | ☐ |

### 7.2 Core Functionality

| TC ID | Test Case | Expected Result | Status |
|-------|-----------|-------|
| REG-010 | Employee CRUD | Can create, read, update, delete employees | ☐ |
| REG-011 | Attendance Operations | Can mark and view attendance | ☐ |
| REG-012 | Leave Operations | Can apply and approve leaves | ☐ |
| REG-013 | Payroll Processing | Can process monthly payroll | ☐ |
| REG-014 | Report Generation | Can generate and export reports | ☐ |

---

## 8. TEST EXECUTION SUMMARY

### Testing Progress

| Stakeholder | Total Tests | Passed | Failed | Blocked | Not Tested | Pass % |
|-------------|-------------|--------|--------|---------|------------|--------|
| SaaS Admin | 0 | 0 | 0 | 0 | 0 | 0% |
| Employer Admin | 0 | 0 | 0 | 0 | 0 | 0% |
| Employee | 0 | 0 | 0 | 0 | 0 | 0% |
| Cross-Functional | 0 | 0 | 0 | 0 | 0 | 0% |
| Integration | 0 | 0 | 0 | 0 | 0 | 0% |
| UI/UX | 0 | 0 | 0 | 0 | 0 | 0% |
| Regression | 0 | 0 | 0 | 0 | 0 | 0% |
| **TOTAL** | **0** | **0** | **0** | **0** | **0** | **0%** |

### Priority Test Cases

**CRITICAL - Must Pass Before Release:**
1. EA-001: Employer Admin Login
2. EM-001: Employee Login
3. EA-020: View Employees List
4. EA-071: Process Monthly Payroll
5. EM-040: View Payslips
6. CF-002: Data Isolation
7. CF-014: Password Security
8. REG-002: Login Works (All Roles)

**HIGH - Should Pass Before Release:**
1. All authentication and authorization tests
2. Core CRUD operations (Employees, Attendance, Payroll)
3. Security and data privacy tests
4. API integration tests

**MEDIUM - Important but not blocking:**
1. Advanced filtering and search
2. Report generation and export
3. Bulk operations
4. UI/UX responsive design

**LOW - Nice to have:**
1. Browser compatibility (non-Chrome)
2. Performance optimization tests
3. Advanced reporting features

---

## 9. TEST ENVIRONMENT SETUP

### Prerequisites
- Backend server running on port 8000
- Frontend server running on port 5174
- Database initialized with seed data
- Test accounts created (saasadmin, employer, employee1)

### Browser Developer Tools Setup
1. Open browser Developer Tools (F12)
2. Keep Console tab open to monitor logs
3. Check Network tab for API calls
4. Look for debug logs prefixed with:
   - `[AuthContext]`
   - `[Axios Interceptor]`
   - `[API Service]`

### Test Data Preparation
- Ensure at least 10 test employees exist
- Have sample attendance data for current month
- Have at least one processed payroll month
- Have pending leave requests for approval tests

---

## 10. BUG REPORTING TEMPLATE

When you find a bug, please report using this format:

**Bug ID**: [Auto-generated]
**Test Case ID**: [TC ID from above]
**Severity**: Critical / High / Medium / Low
**Priority**: P0 / P1 / P2 / P3

**Description**: Brief description of the bug

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Result**: What should happen

**Actual Result**: What actually happened

**Screenshots/Logs**: Attach relevant screenshots or console logs

**Environment**:
- Browser: Chrome 120.0
- OS: Windows 11
- User Role: employer_admin

---

## 11. SIGN-OFF CHECKLIST

### SaaS Admin Sign-off
- [ ] All SA test cases passed
- [ ] System configuration works
- [ ] Multi-tenant isolation verified
- [ ] Admin access to all features confirmed

**Signed By**: _________________ Date: _________

### Employer Admin Sign-off
- [ ] All EA test cases passed
- [ ] Employee management works
- [ ] Payroll processing successful
- [ ] Reports generate correctly

**Signed By**: _________________ Date: _________

### Employee Sign-off
- [ ] All EM test cases passed
- [ ] Self-service features work
- [ ] Payslips accessible
- [ ] Leave application works

**Signed By**: _________________ Date: _________

### Technical Lead Sign-off
- [ ] Security tests passed
- [ ] Performance acceptable
- [ ] API integration verified
- [ ] Code quality standards met

**Signed By**: _________________ Date: _________

---

## NOTES

- Mark test status with: ✓ (Pass) | ✗ (Fail) | ⊘ (Blocked) | ☐ (Not Tested)
- Update the Test Execution Summary table after each test cycle
- Log all bugs found during testing
- Retest failed cases after fixes
- Perform full regression test before final sign-off
