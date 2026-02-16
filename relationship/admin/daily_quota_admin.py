from django.contrib import admin
from django.utils import timezone

from relationship.models.daily_quota import DailyQuota


@admin.register(DailyQuota)
class DailyQuotaAdmin(admin.ModelAdmin):
    """
    Kunlik limit monitoring va boshqarish (reset, search, filter).
    """

    list_display = (
        "id",
        "user",
        "date",
        "used",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "date",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__nickname",
        "user__email",
        "user__phone",
    )

    autocomplete_fields = ("user",)
    ordering = ("-date", "-updated_at")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User & Date", {"fields": ("user", "date")}),
        ("Usage", {"fields": ("used",)}),
        ("Meta", {"fields": ("created_at", "updated_at")}),
    )

    actions = [
        "reset_used_to_zero",
        "reset_today_for_selected_users",
        "delete_selected_rows",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")

    @admin.action(description="Reset used=0 for selected rows")
    def reset_used_to_zero(self, request, queryset):
        queryset.update(used=0)

    @admin.action(description="Reset today's quota (used=0) for selected users")
    def reset_today_for_selected_users(self, request, queryset):
        today = timezone.localdate()
        user_ids = queryset.values_list("user_id", flat=True).distinct()
        DailyQuota.objects.filter(user_id__in=user_ids, date=today).update(used=0)

    @admin.action(description="Delete selected rows")
    def delete_selected_rows(self, request, queryset):
        queryset.delete()
