from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from maps.models import ManufacturerMap, ModelMap

@receiver(post_save, sender=ManufacturerMap)
@receiver(post_delete, sender=ManufacturerMap)
def update_manufacturer_mapped(sender, instance, **kwargs):
    manufacturer = instance.product_brand
    mapped = ManufacturerMap.objects.filter(product_brand=manufacturer, map_choice=True)

    if mapped:
        manufacturer.is_mapped = True
    else:
        manufacturer.is_mapped = False

    manufacturer.save(update_fields=['is_mapped'])

@receiver(post_save, sender=ModelMap)
@receiver(post_delete, sender=ModelMap)
def update_mapped_model(sender, instance, **kwargs):
    model = instance.product
    mapped = ModelMap.objects.filter(product=model, map_choice=True)

    if mapped:
        model.is_mapped = True
    else:
        model.is_mapped = False

    model.save(update_fields=['is_mapped'])