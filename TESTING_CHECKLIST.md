# HR Payroll System - Testing Checklist

**Date**: October 31, 2025
**Purpose**: Comprehensive testing guide for all features
**Status**: Ready for Testing

---

## ✅ **Testing Environment**

### **Prerequisites**:
- [ ] Backend server running (http://127.0.0.1:8000)
- [ ] Frontend server running (http://localhost:5174)
- [ ] Database initialized with seed data
- [ ] SMTP configured (for email tests)
- [ ] Test user credentials available (admin/admin123)

### **Testing Tools**:
- [ ] Swagger UI (http://127.0.0.1:8000/docs)
- [ ] Postman/Insomnia (optional)
- [ ] Browser DevTools
- [ ] Test email account

---

## 🧪 **Phase 1: Authentication & Setup**

### **1.1 User Authentication**:
- [ ] POST `/api/v1/auth/login` with valid credentials
- [ ] Verify JWT token received
- [ ] POST `/api/v1/auth/login` with invalid credentials (should fail)
- [ ] GET `/api/v1/health` (no auth required)

### **1.2 Location Management**:
- [ ] GET `/api/v1/locations/states` - List all states
- [ ] POST `/api/v1/locations/` - Create new location
- [ ] GET `/api/v1/locations/` - List all locations
- [ ] PUT `/api/v1/locations/{id}` - Update location
- [ ] DELETE `/api/v1/locations/{id}` - Delete location

---

## 🧪 **Phase 2: Excel Templates & Upload**

### **2.1 Template Download**:
- [ ] GET `/api/v1/templates/employee-database` - Download Excel
- [ ] Verify file downloads successfully
- [ ] Open Excel file and check format
- [ ] Verify sample data present

### **2.2 Employee Upload**:
- [ ] Fill employee template with test data (5-10 employees)
- [ ] POST `/api/v1/uploads/employees` - Upload filled Excel
- [ ] Verify success response
- [ ] Check validation errors for invalid data
- [ ] Verify employees created in database

### **2.3 Attendance Upload**:
- [ ] GET `/api/v1/templates/attendance` - Download template
- [ ] Fill with attendance data for uploaded employees
- [ ] POST `/api/v1/uploads/attendance` - Upload attendance
- [ ] Verify success response
- [ ] Check validation handling

---

## 🧪 **Phase 3: Payroll Processing**

### **3.1 Single Employee Calculation**:
- [ ] POST `/api/v1/payroll/calculate`
  ```json
  {
    "employee_id": 1,
    "month": 11,
    "year": 2025
  }
  ```
- [ ] Verify response includes:
  - Basic salary (pro-rated if absent days)
  - All allowances (HRA, Conveyance, Medical, Special)
  - PF deduction (if basic ≤ 15,000)
  - ESI deduction (if gross ≤ 21,000)
  - Professional Tax
  - Net salary calculation
- [ ] Verify wage statement created in database

### **3.2 Bulk Payroll Processing**:
- [ ] POST `/api/v1/payroll/process-bulk`
  ```json
  {
    "month": 11,
    "year": 2025
  }
  ```
- [ ] Verify all active employees processed
- [ ] Check success/failure counts
- [ ] Verify wage statements created for all

### **3.3 Wage Statements**:
- [ ] GET `/api/v1/payroll/wage-statements?month=11&year=2025`
- [ ] Verify list of all statements
- [ ] GET `/api/v1/payroll/wage-statement/1?month=11&year=2025`
- [ ] Verify detailed breakdown

### **3.4 Approval Workflow**:
- [ ] POST `/api/v1/payroll/approve`
  ```json
  {
    "wage_statement_ids": [1, 2, 3]
  }
  ```
- [ ] Verify status changed to "approved"
- [ ] Try approving again (should handle gracefully)

### **3.5 Mark as Paid**:
- [ ] POST `/api/v1/payroll/mark-paid`
  ```json
  {
    "wage_statement_ids": [1, 2, 3]
  }
  ```
- [ ] Verify status changed to "paid"
- [ ] Try marking unapproved statement (should fail)

### **3.6 Payroll Summary**:
- [ ] GET `/api/v1/payroll/summary?month=11&year=2025`
- [ ] Verify summary statistics:
  - Total employees
  - Total gross salary
  - Total deductions
  - Total net salary
  - Status breakdown

---

## 🧪 **Phase 4: PDF Generation**

### **4.1 Individual Payslip**:
- [ ] GET `/api/v1/payroll/payslip/1?month=11&year=2025`
- [ ] Verify PDF downloads
- [ ] Open PDF and check:
  - Company header
  - Employee details (code, name, designation)
  - Attendance summary (days worked, absent, effective)
  - Earnings breakdown (all 7 components)
  - Deductions breakdown (all components)
  - Net salary prominently displayed
  - Employer contributions (PF, ESI)
  - Professional formatting

### **4.2 Salary Register**:
- [ ] GET `/api/v1/payroll/salary-register?month=11&year=2025`
- [ ] Verify consolidated PDF downloads
- [ ] Check all employees included
- [ ] Verify totals row
- [ ] Check formatting

---

## 🧪 **Phase 5: Bank Transfer Files**

### **5.1 Standard CSV**:
- [ ] GET `/api/v1/payroll/bank-transfer-file?month=11&year=2025&format=csv`
- [ ] Download and open CSV
- [ ] Verify columns: S.No, Emp Code, Name, Bank A/C, IFSC, Amount
- [ ] Check data accuracy

### **5.2 NEFT Format**:
- [ ] GET `/api/v1/payroll/bank-transfer-file?month=11&year=2025&format=neft`
- [ ] Download text file
- [ ] Verify Header (H), Detail (D), Trailer (T) records
- [ ] Check fixed-width formatting

### **5.3 Bank-Specific Formats**:
- [ ] Test HDFC format (`format=hdfc`)
- [ ] Test ICICI format (`format=icici`)
- [ ] Test SBI format (`format=sbi`)
- [ ] Verify each bank's specific column requirements

### **5.4 Payment Summary**:
- [ ] GET `/api/v1/payroll/payment-summary?month=11&year=2025`
- [ ] Download text file
- [ ] Verify bank-wise breakdown
- [ ] Check employee list
- [ ] Verify totals

---

## 🧪 **Phase 6: Email Functionality**

### **6.1 SMTP Configuration**:
- [ ] Set environment variables in `.env`:
  ```
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your_email@gmail.com
  SMTP_PASSWORD=your_app_password
  ```
- [ ] Restart backend server
- [ ] Test SMTP connection (optional Python script)

### **6.2 Individual Email**:
- [ ] Ensure employee has valid email address
- [ ] POST `/api/v1/payroll/send-payslip-email/1?month=11&year=2025`
- [ ] Check success response
- [ ] Verify email received in inbox
- [ ] Open email and check:
  - Professional HTML formatting
  - Company header
  - Period information
  - PDF attachment
  - Proper filename
- [ ] Try with employee without email (should fail gracefully)

### **6.3 Bulk Email**:
- [ ] POST `/api/v1/payroll/send-bulk-payslips?month=11&year=2025`
- [ ] Check response summary:
  - Total statements
  - Emails sent
  - Emails failed
  - Skipped (no email)
- [ ] Verify multiple employees received emails
- [ ] Check for failed email list if any

---

## 🧪 **Phase 7: Statutory Forms**

### **7.1 EPF-ECR**:
- [ ] GET `/api/v1/statutory/epf-ecr?month=11&year=2025`
- [ ] Download CSV file
- [ ] Open and verify:
  - UAN numbers
  - Employee names
  - EPF wages (capped at ₹15,000)
  - Employee contribution (12%)
  - Employer EPS (8.33%)
  - Employer EPF (3.67%)
  - Totals row
- [ ] Verify only PF-applicable employees included

### **7.2 ESI Return**:
- [ ] GET `/api/v1/statutory/esi-return?month=11&year=2025`
- [ ] Download CSV file
- [ ] Verify:
  - IP numbers
  - Days worked
  - Total wages
- [ ] Verify only ESI-applicable employees (gross ≤ ₹21,000)

### **7.3 Professional Tax Form V**:
- [ ] GET `/api/v1/statutory/pt-form-v?month=11&year=2025&state=Maharashtra`
- [ ] Download PDF
- [ ] Verify:
  - Company details
  - PT registration number
  - Employee-wise deductions table
  - Total PT collected
  - Professional formatting

### **7.4 Form-XIII**:
- [ ] GET `/api/v1/statutory/form-xiii?month=11&year=2025`
- [ ] Download PDF
- [ ] Verify:
  - Company details
  - Employee register table
  - Father/Husband name
  - Age, designation
  - Wages and days worked

### **7.5 PF Challan Summary**:
- [ ] GET `/api/v1/statutory/pf-challan-summary?month=11&year=2025`
- [ ] Download PDF
- [ ] Verify:
  - EPF code
  - Number of employees
  - Total PF wages
  - Employee/Employer breakdown
  - Admin charges (0.5%)
  - EDLI charges (0.5%)
  - Grand total

---

## 🧪 **Phase 8: Edge Cases & Error Handling**

### **8.1 Invalid Data**:
- [ ] Try accessing with invalid token (should return 401)
- [ ] Try accessing other tenant's data (should return 403)
- [ ] Upload Excel with invalid data (email, phone format)
- [ ] Process payroll for non-existent month
- [ ] Download payslip for non-existent employee

### **8.2 Validation**:
- [ ] Employee code uniqueness
- [ ] Email format validation
- [ ] Phone number validation (10 digits)
- [ ] Date validations
- [ ] Salary component validations

### **8.3 Boundary Conditions**:
- [ ] Employee with 0 days worked
- [ ] Employee with all days present
- [ ] Employee with basic salary exactly ₹15,000 (PF ceiling)
- [ ] Employee with gross salary exactly ₹21,000 (ESI ceiling)
- [ ] Approval of already approved statements
- [ ] Mark paid without approval

---

## 🧪 **Phase 9: Performance Testing**

### **9.1 Bulk Operations**:
- [ ] Upload 100+ employees
- [ ] Upload 100+ attendance records
- [ ] Process bulk payroll for 100+ employees
- [ ] Generate 100+ payslips
- [ ] Send 100+ emails (in batches)

### **9.2 Response Times**:
- [ ] Single payroll calculation: < 1 second
- [ ] Bulk payroll (100 employees): < 30 seconds
- [ ] PDF generation: < 2 seconds
- [ ] Email sending: < 5 seconds per email
- [ ] Bank file generation: < 3 seconds

---

## 🧪 **Phase 10: Integration Testing**

### **10.1 Complete Workflow**:
- [ ] **Day 1**: Upload employees
- [ ] **Day 2**: Upload attendance for month
- [ ] **Day 3**: Process bulk payroll
- [ ] **Day 4**: Review and approve
- [ ] **Day 5**: Send emails to all employees
- [ ] **Day 6**: Generate bank transfer file
- [ ] **Day 7**: Mark as paid
- [ ] **Day 8**: Generate statutory forms
- [ ] **Day 9**: Download all reports
- [ ] **Day 10**: Verify data consistency

### **10.2 Multi-User Testing**:
- [ ] Admin processes payroll
- [ ] Manager approves
- [ ] Employee views payslip (if portal exists)
- [ ] Concurrent access handling

---

## 📊 **Test Results Summary**

### **Test Coverage**:
- [ ] Authentication: ___% passed
- [ ] Location Management: ___% passed
- [ ] Excel Upload: ___% passed
- [ ] Payroll Calculation: ___% passed
- [ ] PDF Generation: ___% passed
- [ ] Bank Files: ___% passed
- [ ] Email Service: ___% passed
- [ ] Statutory Forms: ___% passed
- [ ] Error Handling: ___% passed
- [ ] Performance: ___% passed

### **Issues Found**:
1. ______________________________
2. ______________________________
3. ______________________________

### **Critical Bugs**:
1. ______________________________
2. ______________________________

### **Enhancement Requests**:
1. ______________________________
2. ______________________________

---

## 🎯 **Sign-Off**

### **Tested By**: _____________________
### **Date**: _____________________
### **Environment**: Development / Staging / Production
### **Overall Status**: Pass / Fail / Needs Review

### **Recommendation**:
- [ ] Ready for Production
- [ ] Ready for UAT
- [ ] Needs More Testing
- [ ] Critical Issues Must Be Fixed

---

## 📞 **Support**

If you encounter issues during testing:
1. Check server logs: `./venv/Scripts/uvicorn app.main:app --log-level debug`
2. Check browser console for frontend errors
3. Verify database state
4. Check SMTP configuration for email issues
5. Review API documentation: http://127.0.0.1:8000/docs

---

**Document Created**: October 31, 2025
**Version**: 1.0
**Status**: Ready for Use
