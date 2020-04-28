from django.apps import AppConfig


class PPCConfig(AppConfig):
    name = 'ppc'
    verbose_name = "Pricepluscost"

    def ready(self):
        from ppc.signals import refresh_item
