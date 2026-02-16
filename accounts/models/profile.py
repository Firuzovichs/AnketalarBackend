from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from .location import Region, District
from .interest import Interest
from .purpose import Purpose

class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"

class SmokingStatus(models.TextChoices):
    NO = "NO", "I don't smoke"
    YES = "YES", "I smoke"
    SOMETIMES = "SOMETIMES", "Sometimes"


class UserProfile(models.Model):
    # User modeli sizda allaqachon bor (accounts/models/user.py)
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="profile")

    # Majburiy
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)

    birth_region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="born_profiles")
    birth_district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="born_profiles")

    height_cm = models.PositiveSmallIntegerField(validators=[MinValueValidator(120), MaxValueValidator(230)])
    weight_kg = models.PositiveSmallIntegerField(validators=[MinValueValidator(35), MaxValueValidator(250)])

    interests = models.ManyToManyField(Interest, related_name="profiles", blank=False)
    purposes = models.ManyToManyField(Purpose, related_name="profiles", blank=False)

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        validators=[MinValueValidator(Decimal("-90")), MaxValueValidator(Decimal("90"))],
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        validators=[MinValueValidator(Decimal("-180")), MaxValueValidator(Decimal("180"))],
    )

    # Ixtiyoriy
    bio = models.TextField(blank=True)
    telegram_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    tiktok_link = models.URLField(blank=True)
    smoking = models.CharField(max_length=12, choices=SmokingStatus.choices, default=SmokingStatus.NO)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["gender"]),
            models.Index(fields=["birth_region", "birth_district"]),
        ]

    def clean(self):
        # Tug'ilgan joy select logikasi: district regionga mos bo'lishi shart
        if self.birth_district_id and self.birth_region_id:
            if self.birth_district.region_id != self.birth_region_id:
                raise ValidationError({"birth_district": "District tanlangan regionga tegishli emas."})

    @property
    def main_photo(self):
        # UserPhoto modelini quyida beraman
        return self.user.photos.filter(is_main=True).first()

    @property
    def is_profile_complete(self) -> bool:
        """
        Minimal talab: majburiy fieldlar + kamida 1 ta interest + 1 ta purpose + 1 ta main photo.
        """
        if not self.first_name or not self.last_name or not self.birth_date or not self.gender:
            return False
        if not self.birth_region_id or not self.birth_district_id:
            return False
        if not self.height_cm or not self.weight_kg:
            return False
        if not self.interests.exists():
            return False
        if not self.purposes.exists():
            return False
        if not self.main_photo:
            return False
        return True

    def __str__(self):
        return f"{self.user.nickname} profile"
