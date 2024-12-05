from django import forms

from InvestAssistant.instruments.models import Instrument
from InvestAssistant.mixins import PlaceholderMixin, ReadOnlyMixin


class BaseInstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'

# class CreateInstrumentForm(BaseInstrumentForm):
#     widgets = {
#         'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
#         'ticker': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
#         'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
#         'category': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
#     }

class CreateInstrumentForm(PlaceholderMixin, BaseInstrumentForm):
    pass

class EditInstrumentForm(PlaceholderMixin, BaseInstrumentForm):
    # BaseInstrumentForm.Meta.exclude = ('ticker',)
    pass

class DeleteInstrumentForm(ReadOnlyMixin, PlaceholderMixin, BaseInstrumentForm):
    read_only_fields = '__all__'