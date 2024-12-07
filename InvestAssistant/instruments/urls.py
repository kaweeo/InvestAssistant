from django.urls import path, include
from InvestAssistant.instruments import views
from InvestAssistant.instruments.views import InstrumentsListView

urlpatterns = [
    path('', InstrumentsListView.as_view(), name='instruments'),
    path('create/', views.CreateInstrumentView.as_view(), name='create-instrument'),
    path('details/<int:pk>/', views.InstrumentDetailView.as_view(), name='details-instrument'),
    path('edit/<int:pk>/', views.InstrumentEditView.as_view(), name='edit-instrument'),
    path('delete/<int:pk>/', views.InstrumentDeleteView.as_view(), name='delete-instrument'),
]
