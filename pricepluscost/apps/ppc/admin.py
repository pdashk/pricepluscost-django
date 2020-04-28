from django.contrib import admin
from .models import ItemCategory, CategoryMap, Item

class CategoryMapInline(admin.TabularInline):
    model = CategoryMap
    extra = 0
    fk_name = 'item_category'
    verbose_name = 'Prduct Source Mapping'
    verbose_name_plural = 'Mappings to Product Source Categories'

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'default_life'
        ]
        
    fieldsets = [
        (None, {
            'fields': ['name', 'description', 'default_life'],
            'description': 'This is a category that will appear on the web application. Currently, the creation of this category does not automatically create the URL path; this needs to be done manually in urls.py. The mapping below will determine how items are categorized from their product sources.'
            })
    ]
    
    inlines = [CategoryMapInline]

class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'origin',
        'product_id',
        'sku',
        'regular_pricepluscost',
        'sale_pricepluscost',
        'has_affiliate_url',
        'has_image_url',
        'has_image_thumbnail',
        'has_energy_guide',
        'active',
        'last_updated'
    ]

    list_filter = [
        'item_category',
        ('product_class',admin.RelatedOnlyFieldListFilter)
    ]

    fieldsets = [
        ('Selections', {
            'fields': [
                'active',
                'item_category',
                'product_class',
                'specs_table_class',
                'product_id'
                ]
            }),
        ('Immutable fields from product origin', {
            'fields': [
                'sku',
                'upc',
                'name',
                'model_number', 
                'manufacturer',
                'regular_price',
                'sale_price',
                'short_description',
                'long_description',
                'image_url',
                'image_thumbnail',
                'energy_guide',
                'affiliate_url'
                ],
            'description': 'Fields that are extracted from the product origin. If needing to change, modify them from the source app.',
            'classes': ('collapse',),
            }),
        ('Calculated Fields', {
            'fields': [
                'aec',
                'regular_cost',
                'sale_cost',
                'regular_pricepluscost',
                'sale_pricepluscost'
                ],
            'description': 'Fields that are calculated.',
            'classes': ('collapse',),
            }),
        (None, {'fields': ['last_updated']})
    ]
    
    readonly_fields = [
        'sku',
        'upc',
        'name',
        'model_number', 
        'manufacturer',
        'regular_price',
        'sale_price',
        'last_updated',
        'short_description',
        'long_description',
        'image_url',
        'image_thumbnail',
        'energy_guide',
        'affiliate_url'
        ]

    def origin(self, obj):
        return(obj.origin())
    origin.short_description = "Origin"

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Item, ItemAdmin)
