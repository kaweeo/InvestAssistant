from django.urls import path
from InvestAssistant.transactions.views import TransactionListView, cash_transaction_list, cash_transaction_view

urlpatterns = [
    path('', TransactionListView.as_view(), name='transactions'),
    path('cash/', cash_transaction_list, name='cash-transactions'),

    path('deposit/', cash_transaction_view, {'transaction_type': 'DEPOSIT'}, name='deposit'),
    path('withdrawal/', cash_transaction_view, {'transaction_type': 'WITHDRAWAL'}, name='withdrawal'),

]
