from django.core.validators import MinLengthValidator
from django.db import models
from InvestAssistant.accounts.models.app_user import AppUser
from InvestAssistant.accounts.validators import NameValidator, BasicPhoneNumberValidator


class Profile(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 20
    MAX_PHONE_LENGTH = 15

    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            NameValidator,
        ),
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            NameValidator,
        ),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        validators=(
            BasicPhoneNumberValidator,
        ),
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return 'Anonymous'

    def __str__(self):
        return f'{self.full_name} ({self.user.email})'
