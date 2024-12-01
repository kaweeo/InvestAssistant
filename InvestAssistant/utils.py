from InvestAssistant.accounts.models import Profile


def get_user_object():
    user_object = Profile.objects.first()
    return user_object