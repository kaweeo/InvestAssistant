from django.db.models import Q
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

    def get_queryset(self):
        query_set = super().get_queryset()
        query = self.request.GET.get('q')
        print(f"The obeject is: {query}")

        if query:
            query_set = query_set.filter(
                Q(name__icontains=query) | Q(ticker__icontains=query)
            )
        print(query)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        print(context)
        return context


