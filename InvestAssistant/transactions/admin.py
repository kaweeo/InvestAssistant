from django.contrib import admin
from InvestAssistant.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'instrument', 'transaction_side',
                    'quantity', 'price_per_unit', 'profile')
