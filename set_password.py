import psycopg2

print("Connecting to PostgreSQL with trust authentication...")

try:
    # Connect without password (trust auth)
    conn = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        database='postgres'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Set the password
    print("Setting password to: hrpayroll2024")
    cur.execute("ALTER USER postgres WITH PASSWORD 'hrpayroll2024';")
    print("✓ Password set successfully!")
    
    # Drop and create database
    print("\nDropping database hr_payroll if exists...")
    cur.execute('DROP DATABASE IF EXISTS hr_payroll')
    print("✓ Dropped (if existed)")
    
    print("Creating database hr_payroll...")
    cur.execute('CREATE DATABASE hr_payroll')
    print("✓ Database hr_payroll created successfully!")
    
    cur.close()
    conn.close()
    
    print("\n=== SUCCESS ===")
    print("Password: hrpayroll2024")
    print("Database: hr_payroll created")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
