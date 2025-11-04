# Symbiosis HR Payroll System

A comprehensive, production-ready HR and Payroll management system with FastAPI backend and React frontend, supporting multi-tenant SaaS architecture.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

## Overview

Symbiosis is an enterprise-grade HR and Payroll solution designed for Indian compliance requirements, supporting multiple labor acts including Contract Labour Act, Shops & Establishment Act, and Factories Act. The system provides comprehensive employee lifecycle management, automated payroll calculations, statutory compliance, and multi-location support.

## Key Features

### Core HR Management
- ✅ Multi-tenant SaaS architecture with complete data isolation
- ✅ Employee lifecycle management (onboarding to exit)
- ✅ Multi-location support with state-wise labor act compliance
- ✅ Department, designation, and grade management
- ✅ Employee self-service portal
- ✅ Document management and profiles

### Attendance & Leave
- ✅ Biometric attendance integration
- ✅ Bulk attendance upload via Excel
- ✅ Shift management and rostering
- ✅ Leave request and approval workflow
- ✅ Leave balance tracking
- ✅ Holiday calendar management

### Payroll & Wages
- ✅ Advanced wage calculation engine
- ✅ Multiple wage components (Basic, DA, HRA, Conveyance, etc.)
- ✅ Attendance-based salary computation
- ✅ Overtime calculations
- ✅ Loan and advance deductions
- ✅ Payslip generation (PDF)
- ✅ Bank transfer file generation

### Statutory Compliance
- ✅ EPF (Provident Fund) calculations and ECR generation
- ✅ ESI (Employee State Insurance) calculations
- ✅ Professional Tax calculations
- ✅ Form XIII generation
- ✅ PT Form V generation
- ✅ PF Challan summaries

### Reports & Analytics
- ✅ Attendance reports
- ✅ Payroll summaries
- ✅ Salary registers
- ✅ Payment summaries
- ✅ Dashboard analytics for all user roles

### Security & Access
- ✅ JWT-based authentication
- ✅ Role-based access control (SaaS Admin, Employer Admin, Employee)
- ✅ Comprehensive audit logging
- ✅ Multi-tenant data isolation
- ✅ Secure password hashing

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **PDF Generation**: ReportLab
- **Excel Processing**: Pandas, OpenPyXL
- **Email**: SMTP with email templates

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Icons**: Lucide React
- **State Management**: React Context API

### DevOps
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest
- **Linting**: ESLint (frontend)
- **Version Control**: Git

## Project Structure

```
symbiosis/
├── app/                    # Backend application
│   ├── api/               # API routes and endpoints
│   │   └── v1/           # API version 1
│   │       ├── endpoints/ # Individual route handlers
│   │       └── router.py  # Main API router
│   ├── core/              # Core functionality
│   │   ├── security.py    # Authentication & authorization
│   │   ├── constants.py   # System constants
│   │   └── errors.py      # Custom exceptions
│   ├── models/            # SQLAlchemy models (30+ tables)
│   ├── schemas/           # Pydantic schemas for validation
│   ├── services/          # Business logic layer
│   ├── crud/              # Database CRUD operations
│   ├── middleware/        # Custom middleware
│   ├── utils/             # Utility functions
│   │   ├── pdf_generator.py
│   │   ├── excel_parser.py
│   │   ├── bank_transfer_generator.py
│   │   └── statutory_forms_generator.py
│   ├── websockets/        # Real-time communication
│   ├── background_tasks/  # Async job processors
│   ├── db/               # Database configuration
│   ├── config.py         # App configuration
│   └── main.py           # FastAPI application entry
├── frontend/              # React frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # Reusable components
│   │   ├── contexts/     # React contexts
│   │   ├── pages/        # Page components
│   │   ├── utils/        # Utility functions
│   │   └── main.jsx      # Application entry
│   ├── public/           # Static assets
│   └── package.json      # Node dependencies
├── migrations/            # Alembic database migrations
├── tests/                 # Test suite
├── scripts/               # Utility scripts
│   ├── init_database.py
│   ├── create_test_users.py
│   └── seed_data.py
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md             # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- SQLite (included) or PostgreSQL (production)
- Git

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/shekar369/symbiosis.git
cd symbiosis
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python scripts/init_database.py

# Create test users
python scripts/create_test_users.py

# Run backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: **http://localhost:5174**

### Docker Setup (Alternative)

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop all services
docker-compose down
```

