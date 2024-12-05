from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from InvestAssistant.instruments.forms import CreateInstrumentForm, DeleteInstrumentForm, EditInstrumentForm
from InvestAssistant.instruments.models import Instrument
from InvestAssistant.mixins import ReadOnlyMixin


class InstrumentListView(ListView):
    model = Instrument
    template_name = 'main/../../templates/instruments/instruments.html'
    paginate_by = 12
    context_object_name = 'instruments'


class CreateInstrumentView(CreateView):
    model = Instrument
    form_class = CreateInstrumentForm
    template_name = 'instruments/create-instrument.html'
    success_url = reverse_lazy('instruments')


class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = 'instruments/details-instrument.html'
    context_object_name = 'instrument'


class InstrumentEditView(UpdateView):
    model = Instrument
    form_class = EditInstrumentForm
    template_name = 'instruments/edit-instrument.html'
    context_object_name = 'instrument'

    def get_success_url(self):
        return reverse_lazy('details-instrument', kwargs={'pk': self.object.pk})


class InstrumentDeleteView(DeleteView):
    model = Instrument
    # form_class = DeleteInstrumentForm
    template_name = 'instruments/delete-instrument.html'
    success_url = reverse_lazy('instruments')

