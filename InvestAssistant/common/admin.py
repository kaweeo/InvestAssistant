from django.contrib import admin
from InvestAssistant.common.models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    model = Investment
    list_display = ('pk', 'profile', 'instrument', 'total_quantity', 'avg_price')
    list_filter = ('profile', 'instrument')
    list_select_related = ('profile', 'instrument')
