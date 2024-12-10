from django import forms
from InvestAssistant.transactions.models import Transaction


class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['instrument', 'transaction_side', 'quantity', 'price_per_unit',]
