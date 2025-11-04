# HR Payroll System - Testing Guide

## Quick Start

### Test Documents Created
1. **TEST_CASES.md** - Complete test case documentation (200+ test cases)
2. **HR_Payroll_Test_Tracker_[timestamp].xlsx** - Excel tracking spreadsheet (118 core test cases)

### Test Environment
- **Frontend**: http://127.0.0.1:5174
- **Backend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

### Test Credentials
| Role | Username | Password |
|------|----------|----------|
| SaaS Admin | saasadmin | admin123 |
| Employer Admin | employer | employer123 |
| Employee | employee1 | employee123 |

---

## Using the Excel Test Tracker

### Sheets Overview

1. **Summary** - Overall test execution progress and environment info
2. **SaaS_Admin** - 11 test cases for system admin
3. **Employer_Admin** - 47 test cases for HR management
4. **Employee** - 21 test cases for employee self-service
5. **Cross-Functional** - 12 test cases for multi-role scenarios
6. **Integration** - 5 test cases for API and database
7. **UI_UX** - 9 test cases for user interface
8. **Regression** - 10 critical smoke tests
9. **Bug_Tracking** - Log bugs found during testing

### How to Use the Tracker

#### 1. Start with Summary Sheet
- Review test environment details
- Check test credentials
- Note the priority breakdown

#### 2. Execute Tests by Priority

**CRITICAL (Must Test First):**
- REG-002: Login Works
- EA-001: Employer Admin Login
- EM-001: Employee Login
- EA-020: View Employees List
- EA-071: Process Monthly Payroll
- EM-040: View Payslips
- CF-002: Data Isolation

**HIGH (Test Second):**
- All authentication tests
- Core CRUD operations
- Security tests

**MEDIUM & LOW (Test Last):**
- Advanced features
- UI/UX refinements

#### 3. Recording Test Results

For each test case, update these columns:

| Column | What to Enter |
|--------|---------------|
| **Status** | Pass / Fail / Blocked / Not Tested |
| **Tester** | Your name |
| **Date** | Date tested (YYYY-MM-DD) |
| **Comments** | Any observations, notes, or issues |
| **Bug ID** | If failed, reference the bug number |

#### 4. Status Values

- **Pass**: Test executed successfully, met expected result
- **Fail**: Test did not meet expected result, bug found
- **Blocked**: Cannot test due to dependency or environment issue
- **Not Tested**: Not yet executed

#### 5. Logging Bugs

When a test fails:
1. Go to **Bug_Tracking** sheet
2. Create a new row with:
   - **Bug ID**: Auto-increment (BUG-001, BUG-002, etc.)
   - **TC ID**: Test case that failed (e.g., EA-023)
   - **Summary**: Brief description (e.g., "Cannot add new employee")
   - **Description**: Detailed steps and what went wrong
   - **Severity**: Critical / High / Medium / Low
   - **Priority**: P0 / P1 / P2 / P3
   - **Status**: Open / In Progress / Fixed / Closed
   - **Assigned To**: Developer name
   - **Date Found**: Date bug discovered
   - **Date Fixed**: Date bug resolved
3. Reference the Bug ID back in the test case sheet

#### 6. Updating Progress

The **Summary** sheet should be updated regularly:
- Update the "Passed", "Failed", "Blocked", "Not Tested" counts
- Calculate Pass % = (Passed / Total) × 100

---

## Testing Workflow

### Phase 1: Smoke Testing (Critical Priority)
**Goal**: Verify basic functionality works
**Duration**: 1-2 hours

1. Start servers (backend + frontend)
2. Execute all **Regression** sheet tests
3. If any regression test fails, STOP and fix before continuing
4. All regression tests must pass before proceeding

### Phase 2: Role-Based Testing
**Goal**: Test each user role comprehensively
**Duration**: 2-3 days

