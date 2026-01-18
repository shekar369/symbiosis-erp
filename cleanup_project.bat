@echo off
REM Project Cleanup Script - HR Payroll System
REM This script removes temporary, cache, and obsolete files
REM Created: 2025-11-14

echo ========================================
echo HR Payroll System - Project Cleanup
echo ========================================
echo.

REM Create cleanup log
set LOGFILE=cleanup_log_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
set LOGFILE=%LOGFILE: =0%

echo Cleanup started at %date% %time% > %LOGFILE%
echo. >> %LOGFILE%

REM Counter for deleted items
set /a DELETED_FILES=0
set /a DELETED_DIRS=0

echo [1/8] Removing old SQLite database files...
echo [1/8] Removing old SQLite database files... >> %LOGFILE%
if exist "hr_payroll.db" (
    del /F /Q "hr_payroll.db" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted hr_payroll.db >> %LOGFILE%
)
if exist "migrations\hr_payroll.db" (
    del /F /Q "migrations\hr_payroll.db" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted migrations\hr_payroll.db >> %LOGFILE%
)
if exist "test.db.backup" (
    del /F /Q "test.db.backup" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted test.db.backup >> %LOGFILE%
)

echo [2/8] Removing Python cache directories...
echo [2/8] Removing Python cache directories... >> %LOGFILE%
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        rd /S /Q "%%d" 2>nul && set /a DELETED_DIRS+=1 && echo   - Deleted %%d >> %LOGFILE%
    )
)

echo [3/8] Removing pytest cache...
echo [3/8] Removing pytest cache... >> %LOGFILE%
if exist ".pytest_cache\" (
    rd /S /Q ".pytest_cache" 2>nul && set /a DELETED_DIRS+=1 && echo   - Deleted .pytest_cache >> %LOGFILE%
)

echo [4/8] Removing test and debug scripts from root...
echo [4/8] Removing test and debug scripts from root... >> %LOGFILE%
for %%f in (
    test_attendance_upload.py
    test_template_generation.py
    test_employee_template_generation.py
    test_passwords.py
    test_connection.py
    test_db_url.py
    test_api_endpoints.py
    test_api_response.py
    test_employee_setup.py
    test_employee_management.py
    test_employee_dashboard.py
    test_employee_detail_api.py
    test_employee_me_complete.py
    test_payslip_api.py
    analyze_excel.py
    analyze_attendance_sheet.py
    analyze_employee_sheet.py
    check_bank.py
    check_migrations.py
    check_employees.py
    check_leave_balances.py
    check_payslips.py
    check_ctc_calculation.py
    check_employee_status.py
    debug_wage_calc.py
    debug_wage_calc2.py
    create_db.py
    setup_db.py
    set_password.py
    reset_pg_password.py
    clear_failed_transaction.py
    create_tables.py
    add_bank_table.py
    populate_attendance.py
    recreate_advances_table.py
    process_last_2_months_payroll.py
    fix_salary_calculations.py
    fix_lop_balance.py
    fix_lop_db.py
    read_excel.py
    create_indian_employees.py
    setup_leave_types.py
    setup_leave_balances.py
) do (
    if exist "%%f" (
        del /F /Q "%%f" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted %%f >> %LOGFILE%
    )
)

echo [5/8] Removing SQL script files...
echo [5/8] Removing SQL script files... >> %LOGFILE%
for %%f in (
    reset_password.sql
    fix_lop.sql
    create_missing_tables.sql
) do (
    if exist "%%f" (
        del /F /Q "%%f" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted %%f >> %LOGFILE%
    )
)

echo [6/8] Removing temporary Excel and test files...
echo [6/8] Removing temporary Excel and test files... >> %LOGFILE%
for %%f in (
    "HR_Payroll_Test_Tracker_20251103_200221.xlsx"
    "HR_Payroll_Test_Tracker_20251103_202139.xlsx"
    "LEAVE_MANAGEMENT_TEST_SHEET.csv"
    "LEAVE_MANAGEMENT_TEST_CASES.md"
) do (
    if exist %%f (
        del /F /Q %%f 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted %%f >> %LOGFILE%
    )
)

echo [7/8] Removing temporary upload templates...
echo [7/8] Removing temporary upload templates... >> %LOGFILE%
for %%f in (
    "uploads\templates\attendance_template_2024_04_20251107_034646.xlsx"
    "uploads\templates\attendance_template_2025_08_20251114_025426.xlsx"
    "uploads\templates\attendance_template_2025_09_20251114_024910.xlsx"
    "uploads\templates\attendance_template_2025_10_20251114_013615.xlsx"
    "uploads\templates\attendance_template_2025_10_20251114_022035.xlsx"
    "uploads\templates\attendance_template_2025_10_20251114_024646.xlsx"
    "uploads\templates\employee_template_20251107_080024.xlsx"
) do (
    if exist %%f (
        del /F /Q %%f 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted %%f >> %LOGFILE%
    )
)

echo [8/8] Removing miscellaneous temporary files...
echo [8/8] Removing miscellaneous temporary files... >> %LOGFILE%
if exist "NUL" (
    del /F /Q "NUL" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted NUL >> %LOGFILE%
)
if exist "package-lock.json" (
    del /F /Q "package-lock.json" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted root package-lock.json >> %LOGFILE%
)
REM Check and remove Excel lock files
for /f "delims=" %%f in ('dir /s /b "~$*.xlsx" 2^>nul') do (
    del /F /Q "%%f" 2>nul && set /a DELETED_FILES+=1 && echo   - Deleted Excel lock file: %%f >> %LOGFILE%
)

REM Check for config_new.py and compare with config.py
if exist "app\config_new.py" (
    echo   - Found app\config_new.py - needs manual review >> %LOGFILE%
    echo   WARNING: app\config_new.py found - please review manually before deleting
)

echo.
echo ========================================
echo Cleanup Summary
echo ========================================
echo.
echo Deleted Files: %DELETED_FILES% >> %LOGFILE%
echo Deleted Directories: %DELETED_DIRS% >> %LOGFILE%
echo.
echo Deleted Files: %DELETED_FILES%
echo Deleted Directories: %DELETED_DIRS%
echo.
echo Cleanup completed at %date% %time% >> %LOGFILE%
echo Log file: %LOGFILE%
echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
pause
