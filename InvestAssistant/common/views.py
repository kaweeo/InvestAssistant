from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from InvestAssistant.instruments.models import Instrument


class HomePage(ListView):
    model = Instrument
    success_url = reverse_lazy('')
    template_name = 'home-dashboard.html'
    context_object_name = 'instruments'
    paginate_by = 6