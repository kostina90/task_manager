from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "department", "telegram_id", "role", "avatars")

    def save(self, commit=True):
        user = super().save(commit=False)

        # технический пароль = telegram_id
        user.set_password(str(user.telegram_id))

        if commit:
            user.save()

        return user


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
