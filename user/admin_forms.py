from django import forms
from django.contrib.auth.forms import UserCreationForm

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
