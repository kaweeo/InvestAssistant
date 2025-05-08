from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from InvestAssistant.accounts.forms import AppUserRegistrationForm, CustomAuthenticationForm, ProfileEditForm
from InvestAssistant.accounts.models import Profile, AppUser

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


class AppUserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = get_object_or_404(AppUser, pk=self.kwargs['pk'])
        if user != self.request.user:
            raise PermissionDenied("You are not authorized to view this profile.")

        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        context['user'] = user
        context['profile'] = profile

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.user.pk})

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, user__pk=self.kwargs['pk'])
        if profile.user != self.request.user:
            raise PermissionDenied("You are not authorized to edit this profile.")

        return profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your form. Please correct them.")
        return super().form_invalid(form)


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

# Might rework to use User-Based URLs - removing pk from urls
