from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
template = env.get_template("payslip.html")

data = {
    "employer": "Acme Lending Ltd (SAMPLE)",
    "employee_name": "Avery J. Morgan",
    "employee_address": "12 Demo Lane, Brixton, London, SW9 0DE",
    "ni_number": "GB-NINO-DEMO-1234",
    "ni_category": "A",
    "employee_id": "EMP-0001",
    "tax_code": "1257L",
    "tax_basis": "Cumulative",
    "pay_period": "01/08/2025 - 31/08/2025",
    "tax_month": "5",
    "payment_date": "28/08/2025",
    "gross_pay": "4,333.33",
    "net_pay": "3,275.31",
    "total_pay": "3,275.31"
}

earnings = [
    {"description": "Public Holiday (Summer Bank Holiday - 25/08/2025)", "quantity": "8.00", "rate": "200.00", "amount_this": "200.00", "amount_ytd": "200.00"},
    {"description": "Regular Hours", "quantity": "", "rate": "", "amount_this": "4,133.33", "amount_ytd": "20,666.65"},
    {"description": "Other Previous Earnings", "quantity": "", "rate": "", "amount_this": "800.00", "amount_ytd": "800.00"}
]
deductions = [
    {"description": "PAYE", "amount_this": "620.40", "amount_ytd": "3,101.60"},
    {"description": "Employee National Insurance Contribution - A", "amount_this": "254.17", "amount_ytd": "1,270.85"},
    {"description": "Pension Contribution", "amount_this": "183.45", "amount_ytd": "917.25"}
]
contributions = [
    {"description": "Employer National Insurance Contribution - A", "amount_this": "587.45", "amount_ytd": "2,937.25"}
]

html = template.render(
    **data,
    earnings=earnings,
    deductions=deductions,
    contributions=contributions,
    total_earnings="4,333.33",
    total_earnings_ytd="21,666.65",
    total_deductions="1,058.02",
    total_deductions_ytd="5,289.70",
    total_contrib="587.45",
    total_contrib_ytd="2,937.25"
)

out_html = os.path.join(OUT, "payslip_sample.html")
out_pdf  = os.path.join(OUT, "payslip_sample.pdf")
with open(out_html, "w") as f:
    f.write(html)
HTML(out_html).write_pdf(out_pdf)
print("✅ Generated:", out_pdf)
