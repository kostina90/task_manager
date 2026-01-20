from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, telegram_id, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        if not telegram_id:
            raise ValueError("The telegram_id must be set")
        if not password:
            raise ValueError("The password must be set")

        user = self.model(
            username=username,
            telegram_id=telegram_id,
            **extra_fields
        )   

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, telegram_id=None, password=None, **extra_fields):
        return self._create_user(username, telegram_id, password, **extra_fields)

    def create_superuser(self, username, telegram_id=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        return self._create_user(username, telegram_id, password, **extra_fields)

    def create_from_telegram(self, username, telegram_id, **extra_fields):
        user, created = self.get_or_create(
            username=username,
            defaults={
                "telegram_id": telegram_id,
                **extra_fields,
            }
        )

        if not created:
            return user

        user.set_password(str(telegram_id))
        user.save(update_fields=["password"])
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

    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID"
    )

    avatars = models.ImageField(
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

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["telegram_id"]

    class Meta:
        ordering = ["username",]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if self.role == self.ROLE_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
