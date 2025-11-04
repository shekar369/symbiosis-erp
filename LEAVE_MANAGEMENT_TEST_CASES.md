# Leave Management System - Test Cases & Test Sheet

## Test Environment Setup

### Prerequisites
- Backend server running on `http://localhost:8000`
- Frontend running on `http://localhost:5174`
- Database initialized with test data
- Test users created (saasadmin, employer, employee1)

### Test Data Required
- At least 3 employees in the system
- At least 2 leave types configured (Casual Leave, Sick Leave)
- Leave balances allocated to employees
- Mix of pending, approved, and rejected leave requests

---

## Test Cases

### A. EMPLOYEE SIDE - LEAVE APPLICATION

#### TC-EA-001: View Leave Balance
**Priority**: High
**Pre-condition**: Employee logged in, leave balance allocated

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to Employee Dashboard | Dashboard loads successfully | | |
| 2 | Click on "Leave" menu item | Leave Management page opens | | |
| 3 | Verify Leave Balance section | All allocated leave types displayed with balance | | |
| 4 | Check balance values | Correct balance shown (Total, Used, Available) | | |
| 5 | Verify visual display | Cards show leave type name, available days, used days | | |

**Test Data**:
- Employee: employee1
- Expected Leave Types: Casual Leave (12 days), Sick Leave (7 days)

---

#### TC-EA-002: Apply Leave - Valid Request
**Priority**: High
**Pre-condition**: Employee logged in, sufficient leave balance

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Apply Leave" tab | Apply leave form displayed | | |
| 2 | Select leave type (Casual Leave) | Dropdown shows available balance | | |
| 3 | Enter start date (today + 3 days) | Date field accepts input | | |
| 4 | Enter end date (today + 5 days) | Date field accepts input | | |
| 5 | Verify days calculation | System shows "3 days" automatically | | |
| 6 | Enter reason: "Family function" | Text area accepts input | | |
| 7 | Click "Submit Request" | Success message displayed | | |
| 8 | Switch to "My Leaves" tab | New request appears with "Pending" status | | |
| 9 | Verify leave balance updated | Balance unchanged (pending request) | | |

**Test Data**:
- Leave Type: Casual Leave
- Start Date: [Today + 3 days]
- End Date: [Today + 5 days]
- Days: 3
- Reason: "Family function"

---

#### TC-EA-003: Apply Leave - Insufficient Balance
**Priority**: High
**Pre-condition**: Employee logged in, limited leave balance

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Select leave type with low balance | Form loaded | | |
| 2 | Enter date range exceeding balance | Dates entered | | |
| 3 | Click "Submit Request" | Error message: "Insufficient leave balance. Available: X days, Requested: Y days" | | |
| 4 | Verify no request created | "My Leaves" tab shows no new request | | |

**Test Data**:
- Leave Type: Sick Leave (Balance: 2 days)
- Request: 5 days
- Expected Error: Insufficient balance message

---

#### TC-EA-004: Apply Leave - Invalid Date Range
**Priority**: Medium
**Pre-condition**: Employee logged in

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Enter end date before start date | Browser validation or custom error | | |
| 2 | Verify submit button | Form should prevent submission | | |

**Test Data**:
- Start Date: 2025-12-10
- End Date: 2025-12-05

---

#### TC-EA-005: Apply Leave - Past Date
**Priority**: Medium
**Pre-condition**: Employee logged in

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Try to select past date as start date | Date picker should restrict past dates (min=today) | | |
| 2 | Verify date validation | Cannot select dates before today | | |

---

#### TC-EA-006: View Leave Request History
**Priority**: Medium
**Pre-condition**: Employee has submitted multiple leave requests

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to "My Leaves" tab | All leave requests displayed | | |
| 2 | Verify request details shown | Leave type, dates, days, reason, status visible | | |
| 3 | Check status badges | Correct color coding (Yellow=Pending, Green=Approved, Red=Rejected) | | |
| 4 | Verify sorting | Latest requests appear first | | |

