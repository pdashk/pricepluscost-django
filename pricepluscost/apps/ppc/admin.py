from django.contrib import admin
from .models import ItemCategory, CategoryMap, CategoryHoursOfUse, Item, ItemAEC, ItemRegularPPC, ItemSalePPC

class CategoryMapInline(admin.TabularInline):
    model = CategoryMap
    extra = 0
    fk_name = 'item_category'
    verbose_name = 'Prduct Source Mapping'
    verbose_name_plural = 'Mappings to Product Source Categories'

class CategoryHOUInline(admin.TabularInline):
    model = CategoryHoursOfUse
    extra = 0
    fk_name = 'item_category'
    verbose_name = 'Hours of Use'
    verbose_name_plural = 'Category Hours of Use by State'

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
    
    inlines = [CategoryMapInline, CategoryHOUInline]

class ItemRegularPPCInline(admin.TabularInline):
    model = ItemRegularPPC
    extra = 0
    fk_name = 'item'
    verbose_name = 'Regular PPC'
    verbose_name_plural = 'Regular PPC by State'
    classes = ['collapse']
    readonly_fields = ['state','regular_ppc']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class ItemSalePPCInline(admin.TabularInline):
    model = ItemSalePPC
    extra = 0
    fk_name = 'item'
    verbose_name = 'Sale PPC'
    verbose_name_plural = 'Sale PPC by State'
    classes = ['collapse']
    readonly_fields = ['state','sale_ppc']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'origin',
        'product_id',
        'sku',
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
                'last_updated'
                ],
            'description': 'No manual input. Save object to recalculate.'
            })
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

    inlines = [ItemRegularPPCInline, ItemSalePPCInline]

admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(Item, ItemAdmin)
