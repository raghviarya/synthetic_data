# render_credit_report_full.py
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from datetime import datetime, timedelta
import random

TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
tpl = env.get_template("credit_report.html")

# --- helper to generate synthetic 24-month history (pattern) ---
def make_history(pattern=None):
    # pattern: list of tokens e.g. ["OK","OK","1","OK",...]
    # ensure exactly 24 months. If pattern shorter, repeat/truncate.
    base = pattern or ["OK"] * 24
    if len(base) < 24:
        base = (base * ((24 // len(base)) + 1))[:24]
    else:
        base = base[:24]
    months = []
    # create labels for the 24 months (most recent last)
    today = datetime.now()
    for i, val in enumerate(base):
        label_month = (today - timedelta(days=30*(24 - i))).strftime("%b %y")
        months.append({"value": val, "label": f"{label_month} {val}"})
    return months

# --- assemble synthetic report data ---
report = {
    "report_id": f"DCR-{datetime.now().strftime('%Y%m%d')}-FULL-001",
    "report_datetime": datetime.now().strftime("%d %b %Y %H:%M"),
    "full_name": "Avery J. Morgan",
    "dob": "1993-04-18",
    "address": "12 Demo Lane, Brixton, London, SW9 0DE",
    "employer": "Acme Lending Ltd (SAMPLE)",
    "employment_tenure": "2 years, 7 months",
    "electoral_roll": "Confirmed at current address",
    "linked_addresses_count": 2,
    "score": 702,
    "score_max": 999,
    "band": "Fair",
    "percentile": 58,
    "score_comment": "Accounts are generally well maintained. Moderate utilisation and an isolated late payment.",
    "score_factors": [
        "Short overall credit history (<3 years)",
        "One recent 30-day late payment",
        "Moderate utilisation (~44%)",
        "Stable employment and address history"
    ],
    "score_history": [{"month": (datetime.now()-timedelta(days=30*(11-i))).strftime("%b"), "score": 680 + i*2, "avg": 670 + i*2} for i in range(12)],
    "stats": {
        "total_open_accounts": 7,
        "closed_accounts_recent": 3,
        "total_limit": 12000,
        "total_balance": 5320,
        "utilisation": 44,
        "on_time_rate": 96
    }
}

# --- build many open accounts with different patterns ---
open_accounts = []
types = ["Credit Card", "Personal Loan", "Current Account (Overdraft)", "Car Finance", "Mortgage", "Store Card", "Student Loan"]
for i in range(1, 13):  # generate 12 accounts, but will show a subset depending on template length
    acc_type = random.choice(types)
    opened = (datetime.now() - timedelta(days=random.randint(200, 2000))).strftime("%d %b %Y")
    limit = "—"
    if acc_type in ["Credit Card", "Store Card"]:
        limit = str(random.randint(500, 5000))
    elif acc_type == "Current Account (Overdraft)":
        limit = str(random.randint(200, 3000))
    elif acc_type == "Mortgage":
        limit = str(random.randint(50000, 300000))
    elif acc_type == "Personal Loan":
        limit = str(random.randint(1000, 20000))
    elif acc_type == "Car Finance":
        limit = str(random.randint(2000, 40000))
    balance = max(0, int(random.gauss(1500, 1200)))
    high_balance = max(balance, int(balance + random.uniform(0, 2000)))
    status = random.choice(["Open — Current", "Open — Low utilisation", "Open — Paying as agreed"])
    ref = f"ACC-{1000+i}"
    repayment = f"{random.randint(20, 450)}"
    notes = random.choice([
        "Standard account. Payment history shows occasional late payment.",
        "Low utilisation and account in good standing.",
        "Recent increase in balance due to seasonal spending.",
        "Account under promotional rate; normal payments in place."
    ])
    # create a realistic history: mostly OK with occasional lates
    pattern = []
    for _ in range(24):
        r = random.random()
        if r < 0.92:
            pattern.append("OK")
        elif r < 0.96:
            pattern.append("1")
        elif r < 0.98:
            pattern.append("2")
        else:
            pattern.append("M")  # missed
    history = make_history(pattern)
    open_accounts.append({
        "creditor": f"Demo Lender {i}",
        "type": acc_type,
        "opened": opened,
        "limit": limit,
        "balance": str(balance),
        "high_balance": str(high_balance),
        "status": status,
        "ref": ref,
        "repayment": repayment,
        "terms": "Representative APR varies",
        "notes": notes,
        "history": history
    })

# closed accounts (a few)
closed_accounts = [
    {"creditor":"Retail Store Ltd","type":"Store Card","opened":"05 Feb 2017","closed":"09 Jan 2021","status":"Settled","settlement":"Paid in full"},
    {"creditor":"Old Bank Plc","type":"Current Account","opened":"01 Mar 2012","closed":"01 Jul 2019","status":"Closed by customer","settlement":"N/A"},
    {"creditor":"Short Term Lender","type":"Payday loan","opened":"12 Jan 2018","closed":"10 Mar 2018","status":"Settled","settlement":"Paid"}
]

# public records example (empty or one sample)
public_records = []
# optionally add a sample public record for variety:
# public_records.append({"type":"CCJ","date":"15 Mar 2020","authority":"County Court","amount":"450","status":"Satisfied"})

financial_associations = [
    {"name":"Jamie Morgan","relation":"Spouse","accounts":"Joint mortgage with Demo Mortgage Bank","status":"Active"}
]

searches = [
    {"date":"26 Sep 2025","org":"Acme Lending Ltd","purpose":"Affordability check"},
    {"date":"03 Jun 2025","org":"TelecomsCo","purpose":"New contract"},
    {"date":"12 Jan 2025","org":"InsuranceCo","purpose":"Quote"}
]

risk_summary = (
    "The subject presents a moderate risk profile. Overall credit utilisation is approximately "
    f"{report['stats']['utilisation']}%. Payment history shows a predominance of on-time payments across accounts, "
    "with isolated late payments. No active public records recorded. The main contributors to the score are short "
    "credit history and recent credit activity."
)

# --- render and save ---
html = tpl.render(
    report_id=report["report_id"],
    report_datetime=report["report_datetime"],
    full_name=report["full_name"],
    dob=report["dob"],
    address=report["address"],
    employer=report["employer"],
    employment_tenure=report["employment_tenure"],
    electoral_roll=report["electoral_roll"],
    linked_addresses_count=report["linked_addresses_count"],
    score=report["score"],
    score_max=report["score_max"],
    band=report["band"],
    percentile=report["percentile"],
    score_comment=report["score_comment"],
    score_factors=report["score_factors"],
    score_history=report["score_history"],
    stats=report["stats"],
    open_accounts=open_accounts,
    closed_accounts=closed_accounts,
    public_records=public_records,
    searches=searches,
    financial_associations=financial_associations,
    risk_summary=risk_summary
)

out_html = os.path.join(OUT, "credit_report.html")
out_pdf  = os.path.join(OUT, "credit_report_full.pdf")

with open(out_html, "w") as f:
    f.write(html)

# Render PDF (WeasyPrint)
HTML(out_html).write_pdf(out_pdf)
print("✅ Generated detailed credit report:", out_pdf)
