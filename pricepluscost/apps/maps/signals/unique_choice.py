from django.db.models.signals import pre_save
from django.dispatch import receiver
from maps.models import ManufacturerMap, ModelMap

'''
Prior to an update, wipe all other choices (to keep only one choice)
'''  

@receiver(pre_save, sender=ModelMap)
def unique_model_choice(sender, instance, **kwargs):
    choice = instance.map_choice
    model = instance.product

    if choice:
        mapped = ModelMap.objects.filter(product=model, map_choice=True)
        
        if mapped:
            mapped.update(map_choice=False)
