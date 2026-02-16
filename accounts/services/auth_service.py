from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, FaceStatus,TelegramLinkToken
from accounts.services.otp_service import create_otp, verify_otp
from accounts.services.notification_service import send_otp_email, send_otp_telegram


def register_user(*, nickname, password, phone, email, ttl_minutes=5):
    user = User.objects.create_user(
        nickname=nickname.strip().lower(),
        password=password,
        phone=phone or None,
        email=email or None,
        is_active=False,
        face_status=FaceStatus.PENDING,
    )

    if email:
        otp_item, code = create_otp(user=user, channel="email", destination=email, ttl_minutes=ttl_minutes)
        send_otp_email(email, code)
        return {
            "user": user,
            "otp_id": otp_item.id,
            "expires_in": ttl_minutes * 60,
            "channel": "email",
        }

    if user.telegram_chat_id:
        otp_item, code = create_otp(user=user, channel="phone", destination=phone, ttl_minutes=ttl_minutes)
        send_otp_telegram(user.telegram_chat_id, code)
        return {
            "user": user,
            "otp_id": otp_item.id,
            "expires_in": ttl_minutes * 60,
            "channel": "telegram",
        }

    tg_token = TelegramLinkToken.create_for_user(user, ttl_minutes=30)
    return {
        "user": user,
        "channel": "telegram_link_required",
        "tg_link_token": tg_token.id,
        "message": "Telegram botga /start <token> yuboring, so'ng OTP resend qiling.",
    }


def confirm_otp(*, nickname: str, otp_id, code: str) -> None:
    user = User.objects.get(nickname=nickname.strip().lower())

    result = verify_otp(user=user, otp_id=otp_id, code=code)

    if result == "invalid_code":
        raise ValueError("invalid_code")

    if result == "expired":
        raise ValueError("expired")

    if result == "not_found":
        raise ValueError("not_found")

    if result == "too_many_attempts":
        raise ValueError("too_many_attempts")

    if result != "success":
        raise ValueError("otp_error")

    user.is_active = True
    if user.phone:
        user.phone_verified = True
    if user.email:
        user.email_verified = True

    user.save(update_fields=["is_active", "phone_verified", "email_verified"])

def login_user(*, nickname: str, password: str) -> dict:
    nickname = nickname.strip().lower()
    user = authenticate(nickname=nickname, password=password)

    if not user:
        raise ValueError("Invalid credentials")
    if not user.is_active:
        raise ValueError("OTP verification required")

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "nickname": user.nickname,
            "phone_verified": user.phone_verified,
            "email_verified": user.email_verified,
            "face_status": user.face_status,
        },
    }

def resend_otp_for_user(*, nickname: str, ttl_minutes: int = 5):
    user = User.objects.get(nickname=nickname)

    if user.email:
        otp_item, code = create_otp(user=user, channel="email", destination=user.email, ttl_minutes=ttl_minutes)
        send_otp_email(user.email, code)
        return {"otp_id": otp_item.id, "expires_in": ttl_minutes * 60, "channel": "email"}

    if not user.telegram_chat_id:
        tg_token = TelegramLinkToken.create_for_user(user, ttl_minutes=30)
        return {"channel": "telegram_link_required", "tg_link_token": tg_token.id}

    otp_item, code = create_otp(user=user, channel="phone", destination=user.phone or "", ttl_minutes=ttl_minutes)
    send_otp_telegram(user.telegram_chat_id, code)
    return {"otp_id": otp_item.id, "expires_in": ttl_minutes * 60, "channel": "telegram"}