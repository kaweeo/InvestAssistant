from django.db.models.signals import post_save
from django.dispatch import receiver
from InvestAssistant.common.models import Investment
from InvestAssistant.transactions.models import Transaction


@receiver(post_save, sender=Transaction)
def update_investment(sender, instance, created, **kwargs):
    if not created:  # Only handle new transactions
        return

    print(f"Signal triggered for transaction: {instance}")

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