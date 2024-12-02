from django.urls import path, include
from InvestAssistant.instruments import views

urlpatterns = [
    path('', views.InstrumentListView.as_view(), name='instruments'),
    # path('/isnturments/', include([
    #     path('all/', )
    # ])),
]