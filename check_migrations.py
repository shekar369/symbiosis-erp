import sqlite3

conn = sqlite3.connect('hr_payroll.db')
cursor = conn.cursor()

print('=== Database Tables ===')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
for table in tables:
    print(f'  - {table[0]}')

print('\n=== Alembic Version ===')
try:
    cursor.execute("SELECT version_num FROM alembic_version")
    version = cursor.fetchone()
    if version:
        print(f'Current version: {version[0]}')
    else:
        print('No version found')
except:
    print('alembic_version table not found')

conn.close()
