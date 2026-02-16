from django.db import models
from django.utils import timezone

class RelationStatus(models.TextChoices):
    LIKED = "LIKED", "Liked"
    SKIPPED = "SKIPPED", "Skipped"
    REJECTED = "REJECTED", "Rejected"
    MATCHED = "MATCHED", "Matched"

class Relationship(models.Model):
    from_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="relations_sent")
    to_user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="relations_received")

    status = models.CharField(max_length=12, choices=RelationStatus.choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Like bilan birga comment (optional)
    comment = models.TextField(blank=True)
    comment_liked_at = models.DateTimeField(null=True, blank=True)  # comment_like bosilganda

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_user", "to_user"], name="uq_relationship_pair"),
            models.CheckConstraint(check=~models.Q(from_user=models.F("to_user")), name="ck_not_self"),
        ]
        indexes = [
            models.Index(fields=["to_user", "status", "updated_at"]),
            models.Index(fields=["from_user", "status", "updated_at"]),
        ]
