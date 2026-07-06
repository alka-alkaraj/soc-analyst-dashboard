import requests

API_KEY = "YOUR_API_KEY"

def check_ip(ip):
    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if "data" in data:
        abuse_score = data["data"]["abuseConfidenceScore"]
        country = data["data"]["countryCode"]

        print("IP:", ip)
        print("Abuse Score:", abuse_score)
        print("Country:", country)

        if abuse_score == 0:
            severity = "LOW"
        elif abuse_score < 50:
            severity = "MEDIUM"
        elif abuse_score < 80:
            severity = "HIGH"
        else:
            severity = "CRITICAL"

        if severity == "LOW":
            print("🟢 Severity: LOW")
        elif severity == "MEDIUM":
            print("🟡 Severity: MEDIUM")
        elif severity == "HIGH":
            print("🟠 Severity: HIGH")
        else:
            print("🔴 Severity: CRITICAL")

    else:
        print("Could not get information.")