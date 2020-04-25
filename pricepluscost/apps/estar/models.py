from django.db import models
from django.contrib.contenttypes.fields import GenericRelation # added for reverse relation with 'maps' app
from maps.models import CategoryMap, ReferenceManufacturer, ReferenceModel # added for reverse relation with 'maps' app

class EfficiencyMetric(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Efficiency Metric'
        verbose_name_plural = 'Efficiency Metrics'

class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    efficiency_metric = models.ForeignKey(EfficiencyMetric, null=True, on_delete=models.SET_NULL)
    mapping = GenericRelation(CategoryMap, content_type_field='reference_category_class', object_id_field='reference_category_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

class BrandName(models.Model):
    name = models.CharField(max_length=200, unique=True)
    mapping = GenericRelation(ReferenceManufacturer, content_type_field='brand_class', object_id_field='brand_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return(self.name)

class Model(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    estar_uid = models.IntegerField(verbose_name="ENERGY STAR Unique Identifier", unique=True)
    brand_name = models.ForeignKey(BrandName, on_delete=models.CASCADE)
    model_number = models.CharField(max_length=200)
    efficiency_value = models.FloatField()
    life = models.FloatField(blank=True, null=True)
    mapping = GenericRelation(ReferenceModel, content_type_field='model_class', object_id_field='model_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return str(self.estar_uid)

