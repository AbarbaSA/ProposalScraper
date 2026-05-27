import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_email(subject, body_text):
    if not MAILGUN_API_KEY:
        raise ValueError("MAILGUN_API_KEY is not set in environment")
    if not MAILGUN_DOMAIN:
        raise ValueError("MAILGUN_DOMAIN is not set in environment")
    if not EMAIL_FROM:
        raise ValueError("EMAIL_FROM is not set in environment")
    if not EMAIL_TO:
        raise ValueError("EMAIL_TO is not set in environment")

    separators = [",", ";"]
    raw_recipients = [EMAIL_TO]
    for sep in separators:
        if sep in EMAIL_TO:
            raw_recipients = EMAIL_TO.replace(";", ",").split(",")
            break

    recipients = [email.strip() for email in raw_recipients if email.strip()]
    if not recipients:
        raise ValueError("EMAIL_TO must contain at least one recipient email")

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": EMAIL_FROM,
            "to": recipients,
            "subject": subject,
            "text": body_text,
        },
        timeout=20,
    )

    if response.status_code >= 300:
        raise RuntimeError(
            f"Mailgun send failed: {response.status_code} {response.text}"
        )
