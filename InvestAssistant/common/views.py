from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from InvestAssistant.common.models import Investment


class HomePage(ListView):
    model = Investment
    success_url = reverse_lazy('')
    template_name = 'home-dashboard.html'