#### Day 1: Employer Admin Testing
- Execute all **Employer_Admin** sheet tests (47 tests)
- Focus on:
  - Employee management (CRUD)
  - Attendance marking
  - Payroll processing
  - Leave approval

#### Day 2: Employee Testing + Cross-Functional
- Execute all **Employee** sheet tests (21 tests)
- Execute **Cross-Functional** tests (12 tests)
- Focus on:
  - Employee self-service features
  - Data isolation between roles
  - Security testing

#### Day 3: Admin + Integration + UI
- Execute **SaaS_Admin** tests (11 tests)
- Execute **Integration** tests (5 tests)
- Execute **UI_UX** tests (9 tests)

### Phase 3: Bug Fixing & Retesting
**Goal**: Fix all critical/high bugs and retest
**Duration**: Ongoing

1. Fix bugs in priority order: Critical → High → Medium → Low
2. Retest the specific test case after bug fix
3. Run regression tests after each fix
4. Update bug status in Bug_Tracking sheet

### Phase 4: Final Validation
**Goal**: Ensure all critical paths work end-to-end
**Duration**: 1 day

1. Re-run all CRITICAL priority tests
2. Re-run all FAILED tests to verify fixes
3. Perform exploratory testing on fixed areas
4. Update final test execution summary

---

## Common Test Scenarios

### Testing Login (EA-001, EM-001, SA-001)

**Steps:**
1. Open browser, go to http://127.0.0.1:5174
2. Enter credentials
3. Click "Sign In"
4. Open browser console (F12) to check debug logs

**Expected Debug Logs:**
```
[AuthContext] Login attempt for user: employer
[AuthContext] Login response: {access_token: "...", user: {...}}
[AuthContext] Saving token to localStorage
[AuthContext] Token saved, verifying: Token exists
[Axios Interceptor] Token from localStorage: Token exists
[Axios Interceptor] Authorization header set
```

**Pass Criteria:**
- Login successful
- Redirected to dashboard
- No console errors
- Token saved in localStorage

### Testing Employee CRUD (EA-023, EA-025)

**Add Employee:**
1. Login as employer
2. Navigate to Employees page
3. Click "Add Employee" button
4. Fill required fields:
   - First Name
   - Last Name
   - Email
   - Employee ID
   - Department, Designation, Location
5. Click Save
6. Verify employee appears in list

**Edit Employee:**
1. Find employee in list
2. Click Edit icon
3. Modify phone number
4. Click Save
5. Verify changes saved

### Testing Payroll Processing (EA-071)

**Steps:**
1. Login as employer
2. Navigate to Payroll
3. Select current month
4. Click "Process Payroll"
5. Wait for processing to complete
6. Verify:
   - All active employees included
   - Salary calculations correct
   - Deductions applied
   - Net pay calculated
7. Generate pay slips
8. Download sample pay slip

### Testing Leave Flow (EM-033, EA-062)

**Apply Leave (Employee):**
1. Login as employee1
2. Navigate to Leave
3. Click "Apply Leave"
4. Select leave type (Casual/Sick)
5. Choose dates
6. Enter reason
7. Submit
8. Verify status shows "Pending"

**Approve Leave (Employer):**
1. Logout, login as employer
2. Navigate to Leaves
3. Find pending leave request
4. Click on request
5. Click "Approve"
6. Verify status changed to "Approved"

**Verify (Employee):**
1. Logout, login as employee1
2. Navigate to Leave
3. Verify leave status is "Approved"
4. Check leave balance deducted

---

## Browser Console Debugging

### Useful Console Commands

Check if token exists:
```javascript
console.log('Token:', localStorage.getItem('accessToken'))
```

Check current user:
```javascript
console.log('User:', JSON.parse(localStorage.getItem('user')))
```

Clear all auth data:
```javascript
localStorage.removeItem('accessToken')
localStorage.removeItem('user')
location.reload()
```

### Debug Log Prefixes

