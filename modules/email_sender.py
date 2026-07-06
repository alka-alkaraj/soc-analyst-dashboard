import smtplib
from email.message import EmailMessage

def send_email(subject, body):
    sender_email = "alka.raj.031@gmail.com"
    receiver_email = "alka.raj.031@gmail.com"
    app_password = "pmji kbar phpz dlia"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")