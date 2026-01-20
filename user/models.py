from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_from_telegram(self, username: str, telegram_id: int):
        if not username:
            raise ValueError("The username must be set")
        if not telegram_id:
            raise ValueError("The telegram_id must be set")
        
        user, created = self.get_or_create(
            username=username,
            defaults={"telegram_id": telegram_id}
        )

        user.telegram_id = telegram_id
        user.set_password(str(telegram_id))
        user.save()

        return user


class User(AbstractUser):

    ROLE_ADMIN = "admin"
    ROLE_DEVELOPER = "developer"
    ROLE_IT = "it"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_DEVELOPER, "Developer"),
        (ROLE_IT, "IT Specialist"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_IT,
    )

    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID"
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name="Avatar",
        default='avatars/o_litters.png'
    )

    @property
    def is_admin(self):
        return self.role == User.ROLE_ADMIN
    
    @property
    def is_developer(self):
        return self.role == User.ROLE_DEVELOPER
    
    objects = UserManager()

    class Meta:
        ordering = ["username",]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username