# HR Payroll System - Project Summary

Complete full-stack HR and Payroll Management System with FastAPI backend and React frontend.

## Project Overview

A modern, scalable web application for managing human resources and payroll operations. The system supports multi-tenant architecture, employee management, attendance tracking, wage calculations, leave management, and comprehensive reporting.

## Architecture

### Backend (FastAPI)
- **Language**: Python 3.12
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with passlib + bcrypt
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2

### Frontend (React + Vite)
- **Language**: JavaScript (ES6+)
- **Framework**: React 18
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 3
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Quick Start

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python scripts/init_database.py
python scripts/seed_data.py
python scripts/create_superuser.py
```

4. Start server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend available at: http://127.0.0.1:8000
API docs at: http://127.0.0.1:8000/docs

### Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend available at: http://localhost:5173

### Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## Database Schema

### Core Tables (30+ total)

#### Organization Structure
- **tenants**: Multi-tenant organizations
- **departments**: Organizational departments
- **designations**: Job positions
- **grades**: Employee grades/levels

#### Employee Management
- **employees**: Employee master data
- **employee_addresses**: Employee addresses
- **employee_documents**: Employee documents (Aadhar, PAN, etc.)

#### Attendance & Time
- **attendance**: Daily attendance records
- **shifts**: Work shift definitions
- **holidays**: Holiday calendar

#### Leave Management
- **leave_types**: Types of leaves
- **leave_balances**: Employee leave balances
- **leave_requests**: Leave applications

#### Payroll & Wages
- **wage_statements**: Monthly wage calculations
- **payroll**: Payroll processing records
- **salary_structures**: Salary component definitions
- **overtime**: Overtime records
- **advances**: Advance payments
- **loans**: Loan records

#### Vendor Management
- **vendors**: Vendor master data
- **vendor_addresses**: Vendor addresses
- **vendor_contacts**: Vendor contacts

#### Audit & Security
- **users**: System users
- **audit_logs**: System audit trail

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Tenants
- `GET /api/v1/tenants` - List tenants
- `POST /api/v1/tenants` - Create tenant
- `GET /api/v1/tenants/{id}` - Get tenant
- `PUT /api/v1/tenants/{id}` - Update tenant
- `DELETE /api/v1/tenants/{id}` - Delete tenant

### Employees
- `GET /api/v1/employees` - List employees
- `POST /api/v1/employees` - Create employee
- `GET /api/v1/employees/{id}` - Get employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `GET /api/v1/attendance` - List attendance records
- `POST /api/v1/attendance` - Create attendance record
- `POST /api/v1/attendance/upload` - Upload attendance file

### Wages
- `GET /api/v1/wage` - List wage statements
- `GET /api/v1/wage/{id}` - Get wage statement

### Leaves
- `GET /api/v1/leave` - List leave requests
- `POST /api/v1/leave` - Create leave request
- `PUT /api/v1/leave/{id}` - Update leave request

### Payroll
- `GET /api/v1/payroll` - List payroll records
- `POST /api/v1/payroll/process` - Process payroll

### Additional Endpoints
- Holidays, Shifts, Reports, Admin, Auditor, Health

## Frontend Features

### Pages & Components

#### Authentication
- Login page with JWT token management
- Protected route wrapper
- Auto-redirect on 401 errors

#### Dashboard
- Key metrics display
- Recent activity feed
- Upcoming events calendar
- Statistics cards

#### Employee Management
- Employee list with search
- Create/Edit employee modal
- Delete with confirmation
- Status badges (ACTIVE/INACTIVE/TERMINATED)

#### Attendance Tracking
- Manual attendance entry
- Bulk upload via Excel/CSV
- Status indicators
- Date filtering

#### Wage Statements
- Monthly wage views
- Filter by employee/month/year
- Earnings and deductions breakdown
- Net salary display
- Status tracking

#### Layout Components
- **Sidebar**: Main navigation menu
- **Header**: User info and notifications
- **Layout**: Main layout wrapper with routing

#### Common Components
- **Button**: Customizable button (variants, sizes)
- **Input**: Form input with validation
- **Table**: Data table with custom rendering
- **Modal**: Dialog for forms
- **Card**: Container for content
- **ProtectedRoute**: Authentication guard

## Key Features Implemented

### Backend
- Multi-tenant architecture
- JWT authentication with secure password hashing
- SQLAlchemy models with relationships
- Pydantic schemas for validation
- CRUD operations for all entities
- Middleware for logging and error handling
- Database session management
- API endpoint structure
- CORS configuration
- Environment-based configuration

### Frontend
- React Router for navigation
- Protected routes with authentication
- Axios interceptors for token injection
- Context API for state management
- Responsive Tailwind CSS design
- Reusable component library
- Form validation
- Error handling
- Loading states

## Project Structure

```
HR_Payroll/
├── app/                          # Backend application
│   ├── api/                      # API endpoints
│   │   ├── dependencies.py       # Dependency injection
│   │   └── v1/
│   │       ├── router.py         # Main API router
│   │       └── endpoints/        # Endpoint modules
│   ├── core/                     # Core functionality
│   │   ├── security.py           # JWT & password hashing
│   │   ├── constants.py          # App constants
│   │   └── errors.py             # Custom exceptions
│   ├── crud/                     # Database operations
│   │   ├── base.py               # Base CRUD class
│   │   └── *.py                  # Entity-specific CRUD
│   ├── db/                       # Database configuration
│   │   ├── base.py               # SQLAlchemy base
│   │   ├── session.py            # DB session
│   │   └── init_db.py            # DB initialization
│   ├── middleware/               # Custom middleware
│   │   ├── logging.py            # Request logging
│   │   ├── error_handler.py     # Error handling
│   │   └── multi_tenant.py      # Tenant isolation
│   ├── models/                   # SQLAlchemy models
│   │   └── *.py                  # Entity models
│   ├── schemas/                  # Pydantic schemas
│   │   └── *.py                  # Request/response schemas
│   ├── services/                 # Business logic
│   │   └── *.py                  # Service modules
│   ├── utils/                    # Utility functions
│   │   ├── excel_parser.py       # Excel file parsing
│   │   ├── pdf_generator.py     # PDF generation
│   │   └── validators.py        # Custom validators
│   ├── websockets/               # WebSocket handlers
│   ├── background_tasks/         # Async tasks
│   ├── config.py                 # App configuration
│   └── main.py                   # FastAPI app entry
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── api/                  # API client services
│   │   ├── components/           # React components
│   │   │   ├── common/           # Reusable components
│   │   │   └── layout/           # Layout components
│   │   ├── context/              # React Context
│   │   ├── pages/                # Page components
│   │   ├── App.jsx               # Main app
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── .env                      # Environment variables
│   ├── tailwind.config.js        # Tailwind config
│   └── vite.config.js            # Vite config
├── scripts/                      # Utility scripts
│   ├── init_database.py          # Initialize DB
│   ├── seed_data.py              # Seed sample data
│   └── create_superuser.py      # Create admin user
├── tests/                        # Test suite
├── .env                          # Backend environment
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker composition
└── README.md                     # Project documentation
```

## Technologies & Libraries

### Backend Dependencies
```
fastapi==0.104.1              # Web framework
uvicorn[standard]==0.24.0     # ASGI server
sqlalchemy==2.0.23            # ORM
pydantic==2.5.0               # Data validation
pydantic-settings==2.1.0      # Settings management
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4        # Password hashing
bcrypt==4.1.3                 # Password encryption
python-multipart==0.0.6       # File uploads
alembic==1.13.0               # Database migrations
pandas==2.1.3                 # Excel parsing
openpyxl==3.1.2               # Excel files
reportlab==4.0.7              # PDF generation
python-dotenv==1.0.0          # Environment variables
email-validator==2.3.0        # Email validation
```

### Frontend Dependencies
```
react==18.3.1                 # UI library
react-dom==18.3.1             # React DOM
react-router-dom==7.2.1       # Routing
axios==1.7.9                  # HTTP client
tailwindcss==3.4.18           # CSS framework
lucide-react==0.469.0         # Icons
```

## Development Tools

### Backend
- **Testing**: pytest with coverage
- **Linting**: pylint, black
- **API Docs**: Automatic OpenAPI/Swagger
- **Database**: SQLite (dev), PostgreSQL (prod)

### Frontend
- **Build**: Vite with HMR
- **Linting**: ESLint
- **Styling**: PostCSS + Autoprefixer

## Environment Variables

### Backend (.env)
```env
PROJECT_NAME=HR Payroll System
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///./hr_payroll.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Deployment

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000 (requires nginx config)
- Database: PostgreSQL on port 5432

