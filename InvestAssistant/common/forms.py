from django import forms
from InvestAssistant.accounts.models import Profile
from InvestAssistant.transactions.models import Transaction

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['instrument', 'quantity', 'price_per_unit']
        widgets = {
            'profile': forms.HiddenInput()
        }

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.HiddenInput()
    )


