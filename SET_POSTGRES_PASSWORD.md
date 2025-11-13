# PostgreSQL Password Setup Instructions

## New Password: hrpayroll2024

Please set the PostgreSQL 'postgres' user password using ONE of these methods:

### Method 1: Using pgAdmin (Easiest)
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Right-click on "Login/Group Roles" → "postgres"
4. Click "Properties"
5. Go to "Definition" tab
6. Set password to: `hrpayroll2024`
7. Click "Save"

### Method 2: Using psql (Command Line)
Run this in PowerShell or CMD:
```
C:\pgsql\bin\psql.exe -U postgres -d postgres
```
When connected, run:
```sql
ALTER USER postgres WITH PASSWORD 'hrpayroll2024';
\q
```

### Method 3: Edit pg_hba.conf temporarily
1. Open: `C:\pgsql\data\pg_hba.conf`
2. Find lines with `md5` or `scram-sha-256`
3. Temporarily change to `trust`:
   ```
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   host    all             all             127.0.0.1/32            trust
   host    all             all             ::1/128                 trust
   ```
4. Restart PostgreSQL:
   ```
   C:\pgsql\bin\pg_ctl.exe restart -D C:\pgsql\data
   ```
5. Connect and change password:
   ```
   C:\pgsql\bin\psql.exe -U postgres -d postgres
   ALTER USER postgres WITH PASSWORD 'hrpayroll2024';
   \q
   ```
6. Change pg_hba.conf back to `md5` or `scram-sha-256`
7. Restart PostgreSQL again

## After Setting Password
Type "done" or "password set" and I'll continue with database creation!
