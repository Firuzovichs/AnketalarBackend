from django.db import models
from django.utils import timezone

class DailyQuota(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="daily_quotas")
    date = models.DateField(db_index=True)
    used = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "date")
        indexes = [models.Index(fields=["user", "date"])]

    @classmethod
    def today_for(cls, user):
        today = timezone.localdate()
        obj, _ = cls.objects.get_or_create(user=user, date=today, defaults={"used": 0})
        return obj
