import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("reports/soc_report.pdf")
styles = getSampleStyleSheet()

elements = []

elements.append(Paragraph("SOC INCIDENT REPORT", styles['Title']))
elements.append(Spacer(1, 20))

connection = sqlite3.connect("database/soc_alerts.db")
cursor = connection.cursor()

cursor.execute("SELECT alert_type, ip_address, details FROM alerts")
rows = cursor.fetchall()

for row in rows:
    alert_type, ip, details = row

    elements.append(
        Paragraph(
            f"<b>{alert_type}</b><br/>IP: {ip}<br/>Details: {details}",
            styles['BodyText']
        )
    )
    elements.append(Spacer(1, 15))

connection.close()

doc.build(elements)

print("PDF Report Generated Successfully!")