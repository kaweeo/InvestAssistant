from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from InvestAssistant.accounts.models import Profile
from InvestAssistant.common.forms import CreateTransactionForm
from InvestAssistant.common.models import Investment
from InvestAssistant.instruments.models import Instrument
from InvestAssistant.transactions.models import Transaction
from django.contrib.auth import get_user_model


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


# class CreateInvestmentView(CreateView):
#     form_class = CreateTransactionForm
#     template_name = 'common/investment.html'
#     success_url = reverse_lazy('home-dashboard')
#
#     def form_valid(self, form):
#         investment = form.save(commit=False)
#         investment.profile = self.request.user.profile
#         investment.save()
#         return super().form_valid(form)



@login_required
def create_investment(request):
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            try:
                # Save transaction with the logged-in user's profile
                investment = form.save(commit=False)
                investment.profile = request.user.profile  # Link the profile
                investment.save()  # Save to the database
                return redirect('/')  # Redirect after success

            except Exception as e:
                form.add_error(None, f"Error saving investment: {str(e)}")  # Catch and show errors
    else:
        form = CreateTransactionForm()

    return render(request, 'common/investment.html', {'form': form})