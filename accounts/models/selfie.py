from django.db import models


class VerificationSelfie(models.Model):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="verification_selfie",
        db_index=True,
    )

    image = models.ImageField(upload_to="verification/selfies/")
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["uploaded_at"]),
        ]

    def __str__(self):
        return f"Selfie({self.user_id})"
