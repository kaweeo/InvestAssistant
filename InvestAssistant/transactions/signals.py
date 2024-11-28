from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from InvestAssistant.transactions.models import CashTransaction, Transaction


@receiver(post_save, sender=CashTransaction)
def update_profile_balance_on_cash_transaction(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_flow == CashTransaction.DEPOSIT:
            instance.profile.balance += instance.amount
        elif instance.transaction_flow == CashTransaction.WITHDRAWAL:
            if instance.profile.balance >= instance.amount:
                instance.profile.balance -= instance.amount
            else:
                raise ValueError("Insufficient funds for withdrawal.")

        instance.profile.save()


@receiver(post_save, sender=Transaction)
def update_profile_balance_on_investment_transaction(sender, instance, created, **kwargs):
    if created:
        transaction_value = instance.calculate_transaction_value()

        if instance.transaction_side == Transaction.BUY:
            if instance.profile.balance >= transaction_value:
                instance.profile.balance -= transaction_value
            else:
                raise ValueError("Insufficient funds for this transaction.")
        elif instance.transaction_side == Transaction.SELL:
            instance.profile.balance += transaction_value

        instance.profile.save()


@receiver(pre_delete, sender=CashTransaction)
def rollback_profile_balance_on_cash_transaction_delete(sender, instance, **kwargs):
    if instance.transaction_flow == CashTransaction.DEPOSIT:
        instance.profile.balance -= instance.amount
    elif instance.transaction_flow == CashTransaction.WITHDRAWAL:
        instance.profile.balance += instance.amount

    instance.profile.save()


@receiver(pre_delete, sender=Transaction)
def rollback_profile_balance_on_transaction_delete(sender, instance, **kwargs):
    transaction_value = instance.calculate_transaction_value()
    if instance.transaction_side == Transaction.BUY:
        instance.profile.balance += transaction_value
    elif instance.transaction_side == Transaction.SELL:
        instance.profile.balance -= transaction_value

    instance.profile.save()
