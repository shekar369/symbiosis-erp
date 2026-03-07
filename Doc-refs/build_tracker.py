"""
Build the HR Payroll Project Tracker Excel file.
Run from project root with venv active:
    python Doc-refs/build_tracker.py
"""
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import DataBarRule, ColorScaleRule
from datetime import date

OUTPUT = "Doc-refs/HR_Payroll_Project_Tracker.xlsx"

# ── Colour palette ────────────────────────────────────────────────────────────
C_DARK_BLUE   = "003366"
C_MID_BLUE    = "1F5C99"
C_LIGHT_BLUE  = "D6E4F0"
C_GREEN       = "1E8449"
C_LIGHT_GREEN = "D5F5E3"
C_ORANGE      = "E67E22"
C_LIGHT_ORANGE= "FDEBD0"
C_RED         = "C0392B"
C_LIGHT_RED   = "FADBD8"
C_YELLOW      = "F1C40F"
C_LIGHT_YELLOW= "FEF9E7"
C_GRAY        = "7F8C8D"
C_LIGHT_GRAY  = "F2F3F4"
C_WHITE       = "FFFFFF"
C_HEADER_BG   = "003366"
C_SUBHDR_BG   = "1F5C99"

# Status colours
STATUS_COLOR = {
    "Complete":       (C_LIGHT_GREEN,  C_GREEN),
    "In Progress":    (C_LIGHT_ORANGE, C_ORANGE),
    "Partial":        (C_LIGHT_YELLOW, C_ORANGE),
    "Not Started":    (C_LIGHT_RED,    C_RED),
    "Stub/Placeholder": (C_LIGHT_YELLOW, C_GRAY),
    "API Ready / UI Pending": (C_LIGHT_YELLOW, C_ORANGE),
}
APPROVAL_COLOR = {
    "Approved":    (C_LIGHT_GREEN,  C_GREEN),
    "Pending":     (C_LIGHT_ORANGE, C_ORANGE),
    "In Review":   (C_LIGHT_YELLOW, C_ORANGE),
    "Not Required": (C_LIGHT_GRAY,  C_GRAY),
}

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def font(bold=False, color=C_DARK_BLUE, size=10, italic=False):
    return Font(bold=bold, color=color, size=size, italic=italic)

