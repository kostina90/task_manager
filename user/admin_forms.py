from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User


class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "department", "telegram_id", "role", "avatars")


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "telegram_id",
            "department",
            "role",
            "avatars",
            "is_active"
        )
