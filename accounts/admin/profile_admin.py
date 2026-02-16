from django.contrib import admin
from django.utils.html import format_html

from accounts.models import UserProfile, UserPhoto
from .mixins import MapLinkMixin, ImagePreviewMixin

class UserPhotoInline(admin.TabularInline, ImagePreviewMixin):
    model = UserPhoto
    extra = 0
    fields = ("preview", "image", "is_main", "order", "created_at")
    readonly_fields = ("preview", "created_at")
    ordering = ("-is_main", "order", "-created_at")

    def preview(self, obj):
        if not obj.pk or not obj.image:
            return "-"
        return self.img(obj.image.url, h=44)
    preview.short_description = "Preview"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin, MapLinkMixin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "gender",
        "birth_date",
        "birth_region",
        "birth_district",
        "height_cm",
        "weight_kg",
        "smoking",
        "has_main_photo",
        "location_link",
        "updated_at",
    )

    list_filter = (
        "gender",
        "smoking",
        "birth_region",
        "updated_at",
    )

    search_fields = (
        "user__nickname",
        "user__email",
        "user__phone",
        "first_name",
        "last_name",
    )

    ordering = ("-updated_at",)
    autocomplete_fields = ("user", "birth_region", "birth_district")
    filter_horizontal = ("interests", "purposes")
    

    readonly_fields = ("created_at", "updated_at", "location_link")

    fieldsets = (
        ("User", {"fields": ("user",)}),
        ("Required profile", {
            "fields": (
                ("first_name", "last_name"),
                ("birth_date", "gender"),
                ("birth_region", "birth_district"),
                ("height_cm", "weight_kg"),
                ("interests", "purposes"),
            )
        }),
        ("About & links", {
            "fields": ("bio", "telegram_link", "instagram_link", "tiktok_link", "smoking")
        }),
        ("Location (lat/lon)", {
            "fields": ("latitude", "longitude", "location_link")
        }),
        ("Meta", {"fields": ("created_at", "updated_at")}),
    )

    def has_main_photo(self, obj):
        return obj.user.photos.filter(is_main=True).exists()
    has_main_photo.boolean = True
    has_main_photo.short_description = "Main photo"

    def location_link(self, obj):
        return self.map_link(obj.latitude, obj.longitude)
    location_link.short_description = "Map"
