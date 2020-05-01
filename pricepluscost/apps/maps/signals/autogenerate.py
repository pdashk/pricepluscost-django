from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from maps.models import ReferenceManufacturer, ReferenceModel

# Will need to add receiver for each reference source

import ccms.models as ccms

@receiver(post_save, sender=ccms.BrandName)
def autogenerate_manufacturer(sender, instance, **kwargs):
    manufacturer_class = ContentType.objects.get_for_model(instance)
    manufacturer_id = instance.id
    obj, created = ReferenceManufacturer.objects.get_or_create(manufacturer_class=manufacturer_class, manufacturer_id=manufacturer_id)

@receiver(post_save, sender=ccms.Model)
def autogenerate_model(sender, instance, **kwargs):
    model_class = ContentType.objects.get_for_model(instance)
    model_id = instance.id
    obj, created = ReferenceModel.objects.get_or_create(model_class=model_class, model_id=model_id)