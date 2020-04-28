from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import bestbuy.models as bb

'''
Refreshes the ppc item when the source is changed. 
Exception will be raised if new values do not meet ppc item validations, but only after source is allowed to save (post-save).
This only works because we hardcoded the reverse relation in the source app via GenericRelation
'''

@receiver(post_save, sender=bb.Product)
def refresh_item(sender, instance, **kwargs):
    
    items = instance.ppc.all()
    
    for item in items:
        try:
            item.full_clean()
            item.save()
        except:
            raise ValidationError(_(f'Save completed, but failed to automatically update related ppc item: {item}. Please correct manually.'))