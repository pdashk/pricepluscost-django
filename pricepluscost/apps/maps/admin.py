from django.contrib import admin
from .models import Source, TestCategoryMap, Category, CategoryMap, Manufacturer, ManufacturerMap, ProductModel, ReferenceModel, ModelMap

admin.site.register(TestCategoryMap)

class SourceAdmin(admin.ModelAdmin):
    list_display = [
        'verbose_name',
        'source_type',
    ]
    list_filter = [
        'source_type'
    ]
    fieldsets = [
        (None,              {'fields': ['app','source_type']}),
        ('Configuration',   {'fields': [
            'category_model_class', 
            'category_name_field',
            'manufacturer_model_class',
            'manufacturer_name_field',
            'model_model_class',
            'model_number_field',
            'model_manufacturer_field'
            ],
                            'description': 'Type in the Django model class and fields for the selected source app. If the source app does not have such classes of fields, then it is not compatible with this app.'})
    ]
admin.site.register(Source, SourceAdmin)

class CategoryMapInline(admin.TabularInline):
    model = CategoryMap
    extra = 0
    fk_name = "category"
    verbose_name = "Category Mapping"
    verbose_name_plural  = "Category Mappings"

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'source',
        'source_type'
    ]
    list_filter = [
        'source'
    ]
    inlines = [CategoryMapInline]
admin.site.register(Category, CategoryAdmin)

class ManufacturerMapToInline(admin.TabularInline):
    model = ManufacturerMap
    extra = 0
    fk_name = 'manufacturer'
    verbose_name = 'Potential Mapping'
    verbose_name_plural = 'Potential Mappings to a Primary Manufacturer (Select one)'

class ManufacturerMappedFromInline(admin.TabularInline):
    model = ManufacturerMap
    extra = 0
    fk_name = 'matched_manufacturer'
    verbose_name = 'Mapping'
    verbose_name_plural = 'Other Manufacturers mapped to this Manufacturer'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(ManufacturerMappedFromInline, self).get_queryset(request)
        return qs.filter(map_choice=True)

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_mapped',
        'is_primary',
        'mapped_to'
    ]
    list_filter = [
        'is_mapped',
        'is_primary'
    ]
    inlines = [ManufacturerMapToInline, ManufacturerMappedFromInline]
admin.site.register(Manufacturer, ManufacturerAdmin)

class ModelMapInline(admin.TabularInline):
    model = ModelMap
    extra = 0
    fk_name = 'product_model'

class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'primary_manufacturer',
        'is_mapped'
    ]
    list_filter = [
        'is_mapped'
    ]
    inlines = [ModelMapInline]
admin.site.register(ProductModel, ProductModelAdmin)

class ReferenceModelAdmin(admin.ModelAdmin):
        list_display = [
        'primary_manufacturer',
        'pattern',
        'source'
    ]
admin.site.register(ReferenceModel, ReferenceModelAdmin)