### Production Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Update DATABASE_URL to PostgreSQL
- [ ] Set strong admin password
- [ ] Configure CORS origins for production domain
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure logging to file/service
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Optimize database indexes
- [ ] Configure rate limiting
- [ ] Set up CDN for static files

## Testing

### Backend Tests
```bash
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
npm test
```

## Future Enhancements

### High Priority
- [ ] Complete leave management module
- [ ] Implement reports and analytics
- [ ] PDF payslip generation
- [ ] Real-time notifications via WebSocket
- [ ] Email notifications
- [ ] Bulk operations for employees

### Medium Priority
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Advanced search and filtering
- [ ] Export data (Excel, PDF)
- [ ] Calendar view for attendance
- [ ] Mobile app (React Native)

### Low Priority
- [ ] Performance analytics dashboard
- [ ] Integration with biometric devices
- [ ] Integration with accounting software
- [ ] Employee self-service portal
- [ ] Manager approval workflows
- [ ] Customizable reports

## Known Issues

1. Node.js version warning (22.11.0 vs required 20.19+/22.12+) - Non-critical, application works fine
2. Some service modules contain placeholder implementations (TODO comments)
3. WebSocket endpoints not fully implemented
4. Background tasks need queue system (e.g., Celery)

## Security Considerations

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with expiration
- CORS configured for specific origins
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- XSS protection in React
- Environment variables for secrets
- Audit logging for sensitive operations

## Performance Optimizations

- Database indexes on foreign keys
- Pagination for large datasets
- Lazy loading in SQLAlchemy
- React code splitting
- Vite build optimization
- CDN for static assets (production)

## Maintenance

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Backup Database
```bash
# SQLite
cp hr_payroll.db hr_payroll_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump hr_payroll > backup_$(date +%Y%m%d).sql
```

### Update Dependencies
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

## Support & Documentation

- API Documentation: http://127.0.0.1:8000/docs (Swagger UI)
- Alternative API Docs: http://127.0.0.1:8000/redoc (ReDoc)
- Frontend README: [frontend/README.md](frontend/README.md)
- Backend README: [README.md](README.md)

## License

This project is proprietary software for HR and Payroll management.

## Contributors

Generated with Claude Code - AI Assistant
