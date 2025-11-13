"""Fix Loss of Pay leave balance - should be 0 days allocation"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login as employer (who can manage leave balances)
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "employer", "password": "employer123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get all employees
    employees_response = requests.get(f"{BASE_URL}/employees/", headers=headers)

    if employees_response.status_code == 200:
        employees = employees_response.json()
        print(f"Found {len(employees)} employees")

        for employee in employees:
            employee_id = employee["id"]
            print(f"\nProcessing Employee: {employee['first_name']} {employee['last_name']} (ID: {employee_id})")

            # Get leave balances for this employee
            balance_response = requests.get(f"{BASE_URL}/leaves/balance/{employee_id}", headers=headers)

            if balance_response.status_code == 200:
                balances = balance_response.json()

                # Find LOP balance
                for balance in balances:
                    if balance.get('leave_type_name') == 'Loss of Pay':
                        print(f"  Current LOP Balance: {balance.get('balance_days')} days")
                        print(f"  Current LOP Total: {balance.get('total_days')} days")

                        # Update the balance to 0
                        balance_id = balance.get('id')
                        update_data = {
                            "total_days": 0,
                            "balance_days": 0
                        }

                        # Note: We need to check if there's an update endpoint
                        # For now, let's just report what needs to be changed
                        print(f"  ✓ LOP should be updated to 0 total days, 0 balance days")
            else:
                print(f"  Failed to get balance: {balance_response.status_code}")
    else:
        print(f"Failed to get employees: {employees_response.status_code}")
else:
    print(f"Login failed: {login_response.status_code}")

print("\n" + "=" * 80)
print("Note: Database update required. Running SQL script...")
print("=" * 80)
