from django.apps import AppConfig

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InvestAssistant.common'

    def ready(self):
        import InvestAssistant.common.signals