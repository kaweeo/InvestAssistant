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


@login_required
def create_investment(request):
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            try:
                # Save transaction with the logged-in user's profile
                investment = form.save(commit=False)
                investment.profile = request.user.profile
                investment.save()
                return redirect('/')

            except Exception as e:
                form.add_error(None, f"Error saving investment: {str(e)}")
    else:
        form = CreateTransactionForm()

    return render(request, 'common/investment.html', {'form': form})


class Portfolio(ListView):
    model = Investment
    template_name = 'common/portfolio.html'
    context_object_name = 'investments'
    paginate_by = 6

    def get_queryset(self):
        # Filter investments for the current user's profile
        return Investment.objects.filter(profile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investments = context['investments']

        # Calculate portfolio total
        context['portfolio_total'] = sum(
            investment.calculate_market_value() for investment in investments
        )

        # Calculate total unrealized PNL
        total_unrealized_pnl = sum(
            investment.calculate_unrealized_pnl() for investment in investments
        )
        context['total_unrealized_pnl'] = total_unrealized_pnl

        # Calculate total cost basis
        total_cost_basis = sum(
            investment.calculate_cost_basis() for investment in investments
        )
        context['total_cost_basis'] = total_cost_basis

        # Calculate total ROI
        if total_cost_basis != 0:
            context['total_roi'] = round((total_unrealized_pnl / total_cost_basis) * 100, 2)
        else:
            context['total_roi'] = 0

        return context