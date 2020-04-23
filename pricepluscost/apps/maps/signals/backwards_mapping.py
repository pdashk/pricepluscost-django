from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from maps.models import CategoryMap

'''
Need this because backwards relation created automatically only when the relation is created via the Category class.
If created via CategoryMap (as is done with AdminInline), then backwards relation needs to be created manually
'''
@receiver(post_save, sender=CategoryMap)
def backward_save(sender, instance, **kwargs):
    category = instance.category
    mapped_category = instance.mapped_category
    reverse_check = CategoryMap.objects.filter(category=mapped_category,mapped_category=category)
    
    if reverse_check:
        pass
    else:
        reverse = CategoryMap(category=mapped_category,mapped_category=category)
        reverse.save()

@receiver(post_delete, sender=CategoryMap)
def backward_delete(sender, instance, **kwargs):
    category = instance.category
    mapped_category = instance.mapped_category
    reverse = CategoryMap.objects.filter(category=mapped_category,mapped_category=category)
    
    if not reverse:
        pass
    else:
        reverse.delete()
