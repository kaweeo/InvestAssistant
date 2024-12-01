from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from InvestAssistant.common.models import Investment
from InvestAssistant.utils import get_user_object



# class HomePage(ListView):
#     model = Investment
#     success_url = reverse_lazy('')
#     template_name = 'home/index.html'

def home_page(request):
    return render(request, 'home-dashboard.html')