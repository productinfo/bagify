from django.apps import AppConfig


class BagifyConfig(AppConfig):
    name = 'bagify'
    verbose_name = 'Baggify, a fictious bag store'

    def ready(self):
        from .hooks import show_me_the_money
