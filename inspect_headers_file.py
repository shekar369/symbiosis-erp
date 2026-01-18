import pandas as pd
import os

file_path = r"C:\Users\Admin\Documents\projects\Claude_exp\HR_Payroll\Doc-refs\1.Input Data\Employee Database.xlsx"
output_file = "headers.txt"

try:
    xls = pd.ExcelFile(file_path)
    with open(output_file, "w") as f:
        f.write(f"Sheet names: {xls.sheet_names}\n")
        for sheet in xls.sheet_names:
            f.write(f"\n--- Sheet: {sheet} ---\n")
            df = pd.read_excel(xls, sheet_name=sheet, nrows=0)
            f.write(str(list(df.columns)) + "\n")
    print("Headers written to headers.txt")
except Exception as e:
    print(f"Error: {e}")
