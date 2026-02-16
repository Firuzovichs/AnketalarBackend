import uuid
from django.db import models
from django.utils import timezone


class OTPChannel(models.TextChoices):
    PHONE = "phone", "phone"
    EMAIL = "email", "email"


class OTPVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="otp_items",
        db_index=True
    )

    channel = models.CharField(max_length=10, choices=OTPChannel.choices, db_index=True)
    destination = models.CharField(max_length=255, db_index=True) 
    code_hash = models.CharField(max_length=255) 

    expires_at = models.DateTimeField(db_index=True)
    used_at = models.DateTimeField(blank=True, null=True, db_index=True)

    attempts = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["destination", "created_at"]),
            models.Index(fields=["expires_at"]),
        ]

    def mark_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])

    @property
    def is_used(self) -> bool:
        return self.used_at is not None

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at
