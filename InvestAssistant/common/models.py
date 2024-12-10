from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from InvestAssistant.accounts.models import Profile
from InvestAssistant.instruments.models import Instrument
from django.db.models.signals import post_save
from django.dispatch import receiver
from InvestAssistant.transactions.models import Transaction


@receiver(post_save, sender=Transaction)
def update_investment(sender, instance, created, **kwargs):
    if not created:  # Only handle new transactions
        return

    profile = instance.profile
    instrument = instance.instrument
    quantity = instance.quantity
    price_per_unit = instance.price_per_unit

    investment, created = Investment.objects.get_or_create(
        profile=profile,
        instrument=instrument,
    )

    if instance.transaction_side == Transaction.BUY:
        # Update avg_price and total_quantity for BUY
        if investment.total_quantity == 0:
            new_total_cost = quantity * price_per_unit
        else:
            total_cost = investment.total_quantity * investment.avg_price
            new_total_cost = total_cost + (quantity * price_per_unit)

        new_total_quantity = investment.total_quantity + quantity
        investment.avg_price = new_total_cost / new_total_quantity
        investment.total_quantity = new_total_quantity
        investment.save()

    elif instance.transaction_side == Transaction.SELL:
        # Reduce total_quantity for SELL
        if investment.total_quantity < quantity:
            raise ValueError("Insufficient quantity to sell.")

        investment.total_quantity -= quantity

        if investment.total_quantity == 0:
            investment.delete()
        else:
            investment.save()


class Investment(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='investments'
    )

    instrument = models.ForeignKey(
        to=Instrument,
        on_delete=models.CASCADE,
        related_name='instruments'
    )

    total_quantity = models.DecimalField(
        max_digits=16,
        decimal_places=6,
        default=Decimal(0),
    )

    avg_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=Decimal(0),
    )

    def clean(self):
        if self.total_quantity < 0:
            raise ValidationError("Total quantity cannot be negative.")
        if self.avg_price < 0:
            raise ValidationError("Average price cannot be negative.")

    def calculate_cost_basis(self):
        return round(self.total_quantity * self.avg_price, 2)

    def calculate_market_value(self):
        return round(self.total_quantity * self.instrument.current_price, 2)

    def calculate_unrealized_pnl(self):
        return round(self.calculate_market_value() - self.calculate_cost_basis(), 2)

    def calculate_current_roi(self):
        if self.calculate_cost_basis() == 0:
            return Decimal(0)

        return round((self.calculate_unrealized_pnl() / self.calculate_cost_basis()) * 100, 2)

    def __str__(self):
        return f"{self.profile.full_name} owns {self.total_quantity} of {self.instrument.name}"
