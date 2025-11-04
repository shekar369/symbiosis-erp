# HR Payroll System - Frontend

Modern React-based frontend for the HR Payroll Management System, built with Vite and Tailwind CSS.

## Tech Stack

- React 18 + Vite
- React Router v6
- Axios for API calls
- Tailwind CSS
- Lucide React icons

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open http://localhost:5173

## Default Login

- Username: `admin`
- Password: `admin123`

## Features

- Authentication with JWT
- Dashboard with key metrics
- Employee management (CRUD operations)
- Attendance tracking with bulk upload
- Wage statements and payroll
- Responsive design with Tailwind CSS

## Environment Variables

Create a `.env` file:
```
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Project Structure

```
src/
├── api/               # API client services
├── components/        # Reusable UI components
│   ├── common/       # Button, Input, Table, Modal, Card
│   └── layout/       # Sidebar, Header, Layout
├── context/          # AuthContext for authentication
├── pages/            # Page components (Dashboard, Employees, etc.)
└── App.jsx           # Main app with routing
```