- `[AuthContext]` - Authentication state management
- `[Axios Interceptor]` - Auth API calls (login)
- `[API Service]` - General API calls (employees, payroll, etc.)

### Common Issues & Solutions

**Issue**: "Login succeeds but immediately logs out"
- **Check**: Is token being saved? Look for `[AuthContext] Token saved`
- **Check**: Are subsequent API calls including token? Look for `[API Service] Token from localStorage: Token exists`
- **Solution**: Fixed in api.js by using correct localStorage key

**Issue**: "401 Unauthorized after login"
- **Check**: Is Authorization header being set? Look for `Authorization header set`
- **Cause**: Token not found in localStorage or wrong key name
- **Solution**: Ensure both axios.js and api.js use 'accessToken' key

**Issue**: "Dashboard doesn't load data"
- **Check**: Network tab for API calls
- **Check**: Response status codes
- **Cause**: API calls failing or returning empty data
- **Solution**: Verify backend is running and database has data

---

## Test Completion Checklist

### Before Starting Testing
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5174
- [ ] Database initialized with seed data
- [ ] All test accounts exist (saasadmin, employer, employee1)
- [ ] Test tracker spreadsheet opened
- [ ] Browser console open for debugging

### Daily Testing Tasks
- [ ] Update test tracker with results
- [ ] Log any bugs found
- [ ] Take screenshots of issues
- [ ] Note any observations or suggestions
- [ ] Update pass/fail counts in Summary sheet

### Before Marking Testing Complete
- [ ] All CRITICAL tests passed
- [ ] All HIGH priority tests passed or have documented workarounds
- [ ] All bugs logged in Bug_Tracking sheet
- [ ] Summary sheet updated with final counts
- [ ] Sign-off obtained from stakeholders
- [ ] Test reports generated

---

## Reporting Results

### Daily Test Report Format

**Test Report - [Date]**

**Tests Executed:** X
**Tests Passed:** Y
**Tests Failed:** Z
**Pass Rate:** XX%

**Blocker Issues:**
- [List any critical issues preventing further testing]

**New Bugs Found:**
- BUG-XXX: [Brief description]
- BUG-YYY: [Brief description]

**Areas Tested:**
- [Module 1]
- [Module 2]

**Next Steps:**
- [What will be tested tomorrow]
- [Any dependencies or blockers]

### Final Test Summary Report

**Test Execution Summary Report**
**Date:** [Date]
**Tester:** [Name]
**Project:** HR Payroll System

**Overall Statistics:**
- Total Test Cases: 118
- Passed: XX
- Failed: YY
- Blocked: ZZ
- Pass Rate: XX%

**Test Coverage:**
- SaaS Admin: XX%
- Employer Admin: XX%
- Employee: XX%
- Cross-Functional: XX%
- Integration: XX%
- UI/UX: XX%
- Regression: XX%

**Critical Bugs:** X
**High Priority Bugs:** Y
**Medium Priority Bugs:** Z
**Low Priority Bugs:** W

**Recommendation:** Ready for Release / Not Ready (specify reasons)

**Sign-off:**
- QA Lead: _______________
- Project Manager: _______________
- Tech Lead: _______________

---

## Contact & Support

### Bug Severity Guidelines

**Critical:**
- Application crash
- Data loss
- Security vulnerability
- Login broken
- Core functionality completely broken

**High:**
- Major feature not working
- Workaround exists but difficult
- Affects multiple users
- Performance severely degraded

**Medium:**
- Minor feature not working
- Easy workaround available
- Cosmetic issues in important areas
- Minor performance issues

**Low:**
- Cosmetic issues
- Spelling/grammar errors
- Minor UI inconsistencies
- Feature enhancements

### Need Help?

- Check backend logs: Terminal running backend server
- Check frontend logs: Browser console (F12)
- Review TEST_CASES.md for detailed test steps
- Check API documentation: http://127.0.0.1:8000/docs

---

**Good luck with testing!**

_Last Updated: 2025-11-03_
