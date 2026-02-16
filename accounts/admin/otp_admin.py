from django.contrib import admin
from accounts.models import  OTPVerification

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "channel", "destination", "expires_at", "used_at", "attempts", "created_at")
    list_filter = ("channel",)
    search_fields = ("destination", "user__nickname")
    readonly_fields = ("code_hash", "created_at", "used_at", "attempts", "expires_at", "destination", "channel", "user")

