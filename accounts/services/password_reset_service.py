import uuid
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from accounts.models.password_reset import PasswordReset
from accounts.services.otp_service import create_otp, verify_otp
from accounts.services.notification_service import send_otp_email, send_otp_telegram


class ResetError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@transaction.atomic
def start_password_reset(*, nickname: str, channel: str, ttl_minutes: int = 5):
    user = User.objects.filter(nickname=nickname).first()
    if not user:
        raise ResetError("user_not_found")

    reset = PasswordReset.create_for_user(user, ttl_minutes=15)

    if channel == "email":
        if not user.email:
            raise ResetError("email_not_set")
        otp_obj, code = create_otp(user=user, channel="email", destination=user.email, ttl_minutes=ttl_minutes)
        reset.otp_id = otp_obj.id
        reset.save(update_fields=["otp_id"])
        send_otp_email(user.email, code)
        return {"reset_id": str(reset.id), "otp_id": str(otp_obj.id), "channel": "email", "expires_in": ttl_minutes * 60}

    if channel == "telegram":
        if not user.telegram_chat_id:
            raise ResetError("telegram_not_linked")
        otp_obj, code = create_otp(user=user, channel="telegram", destination=str(user.telegram_chat_id), ttl_minutes=ttl_minutes)
        reset.otp_id = otp_obj.id
        reset.save(update_fields=["otp_id"])
        send_otp_telegram(user.telegram_chat_id, code)
        return {"reset_id": str(reset.id), "otp_id": str(otp_obj.id), "channel": "telegram", "expires_in": ttl_minutes * 60}

    raise ResetError("invalid_channel")


@transaction.atomic
def confirm_password_reset(*, reset_id: str, code: str):
    reset = PasswordReset.objects.select_for_update().filter(id=reset_id).first()
    if not reset:
        raise ResetError("reset_not_found")
    if reset.is_used:
        raise ResetError("reset_used")
    if reset.is_expired:
        raise ResetError("reset_expired")
    if reset.is_confirmed and reset.reset_token:
        return {"reset_token": str(reset.reset_token)}

    if not reset.otp_id:
        raise ResetError("otp_missing")

    ok = verify_otp(user=reset.user, otp_id=reset.otp_id, code=code)

    if not ok:
        raise ResetError("invalid_code")

    reset.confirmed_at = timezone.now()
    reset.reset_token = uuid.uuid4()
    reset.save(update_fields=["confirmed_at", "reset_token"])
    return {"reset_token": str(reset.reset_token)}


@transaction.atomic
def finish_password_reset(*, reset_token: str, new_password: str):
    reset = PasswordReset.objects.select_for_update().filter(reset_token=reset_token).first()
    if not reset:
        raise ResetError("reset_not_found")
    if reset.is_used:
        raise ResetError("reset_used")
    if reset.is_expired:
        raise ResetError("reset_expired")
    if not reset.is_confirmed:
        raise ResetError("reset_not_confirmed")

    validate_password(new_password, user=reset.user)
    reset.user.set_password(new_password)
    reset.user.save(update_fields=["password"])

    reset.used_at = timezone.now()
    reset.save(update_fields=["used_at"])
    return {"ok": True}