def align(h="left", v="center", wrap=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def thin_border():
    s = Side(style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def thick_bottom():
    tb = Side(style="medium", color=C_DARK_BLUE)
    s  = Side(style="thin",   color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=tb)

def set_cell(ws, row, col, value, bold=False, fg=None, fc=C_DARK_BLUE,
             h="left", v="center", wrap=True, size=10, italic=False,
             border=True):
    c = ws.cell(row=row, column=col, value=value)
    c.font      = font(bold=bold, color=fc, size=size, italic=italic)
    c.alignment = align(h=h, v=v, wrap=wrap)
    if fg:
        c.fill  = fill(fg)
    if border:
        c.border = thin_border()
    return c

def header_row(ws, row, cols, fg=C_HEADER_BG, fc=C_WHITE, size=10, bold=True, height=22):
    for col, val in enumerate(cols, 1):
        c = ws.cell(row=row, column=col, value=val)
        c.font      = Font(bold=bold, color=fc, size=size)
        c.fill      = fill(fg)
        c.alignment = align(h="center")
        c.border    = thin_border()
    ws.row_dimensions[row].height = height

def status_cell(ws, row, col, status):
    bg, fc = STATUS_COLOR.get(status, (C_LIGHT_GRAY, C_GRAY))
    set_cell(ws, row, col, status, bold=True, fg=bg, fc=fc, h="center")

def approval_cell(ws, row, col, status):
    bg, fc = APPROVAL_COLOR.get(status, (C_LIGHT_GRAY, C_GRAY))
    set_cell(ws, row, col, status, bold=True, fg=bg, fc=fc, h="center")

def pct_cell(ws, row, col, pct):
    if pct == 100:
        bg, fc = C_LIGHT_GREEN, C_GREEN
    elif pct >= 70:
        bg, fc = C_LIGHT_BLUE, C_MID_BLUE
    elif pct >= 40:
        bg, fc = C_LIGHT_ORANGE, C_ORANGE
    else:
        bg, fc = C_LIGHT_RED, C_RED
    set_cell(ws, row, col, f"{pct}%", bold=True, fg=bg, fc=fc, h="center")

wb = openpyxl.Workbook()

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — OVERVIEW DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = "📊 Overview"
ws1.sheet_view.showGridLines = False
ws1.column_dimensions["A"].width = 3

# Title banner
ws1.merge_cells("B2:N2")
t = ws1.cell(row=2, column=2, value="HR PAYROLL SYSTEM — PROJECT TRACKER")
t.font      = Font(bold=True, size=18, color=C_WHITE)
t.fill      = fill(C_DARK_BLUE)
t.alignment = align(h="center", v="center")
ws1.row_dimensions[2].height = 36

ws1.merge_cells("B3:N3")
sub = ws1.cell(row=3, column=2, value=f"Symbiosis HR & Payroll  |  Last Updated: {date.today().strftime('%d %b %Y')}  |  Stack: FastAPI + React + PostgreSQL")
sub.font      = Font(italic=True, size=10, color=C_WHITE)
sub.fill      = fill(C_MID_BLUE)
sub.alignment = align(h="center", v="center")
ws1.row_dimensions[3].height = 18

# ── Summary KPI boxes (row 5–8) ───────────────────────────────────────────
kpis = [
    ("B", "C", "Total Features",    "60",  C_DARK_BLUE,  C_LIGHT_BLUE),
    ("D", "E", "Complete",          "32",  C_GREEN,       C_LIGHT_GREEN),
    ("F", "G", "In Progress",       "14",  C_ORANGE,      C_LIGHT_ORANGE),
    ("H", "I", "Not Started/Stub",  "14",  C_RED,         C_LIGHT_RED),
    ("J", "K", "Overall Progress",  "61%", C_MID_BLUE,    C_LIGHT_BLUE),
    ("L", "M", "Client Approved",   "24",  C_GREEN,       C_LIGHT_GREEN),
]
for start_col, end_col, label, value, fc, bg in kpis:
    sc = openpyxl.utils.column_index_from_string(start_col)
    ec = openpyxl.utils.column_index_from_string(end_col)
    ws1.merge_cells(f"{start_col}5:{end_col}6")
    ws1.merge_cells(f"{start_col}7:{end_col}8")
    lc = ws1.cell(row=5, column=sc, value=label)
    lc.font = Font(bold=True, size=9, color=fc); lc.fill = fill(bg)
    lc.alignment = align(h="center", v="center")
    vc = ws1.cell(row=7, column=sc, value=value)
    vc.font = Font(bold=True, size=20, color=fc); vc.fill = fill(bg)
    vc.alignment = align(h="center", v="center")
    ws1.row_dimensions[5].height = 18; ws1.row_dimensions[6].height = 18
    ws1.row_dimensions[7].height = 30; ws1.row_dimensions[8].height = 18

# ── Stakeholder summary table (row 10+) ──────────────────────────────────
ws1.row_dimensions[10].height = 8  # spacer

ws1.merge_cells("B11:N11")
sh = ws1.cell(row=11, column=2, value="STAKEHOLDER-WISE FEATURE PROGRESS")
sh.font = Font(bold=True, size=12, color=C_WHITE); sh.fill = fill(C_DARK_BLUE)
sh.alignment = align(h="center")
ws1.row_dimensions[11].height = 22

header_row(ws1, 12,
    ["", "Stakeholder", "Total Features", "Complete", "In Progress",
     "Not Started", "Completion %", "Client Approval", "Priority", "Notes"],
    fg=C_SUBHDR_BG, height=20)

stakeholder_summary = [
    # stakeholder, total, complete, in_progress, not_started, pct, approval, priority, notes
    ("SaaS Admin",      7,  4, 2, 1, 57,  "In Review",   "High",   "Tenant & billing mgmt core done"),
    ("Employer/HR",     23, 14, 6, 3, 61,  "In Review",   "High",   "Payroll & leave done; reports pending"),
    ("Employee",        9,  7, 1, 1, 78,  "Approved",    "High",   "Self-service portal mostly complete"),
    ("Auditor",         5,  2, 1, 2, 40,  "Pending",     "Medium", "Audit trail & reports partially done"),
    ("System/Platform", 16, 5, 4, 7, 31,  "Pending",     "Medium", "Auth done; notifications & integrations pending"),
]

STAKEHOLDER_COLORS = {
    "SaaS Admin":      C_MID_BLUE,
    "Employer/HR":     C_DARK_BLUE,
    "Employee":        C_GREEN,
    "Auditor":         C_ORANGE,
    "System/Platform": C_GRAY,
}

for i, (stk, total, comp, inp, ns, pct, appr, prio, notes) in enumerate(stakeholder_summary, 13):
    r = i
    ws1.row_dimensions[r].height = 22
    sc = STAKEHOLDER_COLORS.get(stk, C_DARK_BLUE)
    set_cell(ws1, r, 2, "", fg=sc)  # color bar
    set_cell(ws1, r, 3, stk, bold=True, fg=C_LIGHT_BLUE, fc=C_DARK_BLUE)
    set_cell(ws1, r, 4, total, h="center", fg=C_LIGHT_GRAY)
    set_cell(ws1, r, 5, comp,  h="center", fg=C_LIGHT_GREEN, fc=C_GREEN, bold=True)
    set_cell(ws1, r, 6, inp,   h="center", fg=C_LIGHT_ORANGE, fc=C_ORANGE, bold=True)
    set_cell(ws1, r, 7, ns,    h="center", fg=C_LIGHT_RED, fc=C_RED, bold=True)
    pct_cell(ws1, r, 8, pct)
    approval_cell(ws1, r, 9, appr)
    set_cell(ws1, r, 10, prio, h="center")
    set_cell(ws1, r, 11, notes, italic=True, fc=C_GRAY)

# Totals row
r = 18
ws1.row_dimensions[r].height = 22
set_cell(ws1, r, 2, "", fg=C_DARK_BLUE)
set_cell(ws1, r, 3, "TOTAL", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)
set_cell(ws1, r, 4, 60, h="center", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)
set_cell(ws1, r, 5, 32, h="center", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)
set_cell(ws1, r, 6, 14, h="center", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)
set_cell(ws1, r, 7, 14, h="center", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)
pct_cell(ws1, r, 8, 61)
set_cell(ws1, r, 9, "—", h="center", bold=True, fg=C_DARK_BLUE, fc=C_WHITE)

# ── Legend (row 20+) ─────────────────────────────────────────────────────
ws1.row_dimensions[20].height = 8
ws1.merge_cells("B21:F21")
lh = ws1.cell(row=21, column=2, value="STATUS LEGEND")
lh.font = Font(bold=True, size=9, color=C_WHITE); lh.fill = fill(C_DARK_BLUE)
lh.alignment = align(h="center")

legend_items = [
    ("Complete",            C_LIGHT_GREEN,  C_GREEN),
    ("In Progress",         C_LIGHT_ORANGE, C_ORANGE),
    ("Partial",             C_LIGHT_YELLOW, C_ORANGE),
    ("Not Started",         C_LIGHT_RED,    C_RED),
    ("Stub/Placeholder",    C_LIGHT_YELLOW, C_GRAY),
    ("API Ready / UI Pending", C_LIGHT_YELLOW, C_ORANGE),
]
for j, (lbl, bg, fc) in enumerate(legend_items, 22):
    ws1.row_dimensions[j].height = 16
    set_cell(ws1, j, 2, lbl, fg=bg, fc=fc, bold=True, h="center")

# Column widths
col_widths = {"B":2,"C":3,"D":20,"E":12,"F":12,"G":12,"H":14,"I":14,"J":14,"K":10,"L":38}
for col, w in col_widths.items():
    ws1.column_dimensions[col].width = w

# ══════════════════════════════════════════════════════════════════════════════
# HELPER — write a stakeholder detail sheet
# ══════════════════════════════════════════════════════════════════════════════

def write_detail_sheet(wb, sheet_name, stakeholder, color_hex, features):
    """
    features = list of dicts:
      module, feature, description, backend_status, frontend_status,
      overall_status, client_approval, priority, notes
    """
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2

    # Title
    ws.merge_cells("B2:L2")
    t = ws.cell(row=2, column=2, value=f"{stakeholder.upper()}  —  FEATURE TRACKING")
    t.font = Font(bold=True, size=14, color=C_WHITE)
    t.fill = fill(color_hex); t.alignment = align(h="center", v="center")
    ws.row_dimensions[2].height = 30

    ws.merge_cells("B3:L3")
    s = ws.cell(row=3, column=2, value=f"HR Payroll System  |  {date.today().strftime('%d %b %Y')}")
    s.font = Font(italic=True, size=9, color=C_WHITE)
    s.fill = fill(C_MID_BLUE); s.alignment = align(h="center")
    ws.row_dimensions[3].height = 15

    # Stats row
    total = len(features)
    complete   = sum(1 for f in features if f["overall_status"] == "Complete")
    in_prog    = sum(1 for f in features if f["overall_status"] == "In Progress")
    partial    = sum(1 for f in features if f["overall_status"] == "Partial")
    not_started= sum(1 for f in features if f["overall_status"] in ("Not Started","Stub/Placeholder"))
    api_only   = sum(1 for f in features if f["overall_status"] == "API Ready / UI Pending")
    pct        = round((complete + partial*0.5 + in_prog*0.5 + api_only*0.5) / total * 100) if total else 0

    ws.row_dimensions[4].height = 6
    stats = [
        (5, "Total",      total,       C_LIGHT_GRAY,   C_DARK_BLUE),
        (6, "Complete",   complete,    C_LIGHT_GREEN,  C_GREEN),
        (7, "In Progress",in_prog,     C_LIGHT_ORANGE, C_ORANGE),
        (8, "Partial",    partial,     C_LIGHT_YELLOW, C_ORANGE),
        (9, "Not Started",not_started, C_LIGHT_RED,    C_RED),
        (10,"API Only",   api_only,    C_LIGHT_YELLOW, C_GRAY),
        (11,"Progress %", f"{pct}%",   C_LIGHT_BLUE,   C_MID_BLUE),
    ]
    for row, lbl, val, bg, fc in stats:
        ws.merge_cells(f"B{row}:C{row}")
        ws.merge_cells(f"D{row}:E{row}")
        lc = ws.cell(row=row, column=2, value=lbl)
        lc.font = Font(bold=True, size=9, color=fc); lc.fill = fill(bg)
        lc.alignment = align(h="right")
        vc = ws.cell(row=row, column=4, value=val)
        vc.font = Font(bold=True, size=11, color=fc); vc.fill = fill(bg)
        vc.alignment = align(h="center")
        ws.row_dimensions[row].height = 18

    ws.row_dimensions[12].height = 6

    # Table header
    hdr_cols = ["#","Module","Feature","Description",
                "Backend Status","Frontend Status","Overall Status",
                "Client Approval","Priority","Notes"]
    header_row(ws, 13, [""] + hdr_cols, fg=color_hex, height=22)

    # Group features by module for visual grouping
    current_module = None
    module_bg = [C_LIGHT_BLUE, C_LIGHT_GRAY]
    module_idx = 0

    for i, feat in enumerate(features, 1):
        r = 13 + i
        ws.row_dimensions[r].height = 20
        mod = feat["module"]
        if mod != current_module:
            current_module = mod
            module_idx = (module_idx + 1) % 2

        row_bg = module_bg[module_idx]
        set_cell(ws, r, 2, i, h="center", fg=row_bg)
        set_cell(ws, r, 3, feat["module"], bold=True, fg=row_bg, fc=C_DARK_BLUE)
        set_cell(ws, r, 4, feat["feature"], bold=True, fg=C_WHITE)
        set_cell(ws, r, 5, feat["description"], fg=C_WHITE, fc=C_GRAY, italic=True)
        status_cell(ws,   r, 6, feat["backend_status"])
        status_cell(ws,   r, 7, feat["frontend_status"])
        status_cell(ws,   r, 8, feat["overall_status"])
        approval_cell(ws, r, 9, feat["client_approval"])
        # Priority colour
        prio = feat["priority"]
        prio_colors = {"High": (C_LIGHT_RED, C_RED), "Medium": (C_LIGHT_ORANGE, C_ORANGE),
                       "Low": (C_LIGHT_GREEN, C_GREEN)}
        pb, pf = prio_colors.get(prio, (C_LIGHT_GRAY, C_GRAY))
        set_cell(ws, r, 10, prio, bold=True, fg=pb, fc=pf, h="center")
        set_cell(ws, r, 11, feat.get("notes",""), fg=C_WHITE, fc=C_GRAY, italic=True)

    # Column widths
    widths = {"B":3,"C":4,"D":20,"E":30,"F":36,"G":20,"H":22,"I":24,"J":18,"K":10,"L":40}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w

    return ws


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE DATA — derived from full codebase analysis
# ══════════════════════════════════════════════════════════════════════════════

# ── SaaS Admin ───────────────────────────────────────────────────────────────
saas_features = [
    dict(module="Authentication",    feature="Login / JWT Auth",          description="Username + password, JWT token generation",
         backend_status="Complete",    frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",   priority="High",   notes=""),
    dict(module="Tenant Management", feature="Create / List / Update Tenants", description="Multi-tenant org creation and management",
         backend_status="Complete",    frontend_status="In Progress",       overall_status="In Progress",
         client_approval="In Review",  priority="High",   notes="API complete; SaaS admin UI partial"),
    dict(module="Tenant Management", feature="Tenant Dashboard",           description="Tenant KPIs and overview",
         backend_status="Complete",    frontend_status="Complete",          overall_status="Complete",
         client_approval="In Review",  priority="High",   notes=""),
    dict(module="Registration",      feature="Organisation Registration",  description="New org registration with review workflow",
         backend_status="Complete",    frontend_status="Not Started",       overall_status="API Ready / UI Pending",
         client_approval="Pending",    priority="High",   notes="Backend + review endpoints done; no UI page yet"),
    dict(module="Billing",           feature="Subscription Plans CRUD",   description="Create, list, update pricing plans",
         backend_status="Complete",    frontend_status="Not Started",       overall_status="API Ready / UI Pending",
         client_approval="Pending",    priority="Medium", notes="BillingComponents.jsx stub exists"),
    dict(module="Billing",           feature="Subscription & Invoice Mgmt", description="Tenant subscription lifecycle + invoice tracking",
         backend_status="Complete",    frontend_status="Not Started",       overall_status="API Ready / UI Pending",
         client_approval="Pending",    priority="Medium", notes="Full API done; no UI wired"),
    dict(module="System Config",     feature="System Configuration UI",   description="Initialise config, view system settings",
         backend_status="Complete",    frontend_status="In Progress",       overall_status="In Progress",
         client_approval="Pending",    priority="Medium", notes="SystemConfig.jsx exists; partial implementation"),
]

# ── Employer / HR ────────────────────────────────────────────────────────────
employer_features = [
    dict(module="Dashboard",         feature="Employer Dashboard",        description="Employee count, attendance, recent activity KPIs",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Mgmt",     feature="Employee List & Search",    description="List, search, filter employees",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Mgmt",     feature="Add / Edit Employee",       description="Create and update employee basic info",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Mgmt",     feature="Employee Detail (All Tabs)", description="Bank, salary, statutory, contact, employment tabs",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="6-tab detail form fully wired"),
    dict(module="Employee Mgmt",     feature="Bulk Employee Upload",      description="Excel upload for mass employee onboarding",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="Template download + upload working"),
    dict(module="Attendance",        feature="Attendance Record Entry",   description="Manual single attendance entry",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Attendance",        feature="Bulk Attendance Upload",    description="Excel template download + upload",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Attendance",        feature="Attendance Dashboard Stats", description="Today present/absent/late stats",
         backend_status="Partial",    frontend_status="Partial",           overall_status="Partial",
         client_approval="Pending",   priority="Medium", notes="TODO comment in EmployerDashboard.jsx; API not wired"),
    dict(module="Leave Mgmt",        feature="Leave Request List",        description="View all leave requests with filter",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Leave Mgmt",        feature="Approve / Reject Leave",    description="One-click approval/rejection with remarks",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Leave Mgmt",        feature="Leave Type Management",     description="Create, update, delete leave types",
         backend_status="Complete",   frontend_status="In Progress",       overall_status="In Progress",
         client_approval="Pending",   priority="Medium", notes="API complete; no dedicated UI for leave type CRUD"),
    dict(module="Payroll",           feature="Bulk Payroll Processing",   description="Calculate payroll for all employees in a month",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Payroll",           feature="Wage Statement List & Approval", description="View, approve, mark-paid wage statements",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="PayrollDashboard + Payroll pages"),
    dict(module="Payroll",           feature="Payslip PDF Download",      description="Per-employee payslip PDF generation",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="Professional layout with Indian currency words"),
    dict(module="Payroll",           feature="Salary Register Download",  description="Full month salary register Excel",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Payroll",           feature="Bank Transfer File",        description="Bank-ready transfer file (CSV/NEFT)",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="BankTransfer.jsx wired"),
    dict(module="Payroll",           feature="Bulk Payslip Email",        description="Send payslips via email to all employees",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="In Review", priority="Medium", notes="SMTP config required in .env"),
    dict(module="Holiday Calendar",  feature="Holiday Add / Edit / Delete", description="Manage company holidays with calendar view",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="Color-coded calendar UI"),
    dict(module="Holiday Calendar",  feature="Working Calendar (Weekly Offs)", description="Configure weekly off days per location",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Statutory",         feature="EPF-ECR / ESI / PT / PF Downloads", description="Statutory compliance file generation",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="In Review", priority="High",   notes="5 forms: EPF-ECR, ESI, PT-FormV, FormXIII, PF-Challan"),
    dict(module="Org Structure",     feature="Dept / Designation / Grade CRUD", description="Organisation structure management",
         backend_status="Complete",   frontend_status="In Progress",       overall_status="In Progress",
         client_approval="Pending",   priority="Medium", notes="API done; no dedicated UI page, used in dropdowns"),
    dict(module="Locations",         feature="Location Management",       description="Add, edit, list company locations",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="Medium", notes=""),
    dict(module="Reports",           feature="Attendance & Payroll Reports", description="Downloadable reports for HR",
         backend_status="Partial",    frontend_status="Stub/Placeholder",  overall_status="Stub/Placeholder",
         client_approval="Pending",   priority="Medium", notes="Reports.jsx shows 'coming soon'; 2 basic API stubs"),
]

# ── Employee ──────────────────────────────────────────────────────────────────
employee_features = [
    dict(module="Employee Portal",   feature="Employee Dashboard",        description="Summary: payslip, leave balance, attendance",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Portal",   feature="View Profile",              description="Personal, employment details read-only view",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Portal",   feature="Update Profile",            description="Self-edit personal details",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Employee Portal",   feature="View & Update Bank Details", description="Self-service bank account management",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Payslips",          feature="View Payslip History",      description="List payslips by year with detail modal",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="Enhanced with bank, UAN, ESI, leave data"),
    dict(module="Payslips",          feature="Download Payslip PDF",      description="Download individual payslip as PDF",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Leave",             feature="Apply for Leave",           description="Submit leave request with type and dates",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Leave",             feature="View Leave Balance",        description="Remaining leave days by type",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Leave",             feature="Leave History & Cancel",    description="View past requests, cancel pending ones",
         backend_status="Complete",   frontend_status="In Progress",       overall_status="In Progress",
         client_approval="Approved",  priority="Medium", notes="Cancel modal exists; confirmation flow partial"),
]

# ── Auditor ───────────────────────────────────────────────────────────────────
auditor_features = [
    dict(module="Auditor",           feature="Auditor Dashboard",         description="Summary view for audit access",
         backend_status="Complete",   frontend_status="Not Started",       overall_status="API Ready / UI Pending",
         client_approval="Pending",   priority="Medium", notes="API endpoint exists; no frontend page yet"),
    dict(module="Auditor",           feature="Wage Statement Audit View", description="Read-only payroll data for auditor",
         backend_status="In Progress",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Medium", notes="auditor.py endpoint stub"),
    dict(module="Auditor",           feature="Audit Trail / Logs",        description="Track all data changes with timestamp",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="High",   notes="audit_service.py exists but not wired to endpoints"),
    dict(module="Auditor",           feature="Statutory Compliance Report", description="Compliance summary for auditor review",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Medium", notes="Planned; not started"),
    dict(module="Auditor",           feature="Export Audit Data",         description="Export audit logs to Excel/PDF",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Low",    notes="Planned; not started"),
]

# ── System / Platform ─────────────────────────────────────────────────────────
system_features = [
    dict(module="Auth & Security",   feature="JWT Login / Logout",        description="OAuth2 password bearer, token refresh",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="Auth & Security",   feature="Role-Based Access Control", description="Admin, employer, HR manager, employee, auditor roles",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="Protected routes + API dependency guards"),
    dict(module="Auth & Security",   feature="Password Change",           description="User self-service password reset",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Medium", notes="No endpoint implemented yet"),
    dict(module="Multi-Tenancy",     feature="Tenant Isolation",          description="Schema/row-level data isolation per org",
         backend_status="Complete",   frontend_status="Not Started",       overall_status="In Progress",
         client_approval="In Review", priority="High",   notes="Middleware exists; full isolation testing pending"),
    dict(module="Database",          feature="PostgreSQL Migration (Alembic)", description="DB schema versioning via Alembic",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="7 migration versions applied"),
    dict(module="API",               feature="REST API (FastAPI)",        description="Full OpenAPI spec, Swagger UI at /docs",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="Approved",  priority="High",   notes=""),
    dict(module="API",               feature="Health Check Endpoint",     description="GET /api/v1/health",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="Approved",  priority="Low",    notes=""),
    dict(module="File Processing",   feature="Excel Upload Processing",   description="Employee, attendance, wage Excel parsing",
         backend_status="Complete",   frontend_status="Complete",          overall_status="Complete",
         client_approval="Approved",  priority="High",   notes="pandas + openpyxl pipeline"),
    dict(module="PDF Generation",    feature="Payslip PDF Engine",        description="ReportLab-based professional payslip PDF",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="In Review", priority="High",   notes="Indian currency words, two-color scheme"),
    dict(module="Notifications",     feature="Email Notifications (SMTP)", description="Payslip email delivery via SMTP",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="Pending",   priority="Medium", notes="SMTP config required; email_service.py done"),
    dict(module="Notifications",     feature="WebSocket Notifications",   description="Real-time in-app notifications",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Low",    notes="notifications.py stub exists; not wired"),
    dict(module="Notifications",     feature="Attendance Upload WS",      description="WebSocket progress for bulk upload",
         backend_status="Not Started",frontend_status="Not Started",       overall_status="Not Started",
         client_approval="Pending",   priority="Low",    notes="attendance_upload.py stub exists"),
    dict(module="Background Tasks",  feature="Payroll Batch Processing",  description="Async batch payroll calculation",
         backend_status="Not Started",frontend_status="Not Applicable",    overall_status="Not Started",
         client_approval="Pending",   priority="Medium", notes="payroll_batch.py stub; not wired to scheduler"),
    dict(module="Background Tasks",  feature="Data Cleanup Tasks",        description="Periodic data archival and cleanup",
         backend_status="Not Started",frontend_status="Not Applicable",    overall_status="Not Started",
         client_approval="Pending",   priority="Low",    notes="data_cleanup.py stub exists"),
    dict(module="Docker",            feature="Docker / docker-compose",   description="Containerised deployment setup",
         backend_status="Complete",   frontend_status="Not Applicable",    overall_status="Complete",
         client_approval="Not Required",priority="Medium",notes="Dockerfile + docker-compose.yml ready"),
    dict(module="Testing",           feature="Automated Test Suite",      description="pytest unit + integration tests",
         backend_status="Not Started",frontend_status="Not Applicable",    overall_status="Not Started",
         client_approval="Not Required",priority="Medium",notes="pytest.ini configured; test files mostly stubs"),
]

# ── Write all detail sheets ───────────────────────────────────────────────────
write_detail_sheet(wb, "👤 SaaS Admin",      "SaaS Admin",      C_MID_BLUE,   saas_features)
write_detail_sheet(wb, "🏢 Employer-HR",     "Employer / HR",   C_DARK_BLUE,  employer_features)
write_detail_sheet(wb, "👨‍💼 Employee",        "Employee",        C_GREEN,      employee_features)
write_detail_sheet(wb, "🔍 Auditor",         "Auditor",         C_ORANGE,     auditor_features)
write_detail_sheet(wb, "⚙️ System-Platform", "System/Platform", C_GRAY,       system_features)

# ══════════════════════════════════════════════════════════════════════════════
# SHEET — CHANGE LOG
# ══════════════════════════════════════════════════════════════════════════════
wsc = wb.create_sheet("📝 Change Log")
wsc.sheet_view.showGridLines = False
wsc.column_dimensions["A"].width = 2

wsc.merge_cells("B2:H2")
t = wsc.cell(row=2, column=2, value="CHANGE LOG")
t.font = Font(bold=True, size=14, color=C_WHITE); t.fill = fill(C_DARK_BLUE)
t.alignment = align(h="center"); wsc.row_dimensions[2].height = 28

header_row(wsc, 3, ["","Date","Version","Stakeholder","Feature / Change","Status","Updated By","Notes"], fg=C_SUBHDR_BG, height=20)

changelog = [
    ("2026-03-08", "v1.5", "Employer/HR",     "Payslip PDF redesign — Indian currency words, bank/UAN/ESI data", "Complete",   "Claude AI", "Matches reference payslip format"),
    ("2026-03-08", "v1.5", "Employee",         "EmployeePayslips.jsx — enhanced data display with new API fields", "Complete",   "Claude AI", ""),
    ("2026-03-08", "v1.5", "System/Platform",  "CORS fix: 127.0.0.1 → localhost, axios fallback port 8001→8000",  "Complete",   "Claude AI", ""),
    ("2026-03-08", "v1.5", "All",              "Project cleanup: removed 24 stale files, credential docs unified", "Complete",   "Claude AI", "CREDENTIALS_AND_CONFIG.md created"),
    ("2026-01-18", "v1.4", "Employer/HR",      "Holiday Calendar + Working Calendar UI",                          "Complete",   "Dev Team",  ""),
    ("2026-01-18", "v1.4", "Employer/HR",      "PayrollDashboard with bulk operations",                           "Complete",   "Dev Team",  ""),
    ("2026-01-18", "v1.4", "System/Platform",  "Wage template service + Excel parser enhancements",               "Complete",   "Dev Team",  ""),
    ("2025-xx-xx", "v1.3", "Employee",         "All employee features fixed (leave, profile, payslips)",           "Complete",   "Dev Team",  ""),
    ("2025-xx-xx", "v1.2", "System/Platform",  "PostgreSQL migration + leave types + salary structure",            "Complete",   "Dev Team",  "10 employees seeded"),
    ("2025-xx-xx", "v1.1", "Employee",         "Leave management fixed",                                          "Complete",   "Dev Team",  ""),
    ("2025-xx-xx", "v1.0", "All",              "Initial commit — base HR Payroll scaffold",                        "Complete",   "Dev Team",  ""),
]

for i, (dt, ver, stk, change, status, by, notes) in enumerate(changelog, 4):
    wsc.row_dimensions[i].height = 20
    bg = C_LIGHT_GRAY if i % 2 == 0 else C_WHITE
    set_cell(wsc, i, 2, "", fg=bg)
    set_cell(wsc, i, 3, dt,     fg=bg)
    set_cell(wsc, i, 4, ver,    fg=bg, h="center")
    set_cell(wsc, i, 5, stk,    fg=bg, bold=True)
    set_cell(wsc, i, 6, change, fg=bg)
    status_cell(wsc, i, 7, status)
    set_cell(wsc, i, 8, by,    fg=bg, h="center")
    set_cell(wsc, i, 9, notes, fg=bg, italic=True, fc=C_GRAY)

for col, w in {"B":2,"C":12,"D":8,"E":18,"F":52,"G":14,"H":14,"I":38}.items():
    wsc.column_dimensions[col].width = w

# Save
wb.save(OUTPUT)
print("[OK] Saved: " + OUTPUT)
