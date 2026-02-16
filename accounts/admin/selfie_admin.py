from django.contrib import admin
from accounts.models import  VerificationSelfie

@admin.register(VerificationSelfie)
class VerificationSelfieAdmin(admin.ModelAdmin):
    list_display = ("user", "uploaded_at")
    search_fields = ("user__nickname",)
    readonly_fields = ("uploaded_at",)
