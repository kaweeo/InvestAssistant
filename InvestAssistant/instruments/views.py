from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from InvestAssistant.instruments.models import Instrument


class InstrumentListView(ListView):
    model = Instrument
    template_name = 'main/instruments.html'
    paginate_by = 1

    # context_data = Instrument.objects.all()
    context_object_name = 'instruments'