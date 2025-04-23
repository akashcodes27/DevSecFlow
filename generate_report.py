import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data):
    c = canvas.Canvas("security_report.pdf", pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "🔐 Security Scan Report")

    c.setFont("Helvetica", 12)
    y = height - 80

    if not data["results"]:
        c.drawString(50, y, "✅ No issues found.")
    else:
        for i, finding in enumerate(data["results"], start=1):
            rule_id = finding.get("check_id", "N/A")
            file_path = finding["path"]
            message = finding["extra"].get("message", "No description")

            c.drawString(50, y, f"{i}. [{rule_id}] {message}")
            y -= 20
            c.drawString(70, y, f"📄 File: {file_path}")
            y -= 30

            if y < 100:  # Add new page if space runs out
                c.showPage()
                y = height - 50

    c.save()

if __name__ == "__main__":
    with open("semgrep_results.json", "r") as f:
        scan_data = json.load(f)
    generate_pdf(scan_data)
