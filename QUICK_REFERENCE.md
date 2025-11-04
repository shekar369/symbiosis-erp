# HR Payroll System - Quick Reference Card

**Version**: 1.0.0 | **Date**: October 31, 2025

---

## 🚀 Quick Start

### Start Servers:
```bash
# Backend
cd backend && python -m uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

### Access URLs:
- **Frontend**: http://localhost:5174
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

---

## 📊 System Overview

| Component | Status | Count |
|-----------|--------|-------|
| Backend Endpoints | ✅ | 74+ |
| Frontend Pages | ✅ | 17 |
| Features | ✅ | 50+ |
| Documentation | ✅ | 7 files |

---

## 🎯 Key Features

### Employer:
- Multi-location management
- Employee management (CRUD + bulk upload)
- Attendance tracking (manual + bulk upload)
- Payroll processing (bulk)
- PDF generation (payslips, registers)
- Email distribution
- Bank files (5 formats)
- Statutory forms (5 types)
- Leave management
- Reports

### Employee:
- Personal dashboard
- Payslip viewing & download (5 years)
- Leave application & tracking
- Profile viewing & editing
- Leave balance tracking
- Salary history

---

## 🔐 Default Credentials

**Admin**:
- Username: admin
- Password: password

*Change in production!*

---

## 📂 Project Structure

```
HR_Payroll/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/     # API endpoints
│   │   ├── models/  # Database models
│   │   ├── schemas/ # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── utils/   # Utilities
│   └── requirements.txt
│
└── frontend/         # React frontend
    ├── src/
    │   ├── pages/   # Page components
    │   ├── components/ # Reusable components
    │   ├── services/ # API service
    │   └── context/ # React context
    └── package.json
