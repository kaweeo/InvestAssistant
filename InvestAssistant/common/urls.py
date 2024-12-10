from django.urls import path
from InvestAssistant.common.models import Investment
from InvestAssistant.common.views import create_investment, Portfolio

urlpatterns = [
    path('investment/', create_investment, name='buy-investment'),
     path('portfolio/', Portfolio.as_view(), name='portfolio'),
#     path('edit/<int:pk>/', InstrumentEditView.as_view(), name='edit-instrument'),
#     path('delete/<int:pk>/', InstrumentDeleteView.as_view(), name='delete-instrument'),
]
