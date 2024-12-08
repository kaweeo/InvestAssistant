from django.urls import path, include
from InvestAssistant.accounts.views import AppUserRegisterView, AppUserLoginView, AppUserLogoutView, ProfileDetailView, \
    ProfileEditView, ProfileDeleteView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', AppUserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete'),

    ]))
]
