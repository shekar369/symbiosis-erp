import psycopg2

print("Step 1: Connecting to PostgreSQL with trust authentication...")

try:
    conn = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        database='postgres'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Step 2: Setting password...")
    cur.execute("ALTER USER postgres WITH PASSWORD 'hrpayroll2024';")
    print("[OK] Password set successfully!")
    
    print("\nStep 3: Dropping database hr_payroll if exists...")
    cur.execute('DROP DATABASE IF EXISTS hr_payroll')
    print("[OK] Dropped")
    
    print("\nStep 4: Creating database hr_payroll...")
    cur.execute('CREATE DATABASE hr_payroll')
    print("[OK] Database created!")
    
    cur.close()
    conn.close()
    
    print("\n=== COMPLETE ===")
    print("Password: hrpayroll2024")
    print("Database: hr_payroll")
    
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)
