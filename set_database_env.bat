@echo off
echo Unsetting old DATABASE_URL environment variable...
set DATABASE_URL=
echo Done! DATABASE_URL will now be read from .env file
echo.
echo Current DATABASE_URL from .env: postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll
