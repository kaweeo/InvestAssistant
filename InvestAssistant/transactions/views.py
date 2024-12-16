from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from InvestAssistant.accounts.models import Profile
from InvestAssistant.transactions.forms import CashTransactionForm
from InvestAssistant.transactions.models import Transaction, CashTransaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transactions.html'
    context_object_name = 'transactions'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_queryset(self):
        return Transaction.objects \
            .filter(profile=self.request.user.profile) \
            .order_by('-timestamp')


@login_required
def cash_transaction_list(request):
    return render(request, 'transactions/cash-transactions.html', {
        'transactions': request.user.profile.cash_transactions.order_by('-timestamp'),
        'total_balance': request.user.profile.balance
    })


@login_required
def cash_transaction_view(request, transaction_type):
    if request.method == "POST":
        form = CashTransactionForm(request.POST)
        profile = request.user.profile

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.profile = profile
            transaction.transaction_flow = transaction_type
            transaction.save()

            return redirect('cash-transactions')

    else:
        form = CashTransactionForm()

    return render(request, 'transactions/cash-transaction-form.html', {  # Adjusted template path
        'form': form,
        'transaction_type': transaction_type,
    })
