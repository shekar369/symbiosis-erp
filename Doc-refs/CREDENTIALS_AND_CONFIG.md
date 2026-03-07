# HR Payroll System — Credentials & Configuration Reference

> **Single source of truth.** All passwords, ports, CORS settings, and where to change them.
> Last verified: 2026-03-08

---

## 1. Application Login Credentials (Current — Verified Working)

All app users use the same password set during the PostgreSQL migration.

| Username   | Password   | Role        | Access                              |
|------------|------------|-------------|-------------------------------------|
| `admin`    | `Test@1234`| Admin       | Full system administration          |
| `employer` | `Test@1234`| Employer    | HR/Payroll management               |
| `hrmanager`| `Test@1234`| HR Manager  | HR operations                       |
| `employee` | `Test@1234`| Employee    | Self-service portal                 |

**Login URL:** http://localhost:5174
**API Docs:** http://localhost:8000/docs

---

## 2. Database Credentials (PostgreSQL)

| Field    | Value           |
|----------|-----------------|
| Host     | `localhost`     |
| Port     | `5432`          |
| Database | `hr_payroll`    |
| Username | `postgres`      |
| Password | `hrpayroll2024` |

**Full connection string:**
```
postgresql://postgres:hrpayroll2024@localhost:5432/hr_payroll
```

### Where this is set:
- [`.env`](../.env) — `DATABASE_URL=` (primary, loaded at runtime)
- [`app/config.py`](../app/config.py) — line 28, hardcoded default fallback only

### To change database password:
1. Change in PostgreSQL: `ALTER USER postgres WITH PASSWORD 'newpassword';`
2. Update `.env`: `DATABASE_URL=postgresql://postgres:newpassword@localhost:5432/hr_payroll`
3. Update fallback in `app/config.py` line 28 (optional, `.env` takes priority)

---

## 3. Ports & URLs

| Service   | Port | URL                          |
|-----------|------|------------------------------|
| Frontend  | 5174 | http://localhost:5174        |
| Backend   | 8000 | http://localhost:8000        |
| Database  | 5432 | localhost:5432               |

---

## 4. CORS Configuration

### Current allowed origins (backend):
```
http://localhost:3000
http://localhost:5173
http://localhost:5174
http://localhost:8000
```

> In `ENVIRONMENT=development` mode, the backend allows **ALL origins** (`*`), so the
> list above only matters in staging/production.

### Where CORS is configured:
| File | Location | Purpose |
|------|----------|---------|
| [`app/config.py`](../app/config.py) | Line 64, `BACKEND_CORS_ORIGINS` | Default list |
| [`.env`](../.env) | `BACKEND_CORS_ORIGINS=` | Override (takes priority) |
| [`app/main.py`](../app/main.py) | Line 30 | Applies CORS middleware |

### To add a new frontend port (e.g. 3001):
Edit `.env`:
```
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001","http://localhost:5173","http://localhost:5174","http://localhost:8000"]
```
Then restart the backend.

### Important — localhost vs 127.0.0.1:
The browser treats `localhost` and `127.0.0.1` as **different origins**.
Always use `localhost` consistently across:
- [`frontend/.env`](../frontend/.env): `VITE_API_BASE_URL=http://localhost:8000/api/v1`
- [`frontend/src/api/axios.js`](../frontend/src/api/axios.js): fallback URL
- CORS origins list above

---

## 5. Frontend API URL

### Where it is set:
| File | Value | Purpose |
|------|-------|---------|
| [`frontend/.env`](../frontend/.env) | `VITE_API_BASE_URL=http://localhost:8000/api/v1` | Primary (Vite loads this) |
| [`frontend/src/api/axios.js`](../frontend/src/api/axios.js) | Line 3, fallback value | Used if `.env` not loaded |

### To change backend URL (e.g. different host/port):
1. Edit `frontend/.env`: `VITE_API_BASE_URL=http://YOUR_HOST:PORT/api/v1`
2. Edit `frontend/src/api/axios.js` line 3 fallback to match
3. **Restart Vite** — `.env` changes require a full restart, hot-reload is not enough

---

## 6. Security Key

| Setting | Location | Current value |
|---------|----------|---------------|
| `SECRET_KEY` | `.env` line 8 | `your-secret-key-change-this-...` |
| `ALGORITHM` | `.env` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `.env` | `30` |

> The current SECRET_KEY is a placeholder. It works in development but **must** be
> replaced before any production deployment.

**Generate a secure key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 7. Startup Sequence (Quick Reference)

```
Terminal 1 (Admin PowerShell):  net start postgresql-x64-15
Terminal 2 (project root):      venv\Scripts\activate  →  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Terminal 3 (frontend/):         npm run dev -- --port 5174
```

---

## 8. To Reset App User Passwords

Run from project root with venv active:
```bash
python - <<'EOF'
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()
new_password = "Test@1234"   # change this

for username in ["admin", "employer", "hrmanager", "employee"]:
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        print(f"Reset: {username}")

db.commit()
db.close()
EOF
```
