from django.contrib import admin
from django.utils.html import format_html
from accounts.models import UserPhoto
from .mixins import ImagePreviewMixin

@admin.register(UserPhoto)
class UserPhotoAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("id", "user", "thumb", "is_main", "order", "created_at")
    list_filter = ("is_main", "created_at")
    search_fields = ("user__nickname", "user__email", "user__phone")
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)

    def thumb(self, obj):
        if not obj.image:
            return "-"
        return self.img(obj.image.url, h=44)
    thumb.short_description = "Photo"