---

#### TC-EA-007: Cancel Pending Leave Request
**Priority**: High
**Pre-condition**: Employee has pending leave request

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to "My Leaves" tab | Pending requests shown | | |
| 2 | Click cancel/delete icon on pending request | Confirmation modal appears | | |
| 3 | Read confirmation message | Shows leave dates and days | | |
| 4 | Click "Yes, Cancel Leave" | Success message displayed | | |
| 5 | Verify request removed | Request no longer in list | | |
| 6 | Check leave balance | Balance restored (if applicable) | | |

---

#### TC-EA-008: Cannot Cancel Approved Leave
**Priority**: Medium
**Pre-condition**: Employee has approved leave request

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to "My Leaves" tab | Approved requests shown | | |
| 2 | Check for cancel button | No cancel button on approved requests | | |

---

#### TC-EA-009: Form Reset Functionality
**Priority**: Low
**Pre-condition**: Employee on apply leave form

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Fill all form fields | Fields populated | | |
| 2 | Click "Reset" button | All fields cleared | | |
| 3 | Verify default state | Form returns to initial state | | |

---

### B. EMPLOYER SIDE - LEAVE APPROVAL

#### TC-ER-001: View Leave Requests Dashboard
**Priority**: High
**Pre-condition**: Employer logged in, leave requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to "Leaves" menu | Leave Management page loads | | |
| 2 | Verify statistics cards | Shows Total, Pending, Approved, Rejected counts | | |
| 3 | Check accuracy of counts | Numbers match actual requests | | |
| 4 | Verify default tab | "Pending" tab selected by default | | |

**Test Data**:
- Expected: 10 total, 3 pending, 5 approved, 2 rejected

---

#### TC-ER-002: View Pending Leave Requests
**Priority**: High
**Pre-condition**: Employer logged in, pending requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Pending" tab | Only pending requests displayed | | |
| 2 | Verify request details | Employee name, leave type, dates, days, reason shown | | |
| 3 | Check action buttons | "Approve" and "Reject" buttons visible | | |
| 4 | Verify employee names | Full names displayed correctly | | |

---

#### TC-ER-003: Approve Leave Request
**Priority**: High
**Pre-condition**: Employer logged in, pending request exists

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Approve" button on a request | Approval modal opens | | |
| 2 | Verify modal content | Shows employee name, leave period, days, reason | | |
| 3 | Enter optional remarks: "Approved" | Text area accepts input | | |
| 4 | Click "Approve" button | Processing indicator shown | | |
| 5 | Verify success message | "Leave request approved successfully" | | |
| 6 | Check request moved to Approved tab | Request visible in "Approved" tab | | |
| 7 | Verify status badge updated | Shows green "approved" badge | | |
| 8 | Check employee leave balance | Balance deducted for approved days | | |
| 9 | Verify pending count decreased | Statistics card updated | | |

**Test Data**:
- Employee: John Doe
- Leave Type: Casual Leave
- Days: 3
- Expected Balance After: [Original - 3]

---

#### TC-ER-004: Approve Leave Without Remarks
**Priority**: Medium
**Pre-condition**: Employer logged in, pending request exists

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Approve" on a request | Modal opens | | |
| 2 | Leave remarks field empty | Field empty | | |
| 3 | Click "Approve" | Request approved successfully | | |
| 4 | Verify approval without remarks | System accepts approval without remarks | | |

---

#### TC-ER-005: Reject Leave Request - With Reason
**Priority**: High
**Pre-condition**: Employer logged in, pending request exists

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Reject" button on a request | Rejection modal opens | | |
| 2 | Verify modal content | Shows employee details and leave info | | |
| 3 | Enter rejection reason: "Insufficient staffing during this period" | Text accepted | | |
| 4 | Click "Reject" button | Processing shown | | |
| 5 | Verify success message | "Leave request rejected" displayed | | |
| 6 | Check request moved to Rejected tab | Request in "Rejected" tab | | |
| 7 | Verify status badge | Shows red "rejected" badge | | |
| 8 | Check employee balance | Balance unchanged (request rejected) | | |

