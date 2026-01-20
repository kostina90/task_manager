from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "telegram_id", "role")

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.role == User.ROLE_ADMIN:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "telegram_id",
            "role",
            "avatar",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")

        if role == User.ROLE_ADMIN:
            cleaned_data["is_staff"] = True
            cleaned_data["is_superuser"] = True
        else:
            cleaned_data["is_staff"] = False
            cleaned_data["is_superuser"] = False

        return cleaned_data
