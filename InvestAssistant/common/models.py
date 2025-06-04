from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from InvestAssistant.accounts.models import Profile
from InvestAssistant.instruments.models import Instrument
from functools import cached_property


class Investment(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_quantity__gte=0),
                name='investment_quantity_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(avg_price__gte=0),
                name='investment_price_non_negative'
            ),
        ]

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='investments',
    )

    instrument = models.ForeignKey(
        to=Instrument,
        on_delete=models.CASCADE,
        related_name='investment_instances',
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

    # @cached_property
    # Keep @cached_property if calculate_market_value is accessed multiple times per request and instrument.current_price is stable during a request cycle.
    # Switch to @property if current_price changes frequently or cache staleness is a concern, as it ensures fresh calculations:
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
 
