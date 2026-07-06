from database_manager import save_alert
from email_sender import send_email
from threat_intel import check_ip

ioc_file = open("iocs/ioc_list.txt", "r")
ioc_list = [line.strip() for line in ioc_file]
ioc_file.close()

file = open("logs/sample_logs.txt", "r")

failed_counts = {}
alerted_ips = set()

for line in file:
    line = line.strip()

    if "Failed Login" in line:
        ip = line.split("IP=")[1]

        # Count failures
        if ip in failed_counts:
            failed_counts[ip] += 1
        else:
            failed_counts[ip] = 1

        # IOC Alert
        if ip in ioc_list and ip not in alerted_ips:
            print("🚨 MALICIOUS IP DETECTED:", ip)

            check_ip(ip)

            save_alert(
                "IOC Alert",
                ip,
                "Malicious IP detected from IOC list"
            )

            send_email(
                "SOC Alert - Malicious IP Detected",
                f"Malicious IP detected: {ip}"
            )

            alerted_ips.add(ip)

file.close()

print("\n--- BRUTE FORCE CHECK ---")

for ip, count in failed_counts.items():
    if count >= 5:
        print("🚨 BRUTE FORCE ALERT:", ip, "Failures:", count)

        check_ip(ip)

        save_alert(
            "Brute Force",
            ip,
            f"{count} failed login attempts"
        )

        send_email(
            "SOC Alert - Brute Force Attack",
            f"Brute Force detected from {ip}. Failed attempts: {count}"
        )

    else:
        print("IP:", ip, "Failures:", count)