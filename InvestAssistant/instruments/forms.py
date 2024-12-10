from django import forms

from InvestAssistant.instruments.models import Instrument
from InvestAssistant.mixins import PlaceholderMixin, ReadOnlyMixin


class BaseInstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'


class CreateInstrumentForm(PlaceholderMixin, BaseInstrumentForm):
    pass


class EditInstrumentForm(PlaceholderMixin, BaseInstrumentForm):
    pass


class DeleteInstrumentForm(ReadOnlyMixin, PlaceholderMixin, BaseInstrumentForm):
    read_only_fields = '__all__'
