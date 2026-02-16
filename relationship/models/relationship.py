from django.db import models
from django.core.exceptions import ValidationError

class RelationStatus(models.TextChoices):
    LIKED = "LIKED", "Liked"
    SKIPPED = "SKIPPED", "Skipped"
    REJECTED = "REJECTED", "Rejected"
    MATCHED = "MATCHED", "Matched"

class Relationship(models.Model):
    from_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="relations_sent")
    to_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="relations_received")

    status = models.CharField(max_length=12, choices=RelationStatus.choices, db_index=True)
    comment = models.TextField(blank=True, null=True)
    comment_liked_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_user", "to_user"], name="uq_relationship_pair"),
        ]
        indexes = [
            models.Index(fields=["to_user", "status", "updated_at"]),
            models.Index(fields=["from_user", "status", "updated_at"]),
        ]

    def clean(self):
        if self.from_user_id and self.to_user_id and self.from_user_id == self.to_user_id:
            raise ValidationError({"to_user": "O'zingizga like bosib bo'lmaydi."})