**Test Data**:
- Rejection Reason: "Insufficient staffing during this period"

---

#### TC-ER-006: Reject Leave Request - Without Reason
**Priority**: High
**Pre-condition**: Employer logged in, pending request exists

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Reject" button | Modal opens | | |
| 2 | Leave reason field empty | Field empty | | |
| 3 | Click "Reject" button | Button should be disabled OR error message shown | | |
| 4 | Enter reason and retry | Rejection succeeds | | |

**Expected**: System enforces mandatory rejection reason

---

#### TC-ER-007: Filter Leave Requests - Search by Employee
**Priority**: Medium
**Pre-condition**: Employer logged in, multiple requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Enter employee name in search box: "John" | Table filters in real-time | | |
| 2 | Verify filtered results | Only requests from matching employees shown | | |
| 3 | Clear search box | All requests displayed again | | |

---

#### TC-ER-008: Filter Leave Requests - Search by Leave Type
**Priority**: Medium
**Pre-condition**: Employer logged in, multiple leave types exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Enter leave type in search: "Sick" | Table filters | | |
| 2 | Verify results | Only sick leave requests shown | | |

---

#### TC-ER-009: View Approved Leave Requests
**Priority**: Medium
**Pre-condition**: Approved requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Approved" tab | Only approved requests shown | | |
| 2 | Verify no action buttons | No Approve/Reject buttons visible | | |
| 3 | Check status badges | All show green "approved" | | |

---

#### TC-ER-010: View Rejected Leave Requests
**Priority**: Medium
**Pre-condition**: Rejected requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Rejected" tab | Only rejected requests shown | | |
| 2 | Verify no action buttons | No action buttons visible | | |
| 3 | Check status badges | All show red "rejected" | | |

---

#### TC-ER-011: View All Leave Requests with Status Filter
**Priority**: Medium
**Pre-condition**: Mixed status requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "All" tab | All requests shown | | |
| 2 | Select "Pending" from status dropdown | Only pending requests filtered | | |
| 3 | Select "Approved" from dropdown | Only approved shown | | |
| 4 | Select "All Status" | All requests shown again | | |

---

#### TC-ER-012: Refresh Leave Requests
**Priority**: Low
**Pre-condition**: Employer logged in

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Refresh" button | Loading indicator shown | | |
| 2 | Wait for refresh | Latest data loaded | | |
| 3 | Verify statistics updated | Counts reflect current state | | |

---

#### TC-ER-013: Cancel Approval Modal
**Priority**: Low
**Pre-condition**: Employer viewing approval modal

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Approve" on request | Modal opens | | |
| 2 | Click "Cancel" button | Modal closes | | |
| 3 | Verify no changes | Request still pending | | |

---

#### TC-ER-014: Cancel Rejection Modal
**Priority**: Low
**Pre-condition**: Employer viewing rejection modal

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Click "Reject" on request | Modal opens | | |
| 2 | Enter reason | Text entered | | |
| 3 | Click "Cancel" button | Modal closes | | |
| 4 | Verify no changes | Request still pending | | |

---

### C. INTEGRATION & END-TO-END TESTS

#### TC-INT-001: Complete Leave Request Workflow
**Priority**: Critical
**Pre-condition**: Employee and employer accounts exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Login as employee | Dashboard loads | | |
| 2 | Check initial leave balance | Note: 12 days Casual Leave | | |
| 3 | Apply for 3 days leave | Request submitted | | |
| 4 | Verify status is "Pending" | Yellow pending badge | | |
| 5 | Logout and login as employer | Employer dashboard loads | | |
| 6 | Navigate to Leaves | See new pending request | | |
| 7 | Approve the request | Approval successful | | |
| 8 | Logout and login as employee | Employee dashboard loads | | |
| 9 | Check leave status | Shows "Approved" with green badge | | |
| 10 | Verify balance updated | Shows 9 days remaining | | |

