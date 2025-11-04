# Quick Test Reference Card

## Start Testing in 5 Minutes

### 1. Environment Check ✓
```bash
# Backend: Should be running on http://127.0.0.1:8000
# Frontend: Should be running on http://127.0.0.1:5174
```

### 2. Test Credentials
| User | Password | Role |
|------|----------|------|
| saasadmin | admin123 | System Admin |
| employer | employer123 | HR Manager |
| employee1 | employee123 | Employee |

### 3. Critical Tests (Run These First!)

#### Test 1: Login Works ⭐ CRITICAL
```
1. Open: http://127.0.0.1:5174
2. Login as: employer / employer123
3. Should see: Dashboard with statistics
4. Check console: No errors, token saved
✓ PASS if: Dashboard loads with data
✗ FAIL if: Redirected back to login or errors shown
```

#### Test 2: View Employees ⭐ CRITICAL
```
1. After login, click: "Employees" in sidebar
2. Should see: List of employees
3. Try search: Enter employee name
4. Try filter: Select department/location
✓ PASS if: Employees display and filters work
✗ FAIL if: Empty list or error shown
```

#### Test 3: Employee Login ⭐ CRITICAL
```
1. Logout (if logged in)
2. Login as: employee1 / employee123
3. Should see: Employee dashboard (NOT employer dashboard)
4. Check menu: Only employee options visible
✓ PASS if: Employee dashboard shows, limited menu
✗ FAIL if: Can see employer features or error
```

#### Test 4: Data Isolation ⭐ CRITICAL
```
1. Login as employer
2. Note: Which employees you see
3. Logout, login as employee1
4. Check: Can only see own data
✓ PASS if: Employee sees only personal info
✗ FAIL if: Employee can see other employees' data
```

#### Test 5: Payroll Access ⭐ CRITICAL
```
Employer:
1. Login as employer
2. Navigate to: Payroll
3. Should see: Payroll processing options

Employee:
1. Login as employee1
2. Navigate to: Payslips
3. Should see: List of own payslips
✓ PASS if: Both can access respective payroll features
✗ FAIL if: 403 Forbidden or crash
```

---

## Test Execution Tracking

### How to Mark Results in Excel

Open: `HR_Payroll_Test_Tracker_*.xlsx`

For each test:
1. **Status Column**: Type one of:
   - `Pass` - Works as expected ✓
   - `Fail` - Doesn't work ✗
   - `Blocked` - Can't test (dependency issue)
   - `Not Tested` - Haven't tested yet

2. **Tester Column**: Your name

3. **Date Column**: Today's date (YYYY-MM-DD)

4. **Comments**: Any notes or observations

5. **Bug ID**: If failed, note bug number (BUG-001, BUG-002, etc.)

### Bug Reporting

Go to "Bug_Tracking" sheet and log:

| Field | Example |
|-------|---------|
| Bug ID | BUG-001 |
| TC ID | EA-023 |
| Summary | Cannot add new employee |
| Description | When clicking Save, form shows validation error even with all fields filled |
| Severity | High |
| Priority | P1 |
| Status | Open |

---

## Common Testing Patterns

### Pattern 1: CRUD Testing (Create, Read, Update, Delete)

**Example: Employee Management**
```
CREATE:
1. Navigate to Employees
2. Click "Add Employee"
3. Fill all required fields
4. Click Save
5. Verify: Employee appears in list

READ:
1. Click on employee name
2. Verify: All details display correctly

UPDATE:
1. Click Edit
2. Change phone number
3. Click Save
4. Verify: Changes saved and visible

DELETE:
1. Select employee
2. Click Delete
3. Confirm
4. Verify: Employee removed from list
```

### Pattern 2: Workflow Testing

**Example: Leave Approval Flow**
```
APPLY (as employee):
1. Login as employee1
2. Go to Leave
3. Click Apply
4. Fill dates and reason
5. Submit
6. Verify: Status = "Pending"

APPROVE (as employer):
1. Logout, login as employer
2. Go to Leaves
3. Find pending request
4. Click Approve
5. Verify: Status = "Approved"

VERIFY (as employee):
1. Logout, login as employee1
2. Go to Leave
3. Verify: Status = "Approved"
4. Verify: Leave balance deducted
```

