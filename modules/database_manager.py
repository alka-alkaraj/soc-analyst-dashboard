import sqlite3
from datetime import datetime

def save_alert(alert_type, ip_address, details):
    connection = sqlite3.connect("database/soc_alerts.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        alert_type TEXT,
        ip_address TEXT,
        details TEXT
    )
    """)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO alerts (timestamp, alert_type, ip_address, details) VALUES (?, ?, ?, ?)",
        (timestamp, alert_type, ip_address, details)
    )

    connection.commit()
    connection.close()