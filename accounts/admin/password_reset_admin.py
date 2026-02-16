from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from accounts.models import PasswordReset

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = (
        "id_short",
        "user_link",
        "created_at",
        "expires_at",
        "confirmed_at",
        "used_at",
    )

    list_filter = (
        "created_at",
        "confirmed_at",
        "used_at",
    )

    search_fields = (
        "user__nickname",
        "user__email",
        "user__phone",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "user",
        "otp_id",
        "reset_token",
        "created_at",
        "confirmed_at",
        "used_at",
        "expires_at"
    )

    fieldsets = (
        ("User", {
            "fields": ("user",),
        }),
        ("Reset Info", {
            "fields": (
                "otp_id",
                "reset_token"
            ),
        }),
        ("Dates", {
            "fields": (
                "created_at",
                "expires_at",
                "confirmed_at",
                "used_at",
            ),
        }),
    )

    actions = [
        "mark_used",
        "invalidate_reset",
    ]


    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = "ID"

    def user_link(self, obj):
        return format_html(
            '<a href="/admin/accounts/user/{}/change/">{}</a>',
            obj.user_id,
            obj.user.nickname
        )
    user_link.short_description = "User"

    def status(self, obj):
        if obj.used_at:
            return format_html('<span style="color:red;">USED</span>')
        if obj.confirmed_at:
            return format_html('<span style="color:green;">CONFIRMED</span>')
        if obj.expires_at < timezone.now():
            return format_html('<span style="color:orange;">EXPIRED</span>')
        return format_html('<span style="color:blue;">PENDING</span>')
    status.short_description = "Status"


    @admin.action(description="Mark as USED (invalidate)")
    def mark_used(self, request, queryset):
        updated = queryset.filter(used_at__isnull=True).update(used_at=timezone.now())
        self.message_user(
            request,
            f"{updated} ta reset USED qilindi",
            level=messages.WARNING
        )

    @admin.action(description="Invalidate (expire now)")
    def invalidate_reset(self, request, queryset):
        updated = queryset.update(expires_at=timezone.now())
        self.message_user(
            request,
            f"{updated} ta reset EXPIRED qilindi",
            level=messages.ERROR
        )