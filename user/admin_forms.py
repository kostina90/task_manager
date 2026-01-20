from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "telegram_id", "role", "avatar")

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
            self.instance.is_staff = True
            self.instance.is_superuser = True
        else:
            self.instance.is_staff = False
            self.instance.is_superuser = False
        return cleaned_data
