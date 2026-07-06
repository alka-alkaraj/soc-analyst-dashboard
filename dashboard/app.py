import streamlit as st
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from datetime import date
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="SOC Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

st.title("🛡️ SOC ANALYST DASHBOARD")

connection = sqlite3.connect("database/soc_alerts.db")
cursor = connection.cursor()

if st.button("🗑️ Clear All Alerts"):
    cursor.execute("DELETE FROM alerts")
    connection.commit()
    st.success("All alerts deleted successfully!")
    st.rerun()

cursor.execute("SELECT COUNT(*) FROM alerts")
total_alerts = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM alerts")
unique_ips = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM alerts WHERE alert_type='IOC Alert'")
ioc_count = cursor.fetchone()[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Alerts", total_alerts)
col2.metric("Malicious IPs", ioc_count)
col3.metric("Unique Attackers", unique_ips)

st.divider()

st.subheader("🔎 Search Alerts by IP")
search_ip = st.text_input("Enter IP Address")

st.divider()

st.subheader("📅 Filter Alerts by Date")
selected_date = st.date_input("Select Date", date.today())

st.divider()

st.subheader("🚨 Alerts")

cursor.execute("""
SELECT timestamp, alert_type, ip_address, details
FROM alerts
""")

rows = cursor.fetchall()

for row in rows:
    timestamp, alert_type, ip, details = row
    alert_date = timestamp.split(" ")[0]

    if (search_ip == "" or search_ip == ip) and str(selected_date) == alert_date:

        if alert_type == "IOC Alert":
            severity = "🔴 CRITICAL"
        else:
            severity = "🟠 HIGH"

        st.error(
            f"{severity} | {timestamp} | {alert_type} | {ip} | {details}"
        )

st.divider()

st.subheader("📊 Attack Distribution")

chart_df = pd.read_sql_query("""
SELECT ip_address, COUNT(*) AS alerts
FROM alerts
GROUP BY ip_address
""", connection)

if not chart_df.empty:
    fig, ax = plt.subplots()
    ax.bar(chart_df["ip_address"], chart_df["alerts"])
    ax.set_ylabel("Number of Alerts")
    ax.set_xlabel("IP Address")
    st.pyplot(fig)

st.divider()

st.subheader("🥧 Alert Types Distribution")

pie_df = pd.read_sql_query("""
SELECT alert_type, COUNT(*) AS alerts
FROM alerts
GROUP BY alert_type
""", connection)

if not pie_df.empty:
    fig, ax = plt.subplots()
    ax.pie(
        pie_df["alerts"],
        labels=pie_df["alert_type"],
        autopct="%1.1f%%"
    )
    st.pyplot(fig)

st.divider()

st.subheader("📈 Attack Timeline")

timeline_df = pd.read_sql_query("""
SELECT DATE(timestamp) AS alert_date,
       COUNT(*) AS total_alerts
FROM alerts
GROUP BY DATE(timestamp)
ORDER BY alert_date
""", connection)

if not timeline_df.empty:
    fig, ax = plt.subplots()
    ax.plot(
        timeline_df["alert_date"],
        timeline_df["total_alerts"],
        marker="o"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Alerts")
    st.pyplot(fig)

st.divider()

st.subheader("📋 Saved Alerts")

df = pd.read_sql_query(
    "SELECT * FROM alerts",
    connection
)

if not df.empty:
    df["Severity"] = df["alert_type"].apply(
        lambda x: "🔴 CRITICAL" if x == "IOC Alert" else "🟠 HIGH"
    )

st.dataframe(df)

st.divider()

st.subheader("📥 Download Alerts")

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Alerts CSV",
    data=csv,
    file_name="soc_alerts.csv",
    mime="text/csv"
)

connection.close()