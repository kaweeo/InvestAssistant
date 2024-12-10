from django.urls import path
from InvestAssistant.common.views import create_investment, sell_investment, Portfolio

urlpatterns = [
    path('investment/', create_investment, name='buy-investment'),
    path('sell-investment/', sell_investment, name='sell-investment'),
     path('portfolio/', Portfolio.as_view(), name='portfolio'),
]
