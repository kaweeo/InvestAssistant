from django.contrib import admin
from InvestAssistant.instruments.models import Instrument


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'ticker', 'current_price')
    search_fields = ('ticker',)
    list_editable = ('current_price',)