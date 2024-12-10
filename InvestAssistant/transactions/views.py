from django.shortcuts import render
from django.views.generic import ListView
from InvestAssistant.transactions.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = 'common/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        print(f"Logged-in user: {self.request.user}")
        print(f"User's profile: {getattr(self.request.user, 'profile', None)}")
        print(Transaction.objects.filter(profile=self.request.user.profile))
        return Transaction.objects.filter(profile=self.request.user.profile)

