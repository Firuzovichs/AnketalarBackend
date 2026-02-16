import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class TelegramLinkToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="tg_tokens")
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_for_user(cls, user, ttl_minutes: int = 30):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes)
        )

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_used(self):
        return self.used_at is not None
