"""Check CTC calculation for employees"""
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

    if profile_response.status_code == 200:
        employee = profile_response.json()

        print("=" * 80)
        print(f"EMPLOYEE: {employee.get('first_name')} {employee.get('last_name')}")
        print("=" * 80)

        if employee.get('salary_details'):
            salary = employee['salary_details']

            print("\n--- SALARY COMPONENTS ---")
            basic = float(salary.get('basic_salary', 0))
            hra = float(salary.get('hra', 0))
            conveyance = float(salary.get('conveyance_allowance', 0))
            medical = float(salary.get('medical_allowance', 0))
            special = float(salary.get('special_allowance', 0))
            other = float(salary.get('other_allowance', 0))

            print(f"Basic Salary:         Rs.{basic:,.2f}")
            print(f"HRA:                  Rs.{hra:,.2f}")
            print(f"Conveyance Allowance: Rs.{conveyance:,.2f}")
            print(f"Medical Allowance:    Rs.{medical:,.2f}")
            print(f"Special Allowance:    Rs.{special:,.2f}")
            print(f"Other Allowance:      Rs.{other:,.2f}")

            gross = float(salary.get('gross_salary', 0))
            print(f"\nGross Salary (DB):    Rs.{gross:,.2f}")

            # Calculate expected gross
            expected_gross = basic + hra + conveyance + medical + special + other
            print(f"Expected Gross:       Rs.{expected_gross:,.2f}")

            print("\n--- DEDUCTIONS ---")
            pf_emp = float(salary.get('pf_employee', 0))
            pf_employer = float(salary.get('pf_employer', 0))
            esic_emp = float(salary.get('esic_employee', 0))
            esic_employer = float(salary.get('esic_employer', 0))
            pt = float(salary.get('professional_tax', 0))
            tds = float(salary.get('tds', 0))

            print(f"PF Employee:          Rs.{pf_emp:,.2f}")
            print(f"PF Employer:          Rs.{pf_employer:,.2f}")
            print(f"ESIC Employee:        Rs.{esic_emp:,.2f}")
            print(f"ESIC Employer:        Rs.{esic_employer:,.2f}")
            print(f"Professional Tax:     Rs.{pt:,.2f}")
            print(f"TDS:                  Rs.{tds:,.2f}")

            total_deductions = float(salary.get('total_deductions', 0))
            print(f"\nTotal Deductions (DB): Rs.{total_deductions:,.2f}")

            # Calculate expected deductions (employee portion only)
            expected_emp_deductions = pf_emp + esic_emp + pt + tds
            print(f"Expected Employee Deductions: Rs.{expected_emp_deductions:,.2f}")

            net = float(salary.get('net_salary', 0))
            print(f"\nNet Salary (DB):      Rs.{net:,.2f}")
            expected_net = gross - expected_emp_deductions
            print(f"Expected Net:         Rs.{expected_net:,.2f}")

            ctc = float(salary.get('ctc', 0))
            print(f"\n--- CTC CALCULATION ---")
            print(f"CTC (DB):             Rs.{ctc:,.2f}")
            print(f"Annual CTC (DB):      Rs.{ctc * 12:,.2f}")

            # CTC should include: Gross + Employer contributions
            expected_monthly_ctc = gross + pf_employer + esic_employer
            expected_annual_ctc = expected_monthly_ctc * 12

            print(f"\nExpected Monthly CTC: Rs.{expected_monthly_ctc:,.2f}")
            print(f"  (Gross: {gross:,.2f} + PF Employer: {pf_employer:,.2f} + ESIC Employer: {esic_employer:,.2f})")
            print(f"Expected Annual CTC:  Rs.{expected_annual_ctc:,.2f}")

            print("\n--- VERIFICATION ---")
            if abs(gross - expected_gross) > 0.01:
                print(f"❌ Gross mismatch: DB={gross:,.2f}, Expected={expected_gross:,.2f}")
            else:
                print(f"✓ Gross calculation correct")

            if abs(ctc - expected_monthly_ctc) > 0.01:
                print(f"❌ CTC mismatch: DB={ctc:,.2f}, Expected={expected_monthly_ctc:,.2f}")
                print(f"   Annual: DB={ctc * 12:,.2f}, Expected={expected_annual_ctc:,.2f}")
            else:
                print(f"✓ CTC calculation correct")
        else:
            print("No salary details found")
    else:
        print(f"Failed to fetch profile: {profile_response.status_code}")
else:
    print(f"Login failed: {login_response.status_code}")
