from django.db.models.signals import post_save
from django.dispatch import receiver
from maps.models import ManufacturerMap, ModelMap

@receiver(post_save, sender=ManufacturerMap)
def update_manufacturer_mapped(sender, instance, **kwargs):
    manufacturer = instance.manufacturer
    mapped = ManufacturerMap.objects.filter(manufacturer=manufacturer, map_choice=True)

    if mapped:
        manufacturer.is_mapped = True
    else:
        manufacturer.is_mapped = False

    manufacturer.save(update_fields=['is_mapped'])

@receiver(post_save, sender=ModelMap)
def update_mapped_model(sender, instance, **kwargs):
    model = instance.product_model
    mapped = ModelMap.objects.filter(product_model=model, map_choice=True)

    if mapped:
        model.is_mapped = True
    else:
        model.is_mapped = False

    model.save(update_fields=['is_mapped'])