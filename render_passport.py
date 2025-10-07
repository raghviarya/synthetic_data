# render_passport.py
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Paths
TEMPLATES = "templates"
OUT = "demo_output"
os.makedirs(OUT, exist_ok=True)

# Load Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
template = env.get_template("passport.html")

# Synthetic identity data
data = {
    "issuing_country": "UNITED KINGDOM (SAMPLE)",
    "surname": "Morgan",
    "given_names": "Avery J.",
    "nationality": "British (SAMPLE)",
    "dob": "1993-04-18",
    "place_of_birth": "London, GBR",
    "sex": "F",
    "passport_number": "GB00DEMO456",
    "issuing_authority": "HM Passport Office (SAMPLE)",
    "date_of_issue": "2023-06-13",
    "date_of_expiry": "2033-06-12",
    "photo_label": "PHOTO",
    "signature_label": "(signature)",
    "mrz_line1": "P<GBRMORGAN<<AVERY<J<<<<<<<<<<<<<<<<<<<<<<",
    "mrz_line2": "GB00DEMO4561234567890<<<<<<<<<<<<<<00"
}

# Render the template
html = template.render(**data)

# Output paths
out_html = os.path.join(OUT, "passport_sample.html")
out_pdf = os.path.join(OUT, "passport_sample.pdf")

# Write HTML file (optional, for debugging)
with open(out_html, "w") as f:
    f.write(html)

# Convert to PDF
HTML(out_html).write_pdf(out_pdf)
print(f"✅ Passport PDF generated: {out_pdf}")
