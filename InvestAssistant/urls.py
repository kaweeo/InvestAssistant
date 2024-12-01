from operator import index

from django.contrib import admin
from django.template.context_processors import request
from django.urls import path, include

import InvestAssistant
from InvestAssistant.common import views
from InvestAssistant.common.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('accounts/', include('InvestAssistant.accounts.urls')),
    path('transactions/', include('InvestAssistant.transactions.urls')),
    # path('instruments/', include('instruments.urls')),
    # path('investments/', include('investments.urls')),
]
