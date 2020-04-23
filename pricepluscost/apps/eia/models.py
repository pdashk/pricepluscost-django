from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class ElectricityRate(models.Model):
    series_id = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    month_year = models.DateField(verbose_name="Month-Year")
    value = models.FloatField()
    update_date = models.DateTimeField(verbose_name="Last Updated")
    active = models.BooleanField()
    
    def __str__(self):
        return self.series_id

    def year(self):
        return self.month_year.year
    
    def month(self):
        return self.month_year.month

    class Meta:
        verbose_name = 'Electricity Rate'
        verbose_name_plural = 'Electricity Rates'