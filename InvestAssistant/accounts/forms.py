from django import forms
from InvestAssistant.accounts.models import Profile


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

