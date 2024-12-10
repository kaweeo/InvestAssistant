from django.urls import path
from InvestAssistant.transactions.views import TransactionListView

urlpatterns = [
    path('', TransactionListView.as_view(), name='transactions')
]