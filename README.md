# FastAPI HR Payroll System

A comprehensive HR and Payroll management system built with FastAPI, supporting multi-tenant architecture.

## Features

- Multi-tenant organization management
- Employee management with complete CRUD operations
- Attendance tracking and bulk upload
- Complex wage calculation engine
- Payroll processing and payslip generation
- Leave management
- Shift management
- Holiday calendar
- Loan and advance tracking
- Comprehensive audit logging
- Role-based access control
- Real-time WebSocket updates
- RESTful API with OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **Validation**: Pydantic
- **Migrations**: Alembic
- **Testing**: Pytest
- **Containerization**: Docker & Docker Compose

## Project Structure

```
fastapi-hr-payroll/
├── app/                    # Application code
│   ├── api/               # API routes and endpoints
│   ├── core/              # Security, constants, errors
│   ├── models/            # SQLAlchemy models (30+ tables)
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── crud/              # Database operations
│   ├── middleware/        # Custom middleware
│   ├── utils/             # Utility functions
│   ├── websockets/        # WebSocket handlers
│   └── background_tasks/  # Background job processors
├── migrations/            # Alembic migrations
├── tests/                 # Test suite
└── scripts/               # Utility scripts
```

## Setup

### Local Development

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your database credentials

6. Initialize database:
   ```bash
   python scripts/init_database.py
   ```

7. Create superuser:
   ```bash
   python scripts/create_superuser.py
   ```

8. Seed sample data (optional):
   ```bash
   python scripts/seed_data.py
   ```

9. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`

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
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Employees
- `GET /api/v1/employees` - List employees
- `POST /api/v1/employees` - Create employee
- `GET /api/v1/employees/{id}` - Get employee details
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `GET /api/v1/attendance` - List attendance records
- `POST /api/v1/attendance` - Mark attendance
- `POST /api/v1/attendance/upload` - Bulk upload attendance

### Payroll
- `POST /api/v1/payroll/calculate` - Calculate monthly payroll
- `POST /api/v1/payroll/process` - Process payroll
- `GET /api/v1/wages` - List wage statements
- `GET /api/v1/wages/{id}` - Get wage statement details

### Reports
- `GET /api/v1/reports/attendance` - Attendance report
- `GET /api/v1/reports/payroll` - Payroll report

## Key Features

### Multi-Tenant Architecture
- Tenant isolation at database level
- Tenant-based data filtering
- Custom middleware for tenant context

### Wage Calculation Engine
- Configurable salary components
- Attendance-based calculations
- Statutory deductions (PF, ESI, Tax)
- Loan and advance deductions
- Overtime calculations

### Real-time Updates
- WebSocket support for attendance upload progress
- Real-time notifications

### Security
- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- Audit logging for all operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.
