import os
import requests
from django.core.mail import send_mail

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_otp_email(destination_email: str, code: str) -> None:
    subject = "Your verification code"
    message = f"Your OTP code is: {code}\nThis code will expire soon."
    send_mail(subject, message, None, [destination_email], fail_silently=False)

def send_otp_telegram(chat_id: int, code: str) -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": f"Your OTP code: {code}"}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