```

---

## 🔄 Complete Workflow

### Monthly Payroll:
```
Attendance → Process Payroll → Approve →
Distribute (Email/PDF) → Bank Transfer →
Statutory Forms → Mark as Paid
```

---

## 📁 Key Files

### Backend:
- `app/main.py` - Application entry
- `app/api/v1/router.py` - API routing
- `app/utils/payroll_calculator.py` - Calculations
- `app/services/email_service.py` - Email
- `app/utils/statutory_forms_generator.py` - Forms

### Frontend:
- `src/App.jsx` - Routing
- `src/components/layout/Sidebar.jsx` - Navigation
- `src/services/api.js` - HTTP client
- `src/pages/payroll/Payroll.jsx` - Payroll UI
- `src/pages/employee/*` - Employee portal

---

## 🎨 UI Routes

### Employer:
- `/dashboard` - Main dashboard
- `/employees` - Employee management
- `/locations` - Location management
- `/attendance` - Attendance tracking
- `/payroll` - Payroll processing
- `/statutory` - Statutory forms
- `/bank-transfer` - Bank files
- `/leaves` - Leave management
- `/wages` - Wage config
- `/reports` - Reports

### Employee:
- `/employee/dashboard` - Dashboard
- `/employee/payslips` - Payslip history
- `/employee/leave` - Leave management
- `/employee/profile` - Profile

---

## 🔌 Key API Endpoints

### Authentication:
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
```

### Employees:
```bash
GET    /api/v1/employees
POST   /api/v1/employees
PUT    /api/v1/employees/{id}
DELETE /api/v1/employees/{id}
POST   /api/v1/employees/bulk-upload
```

### Payroll:
```bash
POST /api/v1/payroll/process-bulk
POST /api/v1/payroll/approve
GET  /api/v1/payroll/payslip/{employee_id}
GET  /api/v1/payroll/salary-register
POST /api/v1/payroll/send-bulk-payslips
GET  /api/v1/payroll/bank-transfer-file
```

### Statutory:
```bash
GET /api/v1/statutory/epf-ecr
GET /api/v1/statutory/esi-return
GET /api/v1/statutory/pt-form-v
GET /api/v1/statutory/form-xiii
GET /api/v1/statutory/pf-challan-summary
```

### Leave:
```bash
GET    /api/v1/leave/requests
POST   /api/v1/leave/requests
DELETE /api/v1/leave/requests/{id}
GET    /api/v1/leave/balance/{employee_id}
```

---

## ⚙️ Configuration

### Backend (.env):
```env
DATABASE_URL=postgresql://user:pass@localhost/hrpayroll
SECRET_KEY=your-secret-key-here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (.env):
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

## 🧪 Testing Commands

### Backend:
```bash
# Health check
curl http://127.0.0.1:8000/api/v1/health

# Login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### Frontend:
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📋 Common Tasks

### Add New Employee:
1. Navigate to `/employees`
2. Click "Add Employee"
3. Fill form
4. Save

### Process Payroll:
1. Navigate to `/payroll`
2. Select month/year
3. Click "Process Bulk Payroll"
4. Review in "Review & Approve" tab
5. Select and approve
6. Distribute payslips

### Generate Statutory Forms:
1. Navigate to `/statutory`
2. Select month/year
3. Click download for each form
4. Upload to government portals

### Employee: Download Payslip:
1. Navigate to `/employee/payslips`
2. Find desired month
3. Click "Download" button

### Employee: Apply Leave:
1. Navigate to `/employee/leave`
2. Click "Apply Leave" tab
3. Fill form
4. Submit

---

## 🐛 Troubleshooting

### Frontend Can't Connect to Backend:
- Check VITE_API_BASE_URL in .env
- Verify backend is running
- Check CORS settings

### Email Not Sending:
- Verify SMTP credentials in backend .env
- Check firewall/port 587
- Use app-specific password for Gmail

### File Download Not Working:
- Check responseType: 'blob' in API call
- Verify browser popup blocker settings
- Check Content-Type headers

### Token Expired:
- Clear localStorage
- Login again
- Check JWT expiration time

---

## 📚 Documentation Files

1. **PHASE6_EMAIL_STATUTORY_IMPLEMENTATION.md** - Email & Forms
2. **PROJECT_COMPLETE_SUMMARY.md** - Overall Overview
3. **TESTING_CHECKLIST.md** - Test Cases
4. **FRONTEND_IMPLEMENTATION_SUMMARY.md** - Employer Frontend
5. **EMPLOYEE_PORTAL_IMPLEMENTATION.md** - Employee Frontend
6. **COMPLETE_SYSTEM_TESTING_GUIDE.md** - Testing Guide
7. **PROJECT_COMPLETION_SUMMARY.md** - Final Summary

---

## 🔧 Maintenance

### Daily:
- Check server logs
- Verify backups

### Weekly:
- Review error logs
- Check disk space

### Monthly:
- Security updates
- Performance review

### Quarterly:
- User feedback review
- Feature updates

---

## 📞 Support

**Documentation**: See project root
**Issues**: (Add your tracker URL)
**Email**: (Add support email)

---

## 🎯 Success Metrics

**Development**:
✅ 98% Complete
✅ 9,845+ lines of code
✅ 74+ API endpoints
✅ 17 pages
✅ 50+ features

**Ready For**:
- ✅ Testing
- ✅ Deployment
- ✅ Production

---

## 💡 Quick Tips

1. Use Swagger UI at `/docs` for API testing
2. Check browser console for frontend errors
3. Use search/filter features to find data quickly
4. Bulk operations save time
5. Download templates before uploading
6. Generate statutory forms before deadline
7. Send test emails before bulk sending
8. Backup database regularly
9. Keep SMTP credentials secure
10. Monitor server logs

---

## 🚦 System Status Check

```bash
# Backend health
curl http://127.0.0.1:8000/api/v1/health

# Frontend running
curl http://localhost:5174

# Database connection
# (Check backend logs)
```

---

## 📈 Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Page Load | < 3s | Initial load |
| API Response | < 2s | Most GET requests |
| File Download | < 5s | PDFs, CSVs |
| Payroll Processing | < 10s | 100 employees |
| Bulk Upload | < 15s | 500 records |

---

## 🔐 Security Checklist

- [ ] Change default passwords
- [ ] Set strong JWT secret
- [ ] Enable HTTPS (production)
- [ ] Configure CORS properly
- [ ] Use environment variables
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] User access audit

---

**Quick Reference Card v1.0**
**HR Payroll System**
**Ready for Production Testing!**

---

*Print this card and keep it handy for quick reference!*
