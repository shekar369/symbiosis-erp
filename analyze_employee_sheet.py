import openpyxl
from openpyxl import load_workbook

# Load the Excel file
file_path = r"C:\Users\Admin\Documents\projects\Claude_exp\HR_Payroll\Doc-refs\1.Input Data\Employee Database.xlsx"
wb = load_workbook(file_path)

# Analyze Employee Database sheet
ws = wb["Employee Database"]

print("=== EMPLOYEE DATABASE SHEET ANALYSIS ===\n")
print(f"Total rows: {ws.max_row}")
print(f"Total columns: {ws.max_column}\n")

# Find header row (look for rows with multiple non-empty cells)
print("First 15 rows (showing first 30 columns with data):\n")
for row in range(1, min(16, ws.max_row + 1)):
    non_empty = []
    for col in range(1, min(31, ws.max_column + 1)):
        cell_value = ws.cell(row=row, column=col).value
        if cell_value:
            non_empty.append(f"Col{col}: {str(cell_value)[:50]}")

    if non_empty:
        print(f"Row {row}:")
        for item in non_empty[:10]:  # Show first 10 non-empty cells
            print(f"  {item}")
        if len(non_empty) > 10:
            print(f"  ... and {len(non_empty) - 10} more columns")
        print()

wb.close()
