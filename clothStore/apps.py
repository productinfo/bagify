from django.apps import AppConfig


class ClothstoreConfig(AppConfig):
    name = 'clothStore'
    verbose_name = 'Baggify, a fictious bag store'

    def ready(self):
        from .hooks import show_me_the_money
