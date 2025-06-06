from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Sum, F
from InvestAssistant.accounts.models.app_user import AppUser
from InvestAssistant.accounts.validators import NameValidator, BasicPhoneNumberValidator


class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

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
        validators=(BasicPhoneNumberValidator,),
        null=True,
        blank=True,
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    @property
    def portfolio_value(self):
        return sum(investment.calculate_market_value() for investment in self.investments.all())

    @property
    def portfolio_cost_basis(self):
        return sum(investment.calculate_cost_basis() for investment in self.investments.all())

    @property
    def total_unrealized_pnl(self):
        return self.portfolio_value - self.portfolio_cost_basis

    @property
    def total_roi(self):
        cost_basis = self.portfolio_cost_basis
        if cost_basis == 0:
            return 0
        return round((self.total_unrealized_pnl / cost_basis) * 100, 2)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return 'Anonymous'

    def __str__(self):
        return f'{self.full_name} ({self.user.email})'
