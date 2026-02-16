import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from accounts.models import OTPVerification


def _generate_code() -> str:
    return f"{random.randint(0, 999999):06d}"




def create_otp(*, user, channel: str, destination: str, ttl_minutes: int = 5):
    code = _generate_code()
    item = OTPVerification.objects.create(
        user=user,
        channel=channel,
        destination=destination,
        code_hash=make_password(code),
        expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
    )
    return item, code


def verify_otp(*, user, otp_id, code: str, max_attempts: int = 5) -> str:
    try:
        item = OTPVerification.objects.get(id=otp_id, user=user)
    except OTPVerification.DoesNotExist:
        return "not_found"

    if item.is_used:
        return "expired"

    if item.is_expired:
        return "expired"

    if item.attempts >= max_attempts:
        return "too_many_attempts"

    item.attempts += 1
    item.save(update_fields=["attempts"])

    ok = check_password(code, item.code_hash)

    if not ok:
        return "invalid_code"

    item.mark_used()
    return "success"