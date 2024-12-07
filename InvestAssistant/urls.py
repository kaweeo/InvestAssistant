from django.contrib import admin
from django.urls import path, include
from InvestAssistant.common import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('InvestAssistant.accounts.urls')),
    path('transactions/', include('InvestAssistant.transactions.urls')),
    path('instruments/', include('InvestAssistant.instruments.urls')),
]
