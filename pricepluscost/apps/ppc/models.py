from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    default_life = models.FloatField()

    def __str__(self):
        return(self.name)

    class Meta:
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'

class CategoryMap(models.Model):
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    product_category_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="product_category_ppc", help_text='This is the Django model class for a "category" from a product source app')
    product_category_id = models.PositiveIntegerField(verbose_name="Product source id", help_text="This is the primary key of the category from the product source app")
    product_category_object = GenericForeignKey('product_category_class', 'product_category_id')

    def __str__(self):
        return(f'Mapping for {self.product_category_class} | {self.product_category_id}')

    def clean(self):
        if not self.product_category_object:
            raise ValidationError(_('Product category id does not exist!'))
    
    def product_category_name(self):
        return(self.product_category_object.name)

    class Meta:
        verbose_name = 'Category Mapping'
        verbose_name_plural = 'Mapping Product Categories'
        unique_together = ['product_category_class','product_category_id']

class Item(models.Model):
    product_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="product_class_ppc", help_text='This is the Django model class for a product (model) from a product source app')
    product_id = models.PositiveIntegerField(verbose_name="Origin id", help_text="This is the primary key of model from the reference source app")
    product_object = GenericForeignKey('product_class', 'product_id')
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    specs_table_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='This is the Django model class for the specs of the source product.')
    
    sku = models.CharField(verbose_name="SKU", max_length=100, unique=True)
    upc = models.IntegerField(verbose_name="UPC", unique=True, blank=True)  
    name = models.CharField(max_length=500)
    model_number = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    image_url = models.TextField(verbose_name="Image URL", blank=True)
    image_thumbnail = models.TextField(verbose_name="Image Thumbnail URL", blank=True)
    energy_guide = models.TextField(verbose_name="Energy Guide Label URL", blank=True)
    affiliate_url = models.TextField(blank=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField()

    aec = models.FloatField()
    regular_cost = models.FloatField()
    sale_cost = models.FloatField()
    regular_pricepluscost = models.FloatField(verbose_name="Regular PPC")
    sale_pricepluscost = models.FloatField(verbose_name="Sale PPC")

    active = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(f'{self.product_class} | {self.product_id}')

    def clean(self):
        
        if not self.product_object:
            raise ValidationError(_('Product id does not exist in the product source!'))

        attributes = [
            'sku',
            'upc',
            'name',
            'model_number',
            'short_description',
            'long_description',
            'image_url',
            'image_thumbnail',
            'energy_guide',
            'regular_price',
            'sale_price',
            'affiliate_url'
        ]

        for attribute in attributes:
            try:
                a = getattr(self.product_object, attribute)
                setattr(self, attribute, a)
            except:
                raise ValidationError(_(f'Product class {self.product_class} has no attribute "{attribute}"'))

        try:
            setattr(self, 'manufacturer', self.product_object.manufacturer.name)
        except:
            raise ValidationError(_(f'Product class {self.product_class} has no attribute "manufacturer.name"'))

    def origin(self):
        return(self.product_class.app_label)

    def has_affiliate_url(self):
        return(self.affiliate_url is None)
    has_affiliate_url.boolean = True
    has_affiliate_url.short_description = "Affiliate"

    def has_image_url(self):
        return(self.image_url is None)
    has_image_url.boolean = True
    has_image_url.short_description = "Image"

    def has_image_thumbnail(self):
        return(self.image_thumbnail is None)
    has_image_thumbnail.boolean = True
    has_image_thumbnail.short_description = "Thumbnail"

    def has_energy_guide(self):
        return(self.energy_guide is None)
    has_energy_guide.boolean = True
    has_energy_guide.short_description = "Energy Guide"

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        unique_together = ['product_class','product_id']

# All Item fields are calculated during save so will therefore not update if the reference object updates.
# The only relation is to the product object so to delete the item if the product is deleted.
# Specs table class will be referenced, so any of those attributes will update with the source also.
# I now added a signal that will save this item whenever the source is saved, thereby updating! This must be hardcoded for each source.