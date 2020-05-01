from django.db import models
from django.contrib.contenttypes.fields import GenericRelation # added for reverse relation with 'maps' app
from maps.models import CategoryMap, ReferenceManufacturer, ReferenceModel # added for reverse relation with 'maps' app

class ProductGroup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand_name_field = models.CharField(max_length=200)
    model_number_field = models.CharField(max_length=200)
    efficiency_value_1_field = models.CharField(max_length=200)
    efficiency_value_2_field = models.CharField(max_length=200, blank=True)
    efficiency_value_3_field = models.CharField(max_length=200, blank=True)
    efficiency_value_4_field = models.CharField(max_length=200, blank=True)
    life_field = models.CharField(max_length=200, blank=True)
    energy_guide_field = models.CharField(max_length=200, blank=True)
    subcategory_field = models.CharField(max_length=200, blank=True)
    additional_identifier_field = models.CharField(max_length=200, blank=True)
    mapping = GenericRelation(CategoryMap, content_type_field='reference_category_class', object_id_field='reference_category_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return self.name
    
    def has_efficiency_value_2_field(self):
        return(self.efficiency_value_2_field is not '')
    has_efficiency_value_2_field.boolean = True
    has_efficiency_value_2_field.short_description = "2nd Efficiency Value Field"

    def has_efficiency_value_3_field(self):
        return(self.efficiency_value_3_field is not '')
    has_efficiency_value_3_field.boolean = True
    has_efficiency_value_3_field.short_description = "3rd Efficiency Value Field"

    def has_efficiency_value_4_field(self):
        return(self.efficiency_value_4_field is not '')
    has_efficiency_value_4_field.boolean = True
    has_efficiency_value_4_field.short_description = "4th Efficiency Value Field"

    def has_life_field(self):
        return(self.life_field is not '')
    has_life_field.boolean = True
    has_life_field.short_description = "Life Field"

    def has_energy_guide_field(self):
        return(self.energy_guide_field is not '')
    has_energy_guide_field.boolean = True
    has_energy_guide_field.short_description = "Energy Guide Field"

    def has_subcategory_field(self):
        return(self.subcategory_field is not '')
    has_subcategory_field.boolean = True
    has_subcategory_field.short_description = "Subcategory Field"

    def has_additional_identifier_field(self):
        return(self.additional_identifier_field is not '')
    has_additional_identifier_field.boolean = True
    has_additional_identifier_field.short_description = "Subcategory Field"

    class Meta:
        verbose_name = 'Product Group'
        verbose_name_plural = 'Product Groups'

class BrandName(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    mapping = GenericRelation(ReferenceManufacturer, content_type_field='manufacturer_class', object_id_field='manufacturer_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return(self.name)

class Model(models.Model):
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    ccms_oop = models.IntegerField(verbose_name="CCMS Unique Identifier", unique=True, help_text="Appears to be a unique identifier for CCMS")
    subcategory = models.CharField(max_length=500, blank=True, help_text="For product group that may have sub-categories")
    additional_identifier = models.CharField(max_length=500, blank=True, help_text="Free field to use for any class if additional field is needed to help identify a match.")
    brand_name = models.ForeignKey(BrandName, on_delete=models.CASCADE)
    model_number = models.CharField(max_length=200)
    efficiency_value_1 = models.FloatField(verbose_name="Primary efficiency metric")
    efficiency_value_2 = models.FloatField(blank=True, null=True, help_text="Optional energy calculation metric (e.g., standby)")
    efficiency_value_3 = models.FloatField(blank=True, null=True, help_text="Optional energy calculation metric")
    efficiency_value_4 = models.FloatField(blank=True, null=True, help_text="Optional energy calculation metric")
    life = models.FloatField(blank=True, null=True, help_text="If provided by CCMS, will be used in place of default average")
    energy_guide = models.TextField(blank=True, null=True, help_text="Energy guide URL link when provided by DOE")
    mapping = GenericRelation(ReferenceModel, content_type_field='model_class', object_id_field='model_id') # added for reverse relation with 'maps' app
    last_updated = models.DateTimeField(auto_now=True)

    def has_energy_guide(self):
        return(self.energy_guide is not '')
    has_energy_guide.boolean = True
    has_energy_guide.short_description = "Energy Guide"

    def __str__(self):
        return str(self.ccms_oop)

