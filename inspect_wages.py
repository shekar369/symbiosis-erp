import pandas as pd
import os

file_path = r"C:\Users\Admin\Documents\projects\Claude_exp\HR_Payroll\Doc-refs\1.Input Data\Employee Database.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    print(f"Sheet names: {xls.sheet_names}")
    # Assuming 3rd sheet is Wages
    if len(xls.sheet_names) >= 3:
        sheet_name = xls.sheet_names[2]
        print(f"\n--- Sheet: {sheet_name} ---")
        df = pd.read_excel(xls, sheet_name=sheet_name, nrows=0)
        print(list(df.columns))
    else:
        print("Less than 3 sheets found.")
except Exception as e:
    print(f"Error: {e}")
