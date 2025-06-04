from django.db import models
from django.core.exceptions import ValidationError
from InvestAssistant.accounts.models import Profile
from InvestAssistant.instruments.models import Instrument
from django.conf import settings
from django.core.validators import MinValueValidator

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'

    TRANSACTION_SIDE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    instrument = models.ForeignKey(
        to=Instrument,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    transaction_side = models.CharField(
        max_length=4,
        choices=TRANSACTION_SIDE_CHOICES,
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        validators=[
            MinValueValidator(0.00),
        ],
    )
    price_per_unit = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        validators=[
            MinValueValidator(0.00),
        ],
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        if self.quantity is None:
            raise ValidationError({"quantity": "Transaction quantity is required."})
        if self.quantity <= 0:
            raise ValidationError({"quantity": "Transaction quantity must be greater than zero."})

    def calculate_transaction_value(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.timestamp}: {self.transaction_side} {self.quantity} {self.instrument.name} by {self.profile.full_name}"


class CashTransaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'

    CASH_TRANSACTION_FLOW_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='cash_transactions'
    )

    transaction_flow = models.CharField(
        max_length=10,
        choices=CASH_TRANSACTION_FLOW_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
        ],
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.timestamp}: {self.transaction_flow} {settings.DEFAULT_CURRENCY}{self.amount} by {self.profile.full_name}"
