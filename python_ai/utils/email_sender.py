import os
import ssl
import smtplib
from email.message import EmailMessage

import requests
from dotenv import load_dotenv

load_dotenv()

# Resend (HTTP API) - works on Render free tier
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "onboarding@resend.dev")

# Gmail SMTP - only used locally when RESEND_API_KEY is not set
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Recipient (same variable you already use)
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def _send_with_resend(subject, message):
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": EMAIL_FROM,
            "to": [NOTIFICATION_EMAIL],
            "subject": subject,
            "text": message,
        },
        timeout=20,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Resend error {response.status_code}: {response.text}"
        )


def _send_with_smtp(subject, message):
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = NOTIFICATION_EMAIL
    msg["Subject"] = subject
    msg.set_content(message)

    with smtplib.SMTP_SSL(
        SMTP_SERVER, SMTP_PORT, context=context, timeout=20
    ) as server:
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)


def send_email(subject, message):

    if not NOTIFICATION_EMAIL:
        raise RuntimeError("NOTIFICATION_EMAIL is not configured.")

    if RESEND_API_KEY:
        _send_with_resend(subject, message)
    else:
        _send_with_smtp(subject, message)