from django.contrib import admin
from .models import ProductCategory, Product, ProductSpec, Manufacturer

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category_id'
        )
admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'upc',
        'product_id',
        'product_category',
        'model_number',
        'manufacturer',
        'active',
        'affiliated',
        'download_date'
        )
    list_filter = (
        'product_category',
        'manufacturer',
        'active'
    )
    readonly_fields = ['download_date']
admin.site.register(Product, ProductAdmin)

class ProductSpecAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'attribute',
        'value'
        )
admin.site.register(ProductSpec, ProductSpecAdmin)

admin.site.register(Manufacturer)