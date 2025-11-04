import pandas as pd

# Read Employee Database
print("=" * 80)
print("EMPLOYEE DATABASE STRUCTURE")
print("=" * 80)
df = pd.read_excel('Doc-refs/1.Input Data/Employee Database.xlsx', header=1)
print(f"\nTotal columns: {len(df.columns)}")
print("\nColumns:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print(f"\nTotal rows: {len(df)}")
print("\nFirst 3 rows:")
print(df.head(3).to_string())

# Read Employee Master - Contract Labour
print("\n\n" + "=" * 80)
print("EMPLOYEE MASTER - CONTRACT LABOUR")
print("=" * 80)
xls = pd.ExcelFile('Doc-refs/2.Inprocess Data/1.Employee Master-AP&Telangana Contract Labour.xlsx')
print(f"\nSheet names: {xls.sheet_names}")

for sheet in xls.sheet_names[:2]:  # Read first 2 sheets
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
    print(f"Columns: {list(df.columns)}")

# Read Output Data - Payroll
print("\n\n" + "=" * 80)
print("OUTPUT DATA - PAYROLL SAMPLE")
print("=" * 80)
xls = pd.ExcelFile('Doc-refs/3.Output Data/1.BURGEON HYD  S E Z -APRIL 22.xlsx')
print(f"\nSheet names: {xls.sheet_names}")

for sheet in xls.sheet_names[:1]:  # Read first sheet
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(xls, sheet_name=sheet, nrows=3)
    print(f"Columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
