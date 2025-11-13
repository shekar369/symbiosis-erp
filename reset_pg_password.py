import subprocess
import sys

# New simple password without special characters
new_password = "hrpayroll2024"

print("Resetting PostgreSQL postgres user password...")
print(f"New password will be: {new_password}")

# Create a temporary SQL file
sql_command = f"ALTER USER postgres WITH PASSWORD '{new_password}';"

try:
    # Try using psql with trust authentication or peer authentication
    # Method 1: Try with pg_ctl to temporarily allow trust authentication
    print("\nAttempting to reset password using ALTER USER command...")
    
    # Write SQL to file
    with open('reset_password.sql', 'w') as f:
        f.write(sql_command)
    
    # Try to execute with psql (assuming trust auth is configured)
    result = subprocess.run(
        ['C:/pgsql/bin/psql.exe', '-U', 'postgres', '-d', 'postgres', '-f', 'reset_password.sql'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print("SUCCESS! Password has been reset.")
        print(f"New password: {new_password}")
    else:
        print(f"Error: {result.stderr}")
        print("\nAlternative: Please manually reset the password using pgAdmin or run this SQL:")
        print(f"  ALTER USER postgres WITH PASSWORD '{new_password}';")
        
except subprocess.TimeoutExpired:
    print("\nCommand timed out (waiting for password).")
    print("\nPlease manually reset the password using one of these methods:")
    print("\n1. Using pgAdmin: Right-click on postgres user > Properties > Definition > Set password")
    print(f"\n2. Or edit pg_hba.conf temporarily to allow 'trust' authentication")
    print(f"\nUse this password: {new_password}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"\nPlease manually set the postgres user password to: {new_password}")

print(f"\n=== New password to use: {new_password} ===")
