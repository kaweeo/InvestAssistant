from InvestAssistant.transactions.models import Transaction
from django import forms
from .models import CashTransaction



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class CashTransactionForm(forms.ModelForm):
    class Meta:
        model = CashTransaction
        fields = ['amount', 'transaction_flow']
