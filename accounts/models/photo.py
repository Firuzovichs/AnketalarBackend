from django.db import models, transaction
from django.core.exceptions import ValidationError

def user_photo_upload_to(instance, filename: str) -> str:
    return f"users/{instance.user_id}/photos/{filename}"

class UserPhoto(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to=user_photo_upload_to)

    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-is_main", "order", "-created_at")
        indexes = [
            models.Index(fields=["user", "is_main"]),
        ]
        constraints = [
            # Har bir userda faqat 1 ta main photo bo'lsin
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(is_main=True),
                name="uq_one_main_photo_per_user",
            ),
        ]

    def clean(self):
        # 6 tagacha limit (DB constraint bilan emas, model validation bilan)
        if not self.pk:
            existing = UserPhoto.objects.filter(user_id=self.user_id).count()
            if existing >= 6:
                raise ValidationError("Maksimal 6 ta rasm yuklash mumkin.")

    def save(self, *args, **kwargs):
        # 6 limitni tekshirish uchun clean()ni chaqiramiz (constraintni emas)
        self.clean()

        # Main qilishni atomik qilamiz
        if self.is_main:
            with transaction.atomic():
                # oldin hammasini false qilamiz
                UserPhoto.objects.select_for_update().filter(user_id=self.user_id, is_main=True).update(is_main=False)
                # keyin o'zini true saqlaymiz
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo {self.id} for user {self.user_id}"
