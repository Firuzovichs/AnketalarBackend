from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q

from relationship.models.relationship import Relationship, RelationStatus


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    """
    Like / Skip / Reject / Match + Comment ma'lumotlarini boshqarish.
    """

    list_display = (
        "id",
        "from_user",
        "to_user",
        "status",
        "has_comment",
        "comment_liked",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "from_user__nickname",
        "from_user__email",
        "from_user__phone",
        "to_user__nickname",
        "to_user__email",
        "to_user__phone",
        "comment",
    )

    autocomplete_fields = ("from_user", "to_user")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Users", {"fields": (("from_user", "to_user"),)}),
        ("State", {"fields": (("status",),)}),
        ("Comment", {"fields": ("comment", "comment_liked_at")}),
        ("Meta", {"fields": ("created_at", "updated_at")}),
    )

    actions = [
        "mark_as_liked",
        "mark_as_skipped",
        "mark_as_rejected",
        "mark_as_matched",
        "clear_comment",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("from_user", "to_user")

    # ======= UI helpers =======
    @admin.display(boolean=True, description="Comment?")
    def has_comment(self, obj: Relationship) -> bool:
        return bool((obj.comment or "").strip())

    @admin.display(boolean=True, description="Comment liked?")
    def comment_liked(self, obj: Relationship) -> bool:
        return obj.comment_liked_at is not None

    # ======= Actions =======
    @admin.action(description="Mark selected as LIKED")
    def mark_as_liked(self, request, queryset):
        queryset.update(status=RelationStatus.LIKED)

    @admin.action(description="Mark selected as SKIPPED")
    def mark_as_skipped(self, request, queryset):
        queryset.update(status=RelationStatus.SKIPPED)

    @admin.action(description="Mark selected as REJECTED")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=RelationStatus.REJECTED)

    @admin.action(description="Mark selected as MATCHED")
    def mark_as_matched(self, request, queryset):
        queryset.update(status=RelationStatus.MATCHED)

    @admin.action(description="Clear comment for selected")
    def clear_comment(self, request, queryset):
        queryset.update(comment="", comment_liked_at=None)
