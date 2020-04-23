from django.db import models

class EfficiencyMetric(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Efficiency Metric'
        verbose_name_plural = 'Efficiency Metrics'

class ProductGroup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    efficiency_metric = models.ForeignKey(EfficiencyMetric, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Group'
        verbose_name_plural = 'Product Groups'

class BrandName(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return(self.name)

class Model(models.Model):
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    ccms_oop = models.IntegerField(verbose_name="CCMS Unique Identifier", unique=True)
    brand_name = models.ForeignKey(BrandName, on_delete=models.CASCADE)
    model_number = models.CharField(max_length=200)
    efficiency_value = models.FloatField()
    life = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.ccms_oop)

