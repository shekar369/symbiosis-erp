import psycopg2
from urllib.parse import quote_plus

password = "$hr@payroll"

try:
    # Connect to PostgreSQL server using 127.0.0.1 instead of localhost
    conn = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        password=password,
        database='postgres'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Drop database if exists
    cur.execute('DROP DATABASE IF EXISTS hr_payroll')
    print('Dropped existing hr_payroll database (if it existed)')
    
    # Create database
    cur.execute('CREATE DATABASE hr_payroll')
    print('Database hr_payroll created successfully!')
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