---

#### TC-INT-002: Leave Rejection Workflow
**Priority**: Critical
**Pre-condition**: Employee and employer accounts exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Login as employee | Dashboard loads | | |
| 2 | Apply for 5 days leave | Request submitted | | |
| 3 | Logout and login as employer | Employer dashboard | | |
| 4 | Reject request with reason | Rejection successful | | |
| 5 | Logout and login as employee | Employee dashboard | | |
| 6 | Check request status | Shows "Rejected" with red badge | | |
| 7 | Verify balance unchanged | Balance same as before request | | |

---

#### TC-INT-003: Leave Cancellation Workflow
**Priority**: High
**Pre-condition**: Employee has pending request

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Login as employee | Dashboard loads | | |
| 2 | Navigate to "My Leaves" | See pending request | | |
| 3 | Cancel the request | Request deleted | | |
| 4 | Logout and login as employer | Employer dashboard | | |
| 5 | Check leave requests | Cancelled request not visible | | |

---

#### TC-INT-004: Multiple Concurrent Leave Requests
**Priority**: Medium
**Pre-condition**: Employee has sufficient balance

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Apply for leave: Days 1-3 (3 days) | Request 1 created | | |
| 2 | Apply for leave: Days 10-12 (3 days) | Request 2 created | | |
| 3 | Verify both visible in "My Leaves" | Both shown | | |
| 4 | Employer approves Request 1 | Balance reduced by 3 | | |
| 5 | Employer approves Request 2 | Balance reduced by 3 more | | |
| 6 | Verify total deduction | 6 days total deducted | | |

---

### D. NEGATIVE TEST CASES

#### TC-NEG-001: Submit Leave Without Selecting Type
**Priority**: Medium
**Pre-condition**: Employee on apply leave form

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Enter dates without selecting leave type | Dates entered | | |
| 2 | Click Submit | Validation error: "Please fill in all required fields" | | |

---

#### TC-NEG-002: Access Approval Functions as Employee
**Priority**: High
**Pre-condition**: Employee logged in

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Try to access `/leaves` URL directly | Employee should not have approve/reject buttons OR route protected | | |
| 2 | Verify permissions | Employee cannot approve/reject | | |

---

#### TC-NEG-003: Approve Already Processed Request
**Priority**: Medium
**Pre-condition**: Request already approved

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Try to approve already approved request (via API) | Error: "Leave request not found or already processed" | | |

---

#### TC-NEG-004: Apply Leave for Past Dates (Bypass Client Validation)
**Priority**: Medium
**Pre-condition**: Direct API access

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Send POST request with past dates via API client | Server validation error OR request denied | | |

---

### E. UI/UX TEST CASES

#### TC-UX-001: Responsive Design - Mobile View
**Priority**: Medium
**Pre-condition**: Access from mobile device or responsive mode

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Resize browser to mobile width | Layout adjusts properly | | |
| 2 | Verify table scrollable | Horizontal scroll works | | |
| 3 | Check modals responsive | Modals fit screen | | |
| 4 | Test all buttons accessible | Buttons reachable on small screen | | |

---

#### TC-UX-002: Loading States
**Priority**: Low
**Pre-condition**: Slow network simulation

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to leave page with slow network | Loading spinner shown | | |
| 2 | Submit leave request with slow network | Button shows "Submitting..." | | |
| 3 | Approve request with slow network | "Approving..." state shown | | |

---

#### TC-UX-003: Empty States
**Priority**: Low
**Pre-condition**: No leave requests exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to employer leave page | Empty state message: "No leave requests found" | | |
| 2 | Check each tab | Appropriate empty message for each tab | | |

