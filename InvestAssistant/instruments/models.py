from django.db import models


class Instrument(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Instrument'
        verbose_name_plural = 'Instruments'
        indexes = [
            models.Index(fields=['ticker']),
            models.Index(fields=['type']),
        ]

    TYPE_CHOICES = [  # Can use shortnames for DB optimization on production
        ("SECURITY", "Security"),
        ("ETF", "ETF"),
        ("REAL_ESTATE", "Real Estate"),
        ("CRYPTO", "Crypto Currency"),
    ]

    name = models.CharField(
        max_length=100,
        help_text="The name of the investment instrument (e.g., Apple, Bitcoin, Vanguard ETF)."
    )

    ticker = models.CharField(
        max_length=10,
        unique=True,
        help_text="The unique ticker symbol of the instrument.",
        blank=True,
        null=True,
    )

    current_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        help_text="The current market price per unit of the instrument.",
        default=0.0,
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="The sector or type of instrument (e.g., Security, ETF, Real Estate, Crypto)."
    )

    def __str__(self):
        return f"{self.name} ({self.ticker}, {self.type})"
