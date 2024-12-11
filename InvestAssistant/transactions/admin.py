from django.contrib import admin
from InvestAssistant.transactions.models import Transaction, CashTransaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'instrument', 'transaction_side',
                    'quantity', 'price_per_unit', 'profile')


@admin.register(CashTransaction)
class CashTransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'transaction_flow', 'amount', 'profile')
