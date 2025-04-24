from django.conf import settings

def currency_processor(request):
    """
    Context processor that adds the DEFAULT_CURRENCY to the context
    of all templates.
    """
    return {
        'DEFAULT_CURRENCY': settings.DEFAULT_CURRENCY,
    } 