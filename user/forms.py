from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "department", "telegram_id", "role")

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(str(user.telegram_id))

        if commit:
            user.save()

        return user
