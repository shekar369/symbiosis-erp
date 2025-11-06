from app.db.session import SessionLocal
from app.models.employee import EmployeeBankDetails, Employee

db = SessionLocal()

print('=== Database Check ===')
print(f'Total Employees: {db.query(Employee).count()}')
print(f'Total Bank Details: {db.query(EmployeeBankDetails).count()}')

employee = db.query(Employee).filter(Employee.email == 'employee1@example.com').first()
if employee:
    print(f'\nEmployee1 found:')
    print(f'  ID: {employee.id}')
    print(f'  Email: {employee.email}')
    print(f'  Tenant ID: {employee.tenant_id}')

    bank = db.query(EmployeeBankDetails).filter(EmployeeBankDetails.employee_id == employee.id).first()
    if bank:
        print(f'\nBank details exist:')
        print(f'  Account Holder: {bank.account_holder_name}')
        print(f'  Account Number: {bank.account_number}')
        print(f'  Bank: {bank.bank_name}')
    else:
        print('\nNo bank details found for employee1')
else:
    print('\nEmployee1 not found!')

db.close()
