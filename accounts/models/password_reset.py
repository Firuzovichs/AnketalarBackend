import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone

class PasswordReset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # reset_id
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="password_resets")
    otp_id = models.UUIDField(null=True, blank=True)
    reset_token = models.UUIDField(null=True, blank=True, unique=True)
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_confirmed(self) -> bool:
        return self.confirmed_at is not None

    @property
    def is_used(self) -> bool:
        return self.used_at is not None

    @classmethod
    def create_for_user(cls, user, ttl_minutes: int = 15):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
        )
