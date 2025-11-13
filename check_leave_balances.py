import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login as employee
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "employee", "password": "employee123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get employee profile
    profile_response = requests.get(f"{BASE_URL}/employees/me", headers=headers)
    employee_id = profile_response.json()["id"]

    # Get leave balance
    balance_response = requests.get(f"{BASE_URL}/leaves/balance/{employee_id}", headers=headers)

    if balance_response.status_code == 200:
        balances = balance_response.json()

        print("=" * 80)
        print("LEAVE BALANCES")
        print("=" * 80)

        total_balance = 0
        for balance in balances:
            print(f"\n{balance.get('leave_type_name', 'Unknown')}:")
            print(f"  Total Days: {balance.get('total_days', 0)}")
            print(f"  Used Days: {balance.get('used_days', 0)}")
            print(f"  Balance Days: {balance.get('balance_days', 0)}")
            total_balance += balance.get('balance_days', 0)

        print("\n" + "=" * 80)
        print(f"Total Balance Across All Leave Types: {total_balance} days")
        print(f"Number of Leave Types: {len(balances)}")
        print("=" * 80)
    else:
        print(f"Failed to fetch leave balance: {balance_response.status_code}")
        print(balance_response.text)
else:
    print(f"Login failed: {login_response.status_code}")
