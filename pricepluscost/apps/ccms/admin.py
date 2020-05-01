from string import ascii_uppercase
from django.contrib import admin

from .models import ProductGroup, Model, BrandName

from .utils.update import update_model_data

class BrandLetterListFilter(admin.SimpleListFilter):
    title = 'First Letter'
    parameter_name = 'letter'

    def lookups(self, request, model_admin):
        return [(_,_) for _ in ascii_uppercase] 

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__startswith=self.value())
        else:
            return(queryset)

class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'has_efficiency_value_2_field',
        'has_efficiency_value_3_field',
        'has_efficiency_value_4_field',
        'has_life_field',
        'has_energy_guide_field',
        'has_subcategory_field',
        'has_additional_identifier_field',
    )
        
    fieldsets = [
        (None, {
            'fields': [
                'name'
                ],
            'description': 'Identify the CCMS product group. The name needs to be exact in order to download from the source!'
            }),
        ('Mandatory Fields', {
            'fields': [
                'brand_name_field', 
                'efficiency_value_1_field',
                'model_number_field',
                ],
            'description': 'Identify column headers that map the the relevant fields. If they are not exacty, then download will raise exception. These fields must be filled.'
            }),
        ('Optional Fields', {
            'fields': [
                'life_field', 
                'energy_guide_field', 
                'subcategory_field',
                'additional_identifier_field',
                'efficiency_value_2_field',
                'efficiency_value_3_field',
                'efficiency_value_4_field',
                ],
            'description': 'Identify column headers that map the the relevant fields. If they are not exacty, then download will raise exception. These fields are optional; if they are blank, downloads will ignore them.'
            })
    ]

admin.site.register(ProductGroup, ProductGroupAdmin)

class ModelAdmin(admin.ModelAdmin):
    list_display = (
        'ccms_oop',
        'subcategory',
        'brand_name',
        'model_number',
        'efficiency_value_1',
        'life',
        'has_energy_guide',
        'last_updated'
    )
    list_filter = [
        'product_group'
    ]
    ordering = ['-last_updated','ccms_oop',]

    readonly_fields = ['last_updated']

    actions = ['refresh_model_data']

    def refresh_model_data(self, request, queryset):
        
        updates = []

        for obj in queryset:
            update = update_model_data(obj)
            updates.append(update)
        
        self.message_user(request, f"Successfully refreshed {sum(updates)}/{len(updates)} selected states")

admin.site.register(Model, ModelAdmin)

class BrandNameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_date'
    )
    
    ordering = ['created_date','name']
    readonly_fields = ['created_date']
    list_filter = (BrandLetterListFilter,)

admin.site.register(BrandName, BrandNameAdmin)