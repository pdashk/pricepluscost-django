from django.contrib import admin
from .models import ElectricityRate

class ElectricityRateAdmin(admin.ModelAdmin):
    list_display = (
        'series_id',
        'state',
        'year',
        'month',
        'value',
        'active',
        'update_date'
    )

admin.site.register(ElectricityRate, ElectricityRateAdmin)