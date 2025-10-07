import os
import subprocess
from datetime import datetime

# List of render scripts
scripts = [
    "render_passport.py",
    "render_bank_statement.py",
    "render_payslip.py",
    "render_utility_bill.py",
    "render_p60.py",
    "render_credit_report.py"
]

print("🚀 Running all document generators...\n")

for s in scripts:
    path = os.path.join(os.getcwd(), s)
    if not os.path.exists(path):
        print(f"⚠️  Skipping {s} (file not found)")
        continue
    print(f"▶️  Generating via {s} ...")
    result = subprocess.run(["python", s], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {s} completed successfully\n")
    else:
        print(f"❌ {s} failed:")
        print(result.stderr)
        print("-" * 60)

# Zip everything for easy sharing
import zipfile
zip_name = f"demo_documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
zip_path = os.path.join("demo_output", zip_name)
os.makedirs("demo_output", exist_ok=True)

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in os.listdir("demo_output"):
        if f.endswith(".pdf"):
            zf.write(os.path.join("demo_output", f), arcname=f)

print(f"\n📦 All done! Zipped PDFs saved to: {zip_path}")
