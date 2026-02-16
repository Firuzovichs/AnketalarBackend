from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _norm(self, nickname: str) -> str:
        return (nickname or "").strip().lower()

    def create_user(self, nickname: str, password: str = None, **extra_fields):
        nickname = self._norm(nickname)
        if not nickname:
            raise ValueError("nickname is required")

        user = self.model(nickname=nickname, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname: str, password: str = None, **extra_fields):
        nickname = self._norm(nickname)

        # MUHIM: avval mavjud bo'lsa olib, yo'q bo'lsa yaratamiz
        user, created = self.get_or_create(nickname=nickname, defaults=extra_fields)

        # Har doim superuser flaglarini to'g'rilab qo'yamiz
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        if password:
            user.set_password(password)

        user.save()
        return user



class FaceStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    APPROVED = "APPROVED", "APPROVED"
    REJECTED = "REJECTED", "REJECTED"


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=32, unique=True, db_index=True)

    # Kontaktlar (ixtiyoriy, registratsiyada bittasi majburiy)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)

    telegram_chat_id = models.BigIntegerField(blank=True, null=True, unique=True)
    
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    face_status = models.CharField(
        max_length=16,
        choices=FaceStatus.choices,
        default=FaceStatus.PENDING,
        db_index=True,
    )

    is_active = models.BooleanField(default=False)  # OTP tasdiqlangandan keyin True
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "nickname"
    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=["nickname"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["face_status"]),
        ]

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if self.nickname:
            self.nickname = self.nickname.strip().lower()
        super().save(*args, **kwargs)
    @property
    def contact_verified(self) -> bool:
        return bool(self.phone_verified or self.email_verified)
