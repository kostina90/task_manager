from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "department",
            "telegram_id",
            "role",
            "password1",
            "password2",
        )
