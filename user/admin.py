from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .admin_forms import AdminUserCreationForm, AdminUserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm

    model = User

    list_display = ("id", "username", "department", "telegram_id", "role")
    list_display_links = ("id", "username")
    list_filter = ("role",)
    exclude = ("is_staff", "is_superuser")
    search_fields = ("username", "=telegram_id", "department")
    per_page = 10

    fieldsets = (
        ("Main info:", {
            "classes": ("wide",),
            "fields": ("username", "department", "telegram_id", "avatars"),
        }),
        ("Additional info", {
            "classes": ("wide",),
            "fields": ("role",),
        }),
    )

    add_fieldsets = (
        ("Main info:", {
            "classes": ("wide",),
            "fields": ("username", "department", "telegram_id", "avatars"),
        }),
        ("Additional info", {
            "classes": ("wide",),
            "fields": ("role",),
        }),
    )
