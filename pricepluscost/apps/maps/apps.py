from django.apps import AppConfig

class MapsConfig(AppConfig):
    name = 'maps'
    verbose_name = 'Mappings'
    
    def ready(self):
        from maps.signals import status_updates, unique_choice, autogenerate
