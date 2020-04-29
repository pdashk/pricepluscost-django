from django.db import models

class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    series_id = models.CharField(max_length=50)
    iso3166 = models.CharField(max_length=20)
    rolling_average = models.FloatField(verbose_name="Rolling Annual Average (cents per kWh for last 12 months)")
    average_start_date = models.DateField()
    average_end_date = models.DateField()
    source_update_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name