---

#### TC-UX-004: Status Badge Colors
**Priority**: Low
**Pre-condition**: Requests with different statuses exist

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | View pending request | Yellow badge | | |
| 2 | View approved request | Green badge | | |
| 3 | View rejected request | Red badge | | |

---

## Performance Test Cases

#### TC-PERF-001: Load Many Leave Requests
**Priority**: Medium
**Pre-condition**: 100+ leave requests in system

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Navigate to employer leaves page | Page loads within 3 seconds | | |
| 2 | Switch between tabs | Tab switch instant (<500ms) | | |
| 3 | Search/filter requests | Results update within 1 second | | |

---

## Security Test Cases

#### TC-SEC-001: Cross-Tenant Data Access
**Priority**: Critical
**Pre-condition**: Multiple tenants in system

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Login as Tenant A employer | Dashboard loads | | |
| 2 | View leave requests | Only Tenant A requests shown | | |
| 3 | Try to access Tenant B request via API | 403 Forbidden or 404 Not Found | | |

---

#### TC-SEC-002: Role-Based Access Control
**Priority**: Critical
**Pre-condition**: Employee account exists

| Step | Action | Expected Result | Status | Notes |
|------|--------|----------------|--------|-------|
| 1 | Login as employee | Dashboard loads | | |
| 2 | Try to access approve API endpoint | 403 Forbidden | | |
| 3 | Try to access other employee's leave balance | 403 Forbidden | | |

---

## Test Execution Summary Template

| Test Case ID | Test Case Name | Priority | Status | Tested By | Date | Notes |
|--------------|----------------|----------|--------|-----------|------|-------|
| TC-EA-001 | View Leave Balance | High | | | | |
| TC-EA-002 | Apply Leave - Valid | High | | | | |
| TC-EA-003 | Apply Leave - Insufficient | High | | | | |
| TC-ER-001 | View Dashboard | High | | | | |
| TC-ER-003 | Approve Leave | High | | | | |
| TC-ER-005 | Reject Leave | High | | | | |
| TC-INT-001 | Complete Workflow | Critical | | | | |
| TC-INT-002 | Rejection Workflow | Critical | | | | |

---

## Bug Report Template

**Bug ID**: BUG-LM-XXX
**Title**: [Short description]
**Severity**: Critical/High/Medium/Low
**Priority**: P1/P2/P3/P4
**Module**: Leave Management
**Test Case**: [TC-ID]
**Reported By**: [Name]
**Date**: [Date]

**Description**:
[Detailed description of the bug]

**Steps to Reproduce**:
1.
2.
3.

**Expected Result**:
[What should happen]

**Actual Result**:
[What actually happened]

**Screenshots/Logs**:
[Attach if applicable]

**Environment**:
- Browser:
- OS:
- Backend Version:
- Frontend Version:

**Status**: New/In Progress/Fixed/Closed
**Assigned To**: [Developer name]

---

## Test Metrics

### Coverage Targets
- **Functional Coverage**: 100% of critical features
- **Code Coverage**: >80%
- **Regression Tests**: All high/critical test cases

### Success Criteria
- All Critical and High priority test cases pass
- No P1/P2 bugs open
- Performance within acceptable limits
- Security tests pass

### Test Environment
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5174
- **Database**: SQLite (test database)
- **Browser**: Chrome, Firefox, Edge

---

## Notes for Testers

1. **Test Data Setup**: Run `python scripts/create_test_users.py` before testing
2. **Database Reset**: Clear database between test runs for consistency
3. **API Testing**: Use Postman/Swagger UI for API-level tests
4. **Browser DevTools**: Monitor network tab for API errors
5. **Screenshots**: Capture screenshots for any issues found
6. **Log Files**: Check backend logs for server-side errors

---

**Document Version**: 1.0
**Last Updated**: [Current Date]
**Author**: Test Team
