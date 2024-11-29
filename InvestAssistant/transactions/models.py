from django.core.exceptions import ValidationError
from django.db import models

from InvestAssistant.accounts.models import Profile
from InvestAssistant.instruments.models import Instrument


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
        blank=False,
        null=False,
    )

    instrument = models.ForeignKey(
        to=Instrument,
        on_delete=models.CASCADE,
        related_name='transactions',
        blank=False,
        null=False,
    )

    transaction_side = models.CharField(
        max_length=4,
        choices=TRANSACTION_SIDE_CHOICES,
        blank=False,
        null=False,
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        blank=False,
        null=False,
    )

    price_per_unit = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        blank=False,
        null=False,
        default=0.0,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        # db_index=True
    )

    def calculate_transaction_value(self):
        return self.quantity * self.price_per_unit

    def clean(self):
        transaction_value = self.calculate_transaction_value()
        if self.transaction_side == self.BUY and self.profile.balance < transaction_value:
            raise ValidationError("Insufficient balance for this transaction.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.timestamp} {self.instrument.ticker} {self.transaction_side} {self.quantity} by " \
               f"{self.profile.full_name}, id: {self.profile.user.id}"


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
        decimal_places=2
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        if self.transaction_flow == self.WITHDRAWAL and self.profile.balance < self.amount:
            raise ValidationError("Insufficient balance for withdrawal.")

# TODO: save() with atomic transactions
