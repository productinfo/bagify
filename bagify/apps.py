from django.apps import AppConfig


class BagifyConfig(AppConfig):
    name = 'bagify'
    verbose_name = 'Baggify, a fictious bag store'

    def ready(self):
        from .hooks import PayPalClient
