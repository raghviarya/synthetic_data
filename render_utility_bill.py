from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
template = env.get_template("utility_bill.html")

data = {
    "full_name": "Avery J. Morgan",
    "address": "12 Demo Lane, Brixton, London, SW9 0DE",
    "account_number": "A-543C515F",
    "bill_reference": "265852997",
    "bill_date": "23 September 2025",
    "period_start": "20 Aug 2025",
    "period_end": "19 Sep 2025",
    "previous_balance": "15.30",
    "new_charges": "33.94",
    "total_due": "49.24",
    "payment_method": "Direct Debit",
    "payment_date": "08 October 2025",
    "meter_number": "23P2117307",
    "prev_reading": "1773.9",
    "prev_reading_date": "20 Aug 2025",
    "curr_reading": "1855.0",
    "curr_reading_date": "19 Sep 2025",
    "usage_kwh": "81.1",
    "unit_rate": "23.930",
    "standing_charge": "41.673",
    "standing_days": "31",
    "subtotal": "32.32",
    "vat_rate": "5",
    "vat_amount": "1.62",
    "total_electricity": "33.94",
    "tariff_name": "Next Flex (Sample)",
    "product_type": "Variable",
}

charges = [
    {"date":"16 Sep 2025","description":"Previous balance","amount":"15.30"},
    {"date":"20 Sep 2025","description":"Electricity charges","amount":"33.94"},
]

html = template.render(**data, charges=charges)
out_html = os.path.join(OUT, "utility_bill_sample.html")
out_pdf  = os.path.join(OUT, "utility_bill_sample.pdf")
with open(out_html, "w") as f:
    f.write(html)
HTML(out_html).write_pdf(out_pdf)
print("✅ Generated:", out_pdf)
