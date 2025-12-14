import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_email(recipient, subject, html_content):
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Job Alerts <onboarding@resend.dev>",
            "to": [recipient],
            "subject": subject,
            "html": html_content,
        },
        timeout=15
    )

    if response.status_code >= 400:
        print("Email failed:", response.text)
        return False

    print(f"Email sent to {recipient}")
    return True



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587


# EMAIL_USER = os.environ.get("JOB_AGG_EMAIL")  # your sending email (Gmail recommended)
# EMAIL_PASS = os.environ.get("JOB_AGG_EMAIL_PASS")  # app password or SMTP password

# def send_email(recipient, subject, html_content):
#     """Send HTML job alert email."""

#     msg = MIMEMultipart("alternative")
#     msg["From"] = EMAIL_USER
#     msg["To"] = recipient
#     msg["Subject"] = subject

#     msg.attach(MIMEText(html_content, "html"))

#     try:
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(EMAIL_USER, EMAIL_PASS)
#         server.sendmail(EMAIL_USER, recipient, msg.as_string())
#         server.quit()

#         print(f"Email sent to {recipient}")
#         return True

#     except Exception as e:
#         print(f"Email failed: {e}")
#         return False
