from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from admincustom.utils.check_language import translate_ru


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError("Users should have a username")

        if password is None:
            raise TypeError("Users should have a password")

        user = self.model(
            username=username,
            email=self.normalize_email(email).lower() if email else None,
            **extra_fields,
        )
        user.set_password(password)
        user.save()

    def create_superuser(self, username, password, **extra_fields):
        email = username + "@" + username + ".com"
        user = self.create_user(
            username,
            email,
            password,
            is_superuser=True,
            is_staff=True,
            is_verified=True,
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name=translate_ru("Username", "Логин"),
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=True,
        null=True,
        verbose_name=translate_ru("Email", "Электронная почта"),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=translate_ru("Is staff", "Персонал")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=translate_ru("Is active", "Активный")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=translate_ru("Is verified", "Верифицированный")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=translate_ru("Created at", "Создан")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=translate_ru("Updated at", "Обновлен")
    )

    objects = UserManager()

    USERNAME_FIELD = "username"

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def __str__(self):
        return f"{str(self.username)} {str(self.email)}"

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["User", "Users"],
            ["Пользователь", "Пользователи"]
        )
