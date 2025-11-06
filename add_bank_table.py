import sqlite3
from datetime import datetime

conn = sqlite3.connect('hr_payroll.db')
cursor = conn.cursor()

print('Creating employee_bank_details table...')

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_bank_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL UNIQUE,
    account_holder_name VARCHAR NOT NULL,
    account_number VARCHAR NOT NULL,
    bank_name VARCHAR NOT NULL,
    branch_name VARCHAR,
    ifsc_code VARCHAR NOT NULL,
    account_type VARCHAR,
    pan_number VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
''')

conn.commit()
print('Table created successfully!')

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee_bank_details'")
if cursor.fetchone():
    print('Verification: employee_bank_details table exists!')
else:
    print('ERROR: Table creation failed!')

conn.close()
