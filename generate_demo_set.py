import os, json, random, datetime
from faker import Faker
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

OUT = "demo_output"
TEMPLATES = "templates"
os.makedirs(OUT, exist_ok=True)
env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
fake = Faker("en_GB")

# --- Synthetic identity ---
person = {
    "full_name": "Avery J. Morgan",
    "employee_id": "EMP-0001",
    "nino": "GB-NINO-DEMO-1234",
    "employer": "Acme Lending Ltd",
    "paye_ref": "DEMO/PAYE/123",
    "bank_name": "Demo Bank PLC",
    "account_mask": "****1234",
    "sort_code": "12-34-56"
}

# --- Generate 3 months of payslips ---
payslip_dates = [datetime.date(2025, 7, 31), datetime.date(2025, 8, 31), datetime.date(2025, 9, 30)]
payslips = []
for d in payslip_dates:
    gross = 3500 + random.choice([0, -50, 100])
    tax = round(gross * 0.12, 2)
    ni = round(gross * 0.085, 2)
    net = round(gross - tax - ni, 2)
    payslips.append({
        "period": d.strftime("%B %Y"),
        "pay_date": d.strftime("%d/%m/%Y"),
        "gross": f"{gross:.2f}",
        "tax": f"{tax:.2f}",
        "ni": f"{ni:.2f}",
        "net": f"{net:.2f}"
    })

# --- Render payslips ---
payslip_tpl = env.get_template("payslip.html")
for i, p in enumerate(payslips, start=1):
    html = payslip_tpl.render(**person, **p)
    out_html = os.path.join(OUT, f"payslip_{i}.html")
    out_pdf = os.path.join(OUT, f"payslip_{i}.pdf")
    with open(out_html, "w") as f: f.write(html)
    HTML(out_html).write_pdf(out_pdf)
    print(f"✅ Created {out_pdf}")

# --- Generate bank statements ---
bank_tpl = env.get_template("bank_statement.html")
for i, p in enumerate(payslips, start=1):
    opening = round(2000 + random.uniform(-300, 300), 2)
    txs = []
    balance = opening
    # Add some transactions
    for desc, amt in [
        ("Coffee Shop", -4.50),
        ("PAYROLL ACME LENDING LTD", float(p["net"])),
        ("Grocery Store", -76.20)
    ]:
        balance += amt
        txs.append({
            "date": p["pay_date"],
            "description": desc,
            "amount": amt,
            "balance": balance
        })
    html = bank_tpl.render(
        bank_name=person["bank_name"],
        full_name=person["full_name"],
        account_mask=person["account_mask"],
        sort_code=person["sort_code"],
        period_from=p["pay_date"],
        period_to=p["pay_date"],
        transactions=txs
    )
    out_html = os.path.join(OUT, f"bank_statement_{i}.html")
    out_pdf = os.path.join(OUT, f"bank_statement_{i}.pdf")
    with open(out_html, "w") as f: f.write(html)
    HTML(out_html).write_pdf(out_pdf)
    print(f"✅ Created {out_pdf}")

print("All done! PDFs saved in", OUT)
