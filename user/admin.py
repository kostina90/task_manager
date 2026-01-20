from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "telegram_id", "role", "is_staff")
    list_display_links = ("id", "username")
    list_filter = ("role", "is_staff")
    search_fields = ("username", "email")

    fieldsets = (
        (None, {
            "fields": ("username", "telegram_id", "role", "is_staff"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "telegram_id", "password1", "password2", "role")
        }),
    )
