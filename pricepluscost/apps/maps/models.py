from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CategoryMap(models.Model):
    product_category_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="product_category", help_text='This is the Django model class for a "category" from a product source app')
    product_category_id = models.PositiveIntegerField(verbose_name="Product source id", help_text="This is the primary key of the category from the product source app")
    product_category_object = GenericForeignKey('product_category_class', 'product_category_id')
    reference_category_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='reference_category', help_text='This is the Django model class for a "category" from a reference source app')
    reference_category_id = models.PositiveIntegerField(verbose_name="Referecnce source id", help_text="This is the primary key of the category from the reference source app")
    reference_category_object = GenericForeignKey('reference_category_class', 'reference_category_id')

    def __str__(self):
        return(f'Mapping for {self.product_category_class} | {self.product_category_id}')

    def clean(self):
        if not self.product_category_object:
            raise ValidationError(_('Product category id does not exist!'))
        elif not self.reference_category_object:
            raise ValidationError(_('Reference category id does not exist!'))
    
    def product_category_name(self):
        try:
            return(self.product_category_object.name)
        except:
            return(None)

    def reference_category_name(self):
        try:
            return(self.reference_category_object.name)
        except:
            return(None)

    class Meta:
        verbose_name = 'Category Mapping'
        verbose_name_plural = 'Mapping Categories'
        unique_together = ['product_category_class','product_category_id']

class ProductBrand(models.Model):
    brand_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='This is the Django model class for a brand or manufacturer from a product source app')
    brand_id = models.PositiveIntegerField(verbose_name="Source id", help_text="This is the primary key of the brand or manufacturer from the product source app")
    brand_object = GenericForeignKey('brand_class', 'brand_id')
    is_mapped = models.BooleanField(default=False, editable=False, null=True, verbose_name="Mapped")

    def __str__(self):
        return(f"{self.brand_class} | {self.brand_id}")

    def name(self):
        return(self.brand_object.name)

    def clean(self):
        if not self.brand_object:
            raise ValidationError(_('Brand or manufacturer id does not exist in the product source!'))
        
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Mapping Manufacturers and Brands'
        unique_together = ['brand_class','brand_id']
        
class ReferenceManufacturer(models.Model):
    manufacturer_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='This is the Django model class for a brand or manufacturer from a reference source app')
    manufacturer_id = models.PositiveIntegerField(verbose_name="Source id", help_text="This is the primary key of the brand or manufacturer from the reference source app")
    manufacturer_object = GenericForeignKey('manufacturer_class', 'manufacturer_id')

    def __str__(self):
        return(f"{self.id} | {self.manufacturer_object.name}")

    def name(self):
        return(self.manufacturer_object.name)

    def source(self):
        return(self.manufacturer_class.app_label)

    def clean(self):
        if not self.manufacturer_object:
            raise ValidationError(_('Manufacturer id does not exist in the reference source!'))

    class Meta:
        verbose_name = 'Reference Manufacturer'
        verbose_name_plural = 'List of Reference Manufacturers'
        unique_together = ['manufacturer_class','manufacturer_id']

class ManufacturerMap(models.Model):
    product_brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    reference_manufacturer = models.ForeignKey(ReferenceManufacturer, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    map_choice = models.BooleanField(default=False)

    def __str__(self):
        return(f"A {self.map_choice} mapping for {self.product_brand}")

    class Meta:
        unique_together = ['product_brand','reference_manufacturer']

class Product(models.Model):
    product_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='This is the Django model class for a product (model) from a product source app')
    product_id = models.PositiveIntegerField(verbose_name="Source id", help_text="This is the primary key of model from the reference source app")
    product_object = GenericForeignKey('product_class', 'product_id')
    is_mapped = models.BooleanField(default=False, editable=False, verbose_name="Mapped")

    def model_number(self):
        return(self.product_object.model_number) # will require reference sources to have this field

    def brand(self):
        return(self.product_object.manufacturer.name) # will require reference sources to have these fields

    def source(self):
        return(self.product_class.app_label)

    def __str__(self):
        return(f"{self.brand()} | {self.model_number()}") # will require reference sources to have this field

    def clean(self):
        if not self.product_object:
            raise ValidationError(_('Product id does not exist in the product source!'))

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Mapping Products'
        unique_together = ['product_class','product_id']
            
class ReferenceModel(models.Model):
    model_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='This is the Django model class for a model from a reference source app')
    model_id = models.PositiveIntegerField(verbose_name="Source id", help_text="This is the primary key of model from the reference source app")
    model_object = GenericForeignKey('model_class', 'model_id')

    def model_number(self):
        return(self.model_object.model_number) # will require reference sources to have this field

    def manufacturer(self):
        return(self.model_object.brand_name.name) # will require reference sources to have these fields

    def source(self):
        return(self.model_class.app_label)

    def __str__(self):
        return(f"{self.manufacturer()} | {self.model_number()}")

    def clean(self):
        if not self.model_object:
            raise ValidationError(_('Model id does not exist in the reference source!'))

    class Meta:
        verbose_name = 'Reference Model'
        verbose_name_plural = 'List of Reference Models'
        unique_together = ['model_class','model_id']

class ModelMap(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reference_model = models.ForeignKey(ReferenceModel, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    map_choice = models.BooleanField(default=False)

    def __str__(self):
        return(f"A {self.map_choice} mapping for {self.product}")

    class Meta:
        unique_together = ['product','reference_model']