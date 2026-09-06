import os
from dotenv import load_dotenv
import smtplib
import ssl
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")


SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=465

def send_email(subject, message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:

        msg = EmailMessage()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = NOTIFICATION_EMAIL
        msg["Subject"] = subject

        msg.set_content(message)

        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)

        server.send_message(msg)




