from django.contrib import admin
from .models import ProductGroup, EfficiencyMetric, Model, BrandName

class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'efficiency_metric'
    )
admin.site.register(ProductGroup, ProductGroupAdmin)

class EfficiencyMetricAdmin(admin.ModelAdmin):
    pass
admin.site.register(EfficiencyMetric, EfficiencyMetricAdmin)

class ModelAdmin(admin.ModelAdmin):
    list_display = (
        'ccms_oop',
        'product_group',
        'brand_name',
        'model_number',
        'efficiency_value',
        'life'
    )
admin.site.register(Model, ModelAdmin)

class BrandNameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
admin.site.register(BrandName, BrandNameAdmin)