### Pattern 3: API Testing

**Using API Docs: http://127.0.0.1:8000/docs**
```
1. Open API docs
2. Click "Authorize"
3. Login to get token
4. Paste token in authorization
5. Try any endpoint
6. Check response
```

---

## Debug Checklist

### If Login Fails:

1. **Check browser console (F12):**
   ```
   Should see:
   [AuthContext] Login attempt for user: employer
   [AuthContext] Login response: {...}
   [AuthContext] Token saved, verifying: Token exists

   Should NOT see:
   401 Unauthorized
   Network Error
   ```

2. **Check localStorage:**
   ```javascript
   // In browser console, type:
   localStorage.getItem('accessToken')
   // Should return: "eyJ..." (long string)
   ```

3. **Check backend is running:**
   ```
   Visit: http://127.0.0.1:8000/docs
   Should see: API documentation page
   ```

### If Dashboard Shows No Data:

1. **Check Network tab (F12):**
   ```
   Look for:
   GET /api/v1/employees/ - Should be 200 OK
   GET /api/v1/locations/ - Should be 200 OK

   NOT:
   401 Unauthorized
   404 Not Found
   ```

2. **Check backend has data:**
   ```bash
   # Open backend terminal, run:
   python -c "from app.db.session import SessionLocal; from app.models.employee import Employee; db = SessionLocal(); print(f'Employees: {db.query(Employee).count()}'); db.close()"

   # Should show: Employees: X (where X > 0)
   ```

### If Getting Errors:

1. **Check both server terminals:**
   - Backend terminal: Look for Python errors
   - Frontend terminal: Look for build errors

2. **Check browser console:**
   - Look for red error messages
   - Note the URL that's failing

3. **Try hard refresh:**
   - Press Ctrl + Shift + R (Windows)
   - Or Cmd + Shift + R (Mac)

---

## Testing Priority Matrix

### Priority Order:

1. **CRITICAL - Test First (Must Work)**
   - Login (all roles)
   - View dashboard
   - View employees
   - Data isolation
   - Security (no unauthorized access)

2. **HIGH - Test Second (Should Work)**
   - Add/Edit/Delete employees
   - Mark attendance
   - Apply/Approve leaves
   - Process payroll
   - Generate reports

3. **MEDIUM - Test Third (Good to Have)**
   - Bulk upload
   - Export data
   - Advanced filters
   - Custom reports

4. **LOW - Test Last (Nice to Have)**
   - UI polish
   - Animations
   - Browser compatibility
   - Mobile responsive

---

## Quick Status Check

After each testing session, update:

```
Date: ___________
Time Spent: ___________
Tests Executed: _____ / 118
Tests Passed: _____
Tests Failed: _____
Bugs Found: _____

Status: ○ On Track  ○ At Risk  ○ Blocked

Next Session: _____________________
```

---

## Emergency Contacts

**If Servers Crash:**
```bash
# Kill all processes
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Restart backend
cd HR_Payroll
./venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000

# Restart frontend (new terminal)
cd HR_Payroll/frontend
npm run dev
```

**If Database Corrupted:**
```bash
# Backup current database
copy hr_payroll.db hr_payroll_backup.db

# Reinitialize (WARNING: loses data!)
# Delete hr_payroll.db and restart backend
```

---

## Test Coverage Goal

### Minimum for Release:
- ✓ All CRITICAL tests: 100% pass
- ✓ All HIGH tests: 90%+ pass
- ✓ All security tests: 100% pass
- ✓ No P0 (blocker) bugs open

### Good for Release:
- ✓ All MEDIUM tests: 80%+ pass
- ✓ No P1 (critical) bugs open
- ✓ Core workflows tested end-to-end

### Excellent for Release:
- ✓ All tests: 95%+ pass
- ✓ All bugs documented
- ✓ Performance tested
- ✓ Cross-browser tested

---

**Print this reference card and keep it handy while testing!**

_Quick Reference v1.0 | 2025-11-03_
