from django.views.generic import ListView
from InvestAssistant.transactions.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = 'common/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(profile=self.request.user.profile)
