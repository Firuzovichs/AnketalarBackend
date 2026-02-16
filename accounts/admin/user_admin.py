
from django.contrib import admin,messages
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nickname",
        "email",
        "phone",
        "is_active",
        "is_staff",
        "face_status",
        "telegram_chat_id",
        "email_verified",
        "phone_verified",
    )
    list_filter = ("is_active", "is_staff", "face_status")
    search_fields = ("nickname", "email", "phone")
    ordering = ("-id",)
    
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        ("Main", {"fields": ("nickname", "password")}),
        ("Contacts", {"fields": ("email", "phone", "telegram_chat_id")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser", "face_status")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    actions = ["approve_face", "reject_face"]

    @admin.action(description="Approve face (set face_status=APPROVED)")
    def approve_face(self, request, queryset):
        updated = queryset.update(face_status="APPROVED")
        self.message_user(request, f"Approved: {updated} user(s).", level=messages.SUCCESS)

    @admin.action(description="Reject face (set face_status=REJECTED)")
    def reject_face(self, request, queryset):
        updated = queryset.update(face_status="REJECTED")
        self.message_user(request, f"Rejected: {updated} user(s).", level=messages.WARNING)
