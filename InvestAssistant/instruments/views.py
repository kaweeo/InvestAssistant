from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from InvestAssistant.instruments.forms import CreateInstrumentForm, EditInstrumentForm
from InvestAssistant.instruments.models import Instrument


class InstrumentsListView(ListView):
    model = Instrument
    template_name = 'instruments/instruments.html'
    context_object_name = 'instruments'
    paginate_by = 12

    def get_queryset(self):
        query_set = super().get_queryset()
        query = self.request.GET.get('q')  # Get the search query

        if query:
            query_set = query_set.filter(
                Q(name__icontains=query) | Q(ticker__icontains=query)
            )
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Add the query to the context
        return context


class CreateInstrumentView(LoginRequiredMixin, CreateView):
    model = Instrument
    form_class = CreateInstrumentForm
    template_name = 'instruments/create-instrument.html'
    success_url = reverse_lazy('instruments')


class InstrumentDetailView(LoginRequiredMixin, DetailView):
    model = Instrument
    template_name = 'instruments/details-instrument.html'
    context_object_name = 'instrument'


class InstrumentEditView(LoginRequiredMixin, UpdateView):
    model = Instrument
    form_class = EditInstrumentForm
    template_name = 'instruments/edit-instrument.html'
    context_object_name = 'instrument'

    def get_success_url(self):
        return reverse_lazy('details-instrument', kwargs={'pk': self.object.pk})


class InstrumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Instrument
    template_name = 'instruments/delete-instrument.html'
    success_url = reverse_lazy('instruments')
