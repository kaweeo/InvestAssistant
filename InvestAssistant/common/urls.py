from django.urls import path
from InvestAssistant.common.models import Investment
from InvestAssistant.common.views import create_investment

urlpatterns = [
    path('investment/', create_investment, name='buy-investment'),
#     path('details/<int:pk>/', InstrumentDetailView.as_view(), name='details-instrument'),
#     path('edit/<int:pk>/', InstrumentEditView.as_view(), name='edit-instrument'),
#     path('delete/<int:pk>/', InstrumentDeleteView.as_view(), name='delete-instrument'),
]
