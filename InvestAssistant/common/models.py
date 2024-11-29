from decimal import Decimal
from django.db import models
from InvestAssistant.accounts.models import Profile
from InvestAssistant.instruments.models import Instrument


class Investment(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='investments'
    )

    instrument = models.ForeignKey(
        to=Instrument,
        on_delete=models.CASCADE,
        related_name='investments'
    )

    total_quantity = models.DecimalField(
        max_digits=16,
        decimal_places=6
    )

    avg_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
    )

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
