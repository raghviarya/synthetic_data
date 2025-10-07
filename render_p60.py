from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
template = env.get_template("p60.html")

data = {
    "tax_year_end": "2025",
    "surname": "Morgan",
    "forenames": "Avery J.",
    "nino": "GB-NINO-DEMO-1234",
    "payroll_number": "EMP-0001",
    "pay_prev": "0.00",
    "tax_prev": "0.00",
    "pay_this": "42100.00",
    "tax_this": "5120.00",
    "pay_total": "42100.00",
    "tax_total": "5120.00",
    "tax_code": "1257L",
    "nic_letter": "A",
    "earnings_lel": "5824",
    "earnings_pt": "2216",
    "earnings_uel": "0",
    "employee_contrib": "348.00",
    "smp": "0.00",
    "spp": "0.00",
    "sap": "0.00",
    "sppar": "0.00",
    "student_loan": "0",
    "employee_name": "Avery J. Morgan",
    "employee_address": "12 Demo Lane, Brixton, London, SW9 0DE",
    "employer_name": "Acme Lending Ltd (SAMPLE)",
    "employer_address": "14 Example Street, London, EC1A 7AA",
    "paye_ref": "475/YB16356"
}

html = template.render(**data)
out_html = os.path.join(OUT, "p60_sample.html")
out_pdf  = os.path.join(OUT, "p60_sample.pdf")
with open(out_html, "w") as f:
    f.write(html)

HTML(out_html).write_pdf(out_pdf)
print("✅ Generated:", out_pdf)
