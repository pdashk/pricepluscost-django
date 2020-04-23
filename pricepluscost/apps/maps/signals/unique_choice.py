from django.db.models.signals import pre_save
from django.dispatch import receiver
from maps.models import ManufacturerMap, ModelMap

'''
Prior to an update, wipe all other choices (to keep only one choice)
Also needs to update `is_primary` field for manufacturer when this occurs.
Does this by iterating through all the maps that have been wiped and checks if there are still mappings (expensive)
'''
@receiver(pre_save, sender=ManufacturerMap)
def unique_manufacturer_choice(sender, instance, **kwargs):
    choice = instance.map_choice
    manufacturer = instance.manufacturer

    if choice:
        mapped = ManufacturerMap.objects.filter(manufacturer=manufacturer, map_choice=True)
        
        if mapped:
            mapped.update(map_choice=False)
            

@receiver(pre_save, sender=ModelMap)
def unique_model_choice(sender, instance, **kwargs):
    choice = instance.map_choice
    model = instance.product_model

    if choice:
        mapped = ModelMap.objects.filter(product_model=model, map_choice=True)
        
        if mapped:
            mapped.update(map_choice=False)