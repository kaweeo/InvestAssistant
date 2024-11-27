from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.timezone import now

from InvestAssistant.accounts.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'app_user'
        app_label = 'accounts'
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'
        # permissions = ()

    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        default=now,
    )

    last_login = models.DateTimeField(
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()
