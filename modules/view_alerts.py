import sqlite3

connection = sqlite3.connect("database/soc_alerts.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM alerts")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()