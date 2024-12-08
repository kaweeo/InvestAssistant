from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from InvestAssistant.accounts.models import Profile, AppUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from InvestAssistant.accounts.models import AppUser


class AppUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Create a password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = AppUser
        fields = ('email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address'
        }),
        help_text="Enter your email address to log in."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        }),
        help_text="Enter your password to access your account."
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First Name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name'}
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Phone Number'}
            ),
        }

# class AppUserChangePassword(PasswordChangeForm):
#     old_password = forms.CharField(
#         label='',
#         widget=forms.PasswordInput(
#             attrs={
#                 "autocomplete": "current-password",
#                 'placeholder': 'Enter your old password',
#                 'style': "height: 55px",
#             }
#         ),
#     )
#     new_password1 = forms.CharField(
#         label='',
#         widget=forms.PasswordInput(attrs={
#             "autocomplete": "new-password",
#             'placeholder': 'Enter your new password',
#             'style': "height: 55px",
#         }
#         ),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label='',
#         widget=forms.PasswordInput(
#             attrs={
#                 "autocomplete": "new-password",
#                 'placeholder': 'New password confirmation',
#                 'style': "height: 55px",
#             }
#         ),
#     )
