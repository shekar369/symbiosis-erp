# HR Payroll System - Quick Start Guide

## Current Status: ✅ FULLY OPERATIONAL

Both frontend and backend are running and integrated!

## Access the Application

### Frontend (React Web App)
**URL**: http://localhost:5174

### Backend API
**URL**: http://127.0.0.1:8000
**API Docs**: http://127.0.0.1:8000/docs

### Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

## What's Running

### Backend Server (FastAPI)
- Port: 8000
- Status: ✅ Running
- Shell ID: d4fef7
- Features:
  - JWT Authentication
  - 30+ Database Tables
  - Complete REST API
  - Auto-reload enabled

### Frontend Server (Vite)
- Port: 5174
- Status: ✅ Running
- Shell ID: f38fc9
- Features:
  - React 18
  - Tailwind CSS v3
  - Hot Module Replacement (HMR)

## How to Use

### 1. Open the Web Application
Navigate to: **http://localhost:5174**

### 2. Login
Use the credentials above to log in

### 3. Explore the Features

#### Dashboard
- View key metrics (employees, attendance, payroll)
- Recent activity feed
- Upcoming events

#### Employees
- **List**: View all employees
- **Search**: Filter employees by name, code, or email
- **Create**: Click "Add Employee" button
- **Edit**: Click the edit icon (pencil) on any row
- **Delete**: Click the delete icon (trash) with confirmation

#### Attendance
- **View Records**: See all attendance entries
- **Add Record**: Click "Add Record" button
- **Upload Bulk**: Click "Upload Excel" to import attendance data
- **Filters**: Filter by employee, date range

#### Wages
- **View Statements**: See all wage calculations
- **Filter**: By employee ID, month, year
- **Status**: Track payment status (DRAFT, CALCULATED, APPROVED, PAID)

#### Leaves
- Coming soon - placeholder page

#### Reports
- Coming soon - placeholder page

## API Testing

### Using Swagger UI
1. Open: http://127.0.0.1:8000/docs
2. Click "Authorize" button
3. Login with admin credentials to get token
4. Token is automatically used for all requests

### Example API Calls

#### Get Authentication Token
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### List Tenants (Protected Route)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/tenants/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### List Employees
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/employees/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Stopping the Servers

### Stop Backend
```bash
# Use the KillShell tool with ID: d4fef7
```

### Stop Frontend
```bash
# Use the KillShell tool with ID: f38fc9
```

Or press Ctrl+C in the terminal where they're running

## Restarting the Servers

### Start Backend
```bash
./venv/Scripts/uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```

## Database

### Current Database
- **Type**: SQLite
- **File**: hr_payroll.db
- **Location**: Project root

### Sample Data Loaded
- ✅ 1 Demo Tenant (Demo Company)
- ✅ 3 Departments (Engineering, HR, Sales)
- ✅ 4 Designations (Software Engineer, HR Manager, Sales Executive, Manager)
- ✅ 3 Grades (Junior, Mid-Level, Senior)
- ✅ 1 Admin User (admin/admin123)

### Database Scripts
```bash
# Reinitialize database
python scripts/init_database.py

# Reseed sample data
python scripts/seed_data.py

# Create new superuser
python scripts/create_superuser.py
```

## Project Structure

```
HR_Payroll/
├── app/                    # Backend (FastAPI)
│   ├── api/               # API endpoints
│   ├── models/            # 30+ database tables
│   ├── schemas/           # Pydantic validation
│   ├── crud/              # Database operations
│   └── main.py            # App entry point
├── frontend/              # Frontend (React)
│   └── src/
│       ├── pages/        # Dashboard, Employees, etc.
│       ├── components/   # Reusable UI components
│       └── api/          # API client services
└── scripts/              # Database utilities
```

## Common Issues & Solutions

### Frontend Port Already in Use
If port 5173 or 5174 is in use, Vite will automatically try the next available port. Check the console output for the actual port.

### CORS Errors
The backend `.env` file includes CORS origins for:
- localhost:5173
- localhost:5174
- 127.0.0.1:5173
- 127.0.0.1:5174

If you see CORS errors, make sure you're using one of these URLs.

### Authentication Errors
- Clear browser localStorage and try logging in again
- Token expires after 30 minutes - login again
- Check that backend server is running

### Database Issues
If you see database errors:
```bash
# Reinitialize the database
python scripts/init_database.py
python scripts/seed_data.py
```

## Next Steps

### For Development
1. Implement leave management module
2. Complete reports functionality
3. Add PDF payslip generation
4. Implement WebSocket notifications
5. Add comprehensive tests

### For Production
1. Change SECRET_KEY in .env
2. Switch to PostgreSQL database
3. Set up proper logging
4. Configure HTTPS
5. Set up monitoring
6. Build frontend for production: `npm run build`

## Technologies Used

### Backend
- Python 3.12
- FastAPI 0.104.1
- SQLAlchemy 2.0
- Pydantic v2
- JWT Authentication
- SQLite/PostgreSQL

### Frontend
- React 18
- Vite 7
- Tailwind CSS 3
- React Router v6
- Axios
- Lucide Icons

## Support

- Check API documentation: http://127.0.0.1:8000/docs
- Review PROJECT_SUMMARY.md for detailed information
- Frontend README: frontend/README.md
- Backend README: README.md

---

**Status**: Both servers are running and fully integrated! 🚀

Open http://localhost:5174 to start using the application.
