from django.contrib import admin
from .models import CategoryMap, ProductBrand, ReferenceManufacturer, ManufacturerMap, Product, ReferenceModel, ModelMap

#####################################################################################################################
########### Each reference source will require it's own inline in "ProductBrandAdmin" and "ProductAdmin" ############
#####################################################################################################################
# 1. Override the get_queryset() method to make sure that "ManufacturerMap" is filtered for the appropriate reference
# 2. Remember to add the inline the the classes below

#### Inlines for Reference: CCMS
class ManufacturerMapInline_1(admin.TabularInline):
    model = ManufacturerMap
    extra = 0
    fk_name = 'product_brand'
    verbose_name = 'Potential Mapping'
    verbose_name_plural = 'Mappings to CCMS Manufacturer'

    def get_queryset(self, request):
        qs = super(ManufacturerMapInline_1, self).get_queryset(request)
        return qs.filter(reference_manufacturer__manufacturer_class__app_label='ccms')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reference_manufacturer":
            kwargs["queryset"] = ReferenceManufacturer.objects.filter(manufacturer_class__app_label='ccms')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ModelMapInline_1(admin.TabularInline):
    model = ModelMap
    extra = 0
    fk_name = 'product'
    verbose_name = 'Potential Mapping'
    verbose_name_plural = 'Mappings to CCMS Model'

    def get_queryset(self, request):
        qs = super(ModelMapInline_1, self).get_queryset(request)
        return qs.filter(reference_model__model_class__app_label='ccms')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reference_model":
            kwargs["queryset"] = ReferenceModel.objects.filter(model_class__app_label='ccms')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#### Inlines for Reference: ENERGY STAR
class ManufacturerMapInline_2(admin.TabularInline):
    model = ManufacturerMap
    extra = 0
    fk_name = 'product_brand'
    verbose_name = 'Potential Mapping'
    verbose_name_plural = 'Mappings to ENERGY STAR Brand'

    def get_queryset(self, request):
        qs = super(ManufacturerMapInline_2, self).get_queryset(request)
        return qs.filter(reference_manufacturer__manufacturer_class__app_label='estar')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reference_manufacturer":
            kwargs["queryset"] = ReferenceManufacturer.objects.filter(manufacturer_class__app_label='estar')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ModelMapInline_2(admin.TabularInline):
    model = ModelMap
    extra = 0
    fk_name = 'product'
    verbose_name = 'Potential Mapping'
    verbose_name_plural = 'Mappings to ENERGY STAR Model'

    def get_queryset(self, request):
        qs = super(ModelMapInline_2, self).get_queryset(request)
        return qs.filter(reference_model__model_class__app_label='estar')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reference_model":
            kwargs["queryset"] = ReferenceModel.objects.filter(model_class__app_label='estar')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

#####################################################################################################################
#####################################################################################################################


class CategoryMapAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product_category_name',
        'reference_category_name',
        'product_category_class',
        'reference_category_class'
    ]
    
    list_filter = [
        ('product_category_class', admin.RelatedOnlyFieldListFilter),
        ('reference_category_class', admin.RelatedOnlyFieldListFilter)
    ]
    
    fieldsets = [
        (None, {
            'fields': ['product_category_class', 'product_category_id', 'product_category_name'],
            'description': 'Select the class and id for a product category from any product source app. You will map this to one or more reference source categories. The mapping allows for products in the product category to be mapped to reference models in the reference source and category. You must go to the admin page for the category to find the id (primary key), or you can just add it, and the category name should show up before or on the model list page.'
            }),
        (None, {
            'fields': ['reference_category_class', 'reference_category_id','reference_category_name'],
            'description': 'Next, select the class and id for a corresponding reference category. A product category can map to multiple reference categories, e.g, if the product category is broader than any single reference category.'
            }),
    ]

    readonly_fields = ['product_category_name','reference_category_name']

    def product_category_name(self, obj):
        return(obj.product_category_name())
    product_category_name.short_description = "Product Category Name (from lookup)"

    def reference_category_name(self, obj):
        return(obj.reference_category_name())
    reference_category_name.short_description = "Reference Category Name (from lookup)"

class ProductBrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'brand_class',
        'is_mapped'
    ]
    
    list_filter = [
        'is_mapped',
        ('brand_class', admin.RelatedOnlyFieldListFilter)
    ]
    
    fieldsets = [
        (None, {
            'fields': ['brand_class', 'brand_id','name'],
            'description': 'Select the Django manufacturer or brand class and id from a product source. You will have to look up the primary key from the source app. Once saved, the name should display below. You can also add potential mappings to any of the below reference manufacturers. You may then select one or more of the potential mappings. The mapping will restrict which models from the reference can be mapped to the product.'
            })
    ]
    
    readonly_fields = ['name']

    def name(self, obj):
        return(obj.name())
    name.short_description = "Name (from lookup)"

    inlines = [ManufacturerMapInline_1, ManufacturerMapInline_2]

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'model_number',
        'brand',
        'product_id',
        'product_class',
        'is_mapped'
    ]

    list_filter = [
        'is_mapped',
        ('product_class', admin.RelatedOnlyFieldListFilter)
    ]

    fieldsets = [
        (None, {
            'fields': ['product_class', 'product_id','model_number', 'brand'],
            'description': 'Select the Django model class and id from a product source. You will have to look up the primary key from the source app. Once saved, the model number and brand should display below.'
            })
    ]
    
    readonly_fields = ['model_number', 'brand']

    def model_number(self, obj):
        return(obj.model_number())
    model_number.short_description = "Model number (from lookup)"

    def brand(self, obj):
        return(obj.brand())
    brand.short_description = "Manufacturer or Brand (from lookup)"

    inlines = [ModelMapInline_1, ModelMapInline_2]

class ReferenceManufacturerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'manufacturer_id',
        'manufacturer_class'
    ]

    list_filter = [
        ('manufacturer_class', admin.RelatedOnlyFieldListFilter)
    ]

    fieldsets = [
        (None, {
            'fields': ['manufacturer_class', 'manufacturer_id','name'],
            'description': 'Select the Django manufacturer or brand class and id from a reference source. You will have to look up the primary key from the source app. Once saved, the model number and manufacturer should display below.'
            })
    ]
    
    readonly_fields = ['name']

    def name(self, obj):
        return(obj.name())
    name.short_description = "Name (from lookup)"

class ReferenceModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'model_number',
        'manufacturer',
        'model_id',
        'model_class'
    ]

    list_filter = [
        ('model_class', admin.RelatedOnlyFieldListFilter)
    ]

    fieldsets = [
        (None, {
            'fields': ['model_class', 'model_id','model_number', 'manufacturer'],
            'description': 'Select the Django model class and id from a reference source. You will have to look up the primary key from the source app. Once saved, the name should display below.'
            })
    ]
    
    readonly_fields = ['model_number', 'manufacturer']

    def model_number(self, obj):
        return(obj.model_number())
    model_number.short_description = "Model number (from lookup)"

    def manufacturer(self, obj):
        return(obj.manufacturer())
    manufacturer.short_description = "Manufacturer or Brand (from lookup)"

admin.site.register(CategoryMap, CategoryMapAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReferenceManufacturer, ReferenceManufacturerAdmin)
admin.site.register(ReferenceModel, ReferenceModelAdmin)