from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from InvestAssistant.accounts.forms import AppUserRegistrationForm, CustomAuthenticationForm, ProfileEditForm
from InvestAssistant.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)

        return result


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')


class AppUserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class ProfileDetailView(DetailView):  # LoginRequiredMixin
    model = UserModel
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()  # Get the UserModel instance
        # Explicitly fetch the profile to ensure it's accessible
        profile = get_object_or_404(Profile, user=user)
        context['user'] = user
        context['profile'] = profile

        return context


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.user.pk})

    def get_object(self, queryset=None):
        return Profile.objects.get(user__pk=self.kwargs['pk'])

    def form_valid(self, form):
        response = super().form_valid(form)

        return response


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user
