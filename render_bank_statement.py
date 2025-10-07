from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os, datetime

TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
template = env.get_template("bank_statement.html")

# Synthetic example
person = {
  "full_name": "Avery J. Morgan",
  "address": "12 Demo Lane, Brixton, London, SW9 0DE (SAMPLE)",
  "account_number": "00012345",
  "sort_code": "12-34-56",
  "period_start": "01 September 2025",
  "period_end": "30 September 2025",
  "opening_balance": "2,432.15",
  "money_in": "3,275.51",
  "money_out": "1,687.23",
  "closing_balance": "4,020.43"
}

transactions = [
  {"date":"01 Sep 2025","description":"Opening balance","amount":0.0,"balance":2432.15},
  {"date":"05 Sep 2025","description":"Coffee Shop","amount":-4.50,"balance":2427.65},
  {"date":"06 Sep 2025","description":"Grocery Store","amount":-76.20,"balance":2351.45},
  {"date":"10 Sep 2025","description":"Electric Co. - Direct Debit","amount":-45.00,"balance":2306.45},
  {"date":"15 Sep 2025","description":"Rent - Standing Order","amount":-1200.00,"balance":1106.45},
  {"date":"26 Sep 2025","description":"ACME LENDING LTD - Salary","amount":3275.51,"balance":4381.96},
  {"date":"30 Sep 2025","description":"Closing balance","amount":0.0,"balance":4381.96}
]

html = template.render(**person, transactions=transactions)
out_html = os.path.join(OUT, "bank_statement_sample.html")
out_pdf  = os.path.join(OUT, "bank_statement_sample.pdf")

with open(out_html, "w") as f:
    f.write(html)

HTML(out_html).write_pdf(out_pdf)
print("✅ Generated:", out_pdf)
