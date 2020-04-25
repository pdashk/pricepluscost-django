from django.contrib import admin
from .models import ProductCategory, EfficiencyMetric, Model, BrandName

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'efficiency_metric'
    )
admin.site.register(ProductCategory, ProductCategoryAdmin)

class EfficiencyMetricAdmin(admin.ModelAdmin):
    pass
admin.site.register(EfficiencyMetric, EfficiencyMetricAdmin)

class ModelAdmin(admin.ModelAdmin):
    list_display = (
        'estar_uid',
        'product_category',
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