Access the application:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5174`

## Default Test Credentials

After running `python scripts/create_test_users.py`, the following test accounts are available:

| Username | Password | Role | Tenant | Access Level |
|----------|----------|------|--------|--------------|
| `saasadmin` | `admin123` | SaaS Admin | All | Full system access across all tenants |
| `employer` | `employer123` | Employer Admin | 2 (ABC Corp) | Manage employees, payroll, attendance |
| `employee1` | `employee123` | Employee | 2 (ABC Corp) | Self-service portal access |

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login (returns JWT token)
- `POST /api/v1/auth/register` - User registration

### Employees
- `GET /api/v1/employees` - List all employees (tenant-filtered)
- `GET /api/v1/employees/me` - Get current logged-in employee's record
- `POST /api/v1/employees` - Create new employee
- `GET /api/v1/employees/{id}` - Get employee details by ID
- `PUT /api/v1/employees/{id}` - Update employee information
- `DELETE /api/v1/employees/{id}` - Soft delete employee

### Locations & Organization
- `GET /api/v1/locations` - List all locations
- `POST /api/v1/locations` - Create new location
- `GET /api/v1/tenants` - List tenants (SaaS Admin only)
- `POST /api/v1/tenants` - Create new tenant (SaaS Admin only)

### Attendance
- `GET /api/v1/attendance` - List attendance records
- `POST /api/v1/attendance` - Mark attendance manually
- `POST /api/v1/attendance/upload` - Bulk upload attendance via Excel

### Leave Management
- `GET /api/v1/leaves` - List leave requests
- `POST /api/v1/leaves` - Create leave request
- `PUT /api/v1/leaves/{id}/approve` - Approve leave request
- `PUT /api/v1/leaves/{id}/reject` - Reject leave request

### Payroll & Wages
- `POST /api/v1/payroll/calculate` - Calculate monthly payroll for all employees
- `POST /api/v1/payroll/process` - Process and finalize payroll
- `GET /api/v1/wages` - List wage statements
- `GET /api/v1/wages/{id}` - Get specific wage statement
- `GET /api/v1/wages/{id}/payslip` - Download payslip PDF

### Statutory Compliance
- `GET /api/v1/statutory/pf-ecr` - Generate PF ECR file
- `GET /api/v1/statutory/esi-challan` - Generate ESI challan
- `GET /api/v1/statutory/form-xiii` - Generate Form XIII
- `GET /api/v1/statutory/pt-form-v` - Generate PT Form V

### Reports
- `GET /api/v1/reports/attendance` - Attendance summary report
- `GET /api/v1/reports/payroll` - Payroll summary report
- `GET /api/v1/reports/salary-register` - Monthly salary register
- `GET /api/v1/reports/payment-summary` - Payment summary by bank/cash

## Architecture Highlights

### Multi-Tenant Architecture
- **Tenant isolation**: Complete data separation at database level using `tenant_id`
- **Automatic filtering**: Middleware automatically filters queries by tenant context
- **Scalable design**: Supports unlimited tenants on single database instance
- **Security**: No cross-tenant data leakage through role-based access control

### Wage Calculation Engine
- **Flexible components**: Configurable salary structure (Basic, DA, HRA, Conveyance, Special Allowance)
- **Attendance integration**: Automatic salary calculation based on present/absent days
- **Statutory compliance**: Built-in PF (12%), ESI (0.75%), and PT calculations
- **Deductions**: Support for loans, advances, and other custom deductions
- **Overtime**: Configurable overtime rates and calculations

### Real-time Features
- **WebSocket support**: Live progress updates during bulk attendance uploads
- **Instant notifications**: Real-time alerts for leave approvals, payroll processing
- **Auto-refresh dashboards**: Live employee count and statistics updates

### Security Features
- **JWT authentication**: Secure token-based authentication with configurable expiry
- **Role-based access**: Three-tier access (SaaS Admin, Employer Admin, Employee)
- **Password security**: bcrypt hashing with salt rounds
- **Audit trail**: Complete logging of all CRUD operations with timestamps
- **SQL injection protection**: Parameterized queries through SQLAlchemy ORM

## Recent Updates

### Latest Changes (November 2025)
- Added `/api/v1/employees/me` endpoint for employee self-service portal
- Fixed route ordering to prevent path parameter conflicts
- Created comprehensive test data generation scripts
- Enhanced dashboard with real-time employee statistics
- Improved multi-tenant data isolation with middleware
- Added comprehensive `.gitignore` for clean version control
- Fixed Swagger/OpenAPI documentation - upgraded FastAPI to 0.121.0 and Pydantic to 2.12.3
- Resolved schema generation issues in location.py and billing.py

### Known Issues
- PostgreSQL migration pending for production deployment

## Development Roadmap

### Upcoming Features
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard with charts
- [ ] Biometric device integration (ZKTeco, eSSL)
- [ ] Email notifications for leave approvals and payslips
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Tax (TDS) calculations and Form 16 generation
- [ ] Performance appraisal module
- [ ] Training and development tracking

## Contributing

We welcome contributions to improve Symbiosis HR Payroll System:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide (Python) and ESLint rules (JavaScript)
- All tests pass before submitting PR
- Add tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Contact

For issues, questions, or feature requests:
- Create an issue: [GitHub Issues](https://github.com/shekar369/symbiosis/issues)
- Email: support@symbiosis-hr.com
- Documentation: [Wiki](https://github.com/shekar369/symbiosis/wiki)

## Acknowledgments

Built with modern web technologies and best practices:
- FastAPI team for excellent Python web framework
- React team for powerful frontend library
- SQLAlchemy team for robust ORM
- All open-source contributors

---

**Status**: Production-ready with active development
**Version**: 1.0.0
**Last Updated**: November 2025
