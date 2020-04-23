from django.db import models

class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    default_life = models.FloatField()
    
    def __str__(self):
        return(self.name)

    class Meta:
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'

class Item(models.Model):
    product = models.ForeignKey('bb.Product', on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Generated Items'

# we want PPC items to delete when the item from the product source is deleted (use genericforeignkey)
# two approaches to updating other fields
# -- we could link everything so that if field changes in source, it changes in the ppc item
# -- we could unsync and force integration step