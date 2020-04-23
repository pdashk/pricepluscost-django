from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
import importlib

def app_choices():
    return [(a.name, a.verbose_name) for a in apps.get_app_configs() if not a.name.startswith('django')]

class Source(models.Model):
    app = models.CharField(max_length=200, choices=app_choices(), unique=True)
    source_type = models.CharField(max_length=100, choices=[
        ('Product','Product Source'),
        ('Reference','Reference Source')
    ])
    category_model_class = models.CharField(max_length=200)
    category_name_field = models.CharField(max_length=200)
    manufacturer_model_class = models.CharField(max_length=200)
    manufacturer_name_field = models.CharField(max_length=200)
    model_model_class = models.CharField(max_length=200)
    model_number_field = models.CharField(max_length=200)
    model_manufacturer_field = models.CharField(max_length=200)
    
    def verbose_name(self):
        return(apps.get_app_config(self.app).verbose_name)

    def __str__(self):
        return(apps.get_app_config(self.app).verbose_name)

    def clean(self):
        app_config = apps.get_app_config(self.app)
        app_name = dict(app_choices()).get(self.app)
        models = [m.__name__ for m in app_config.get_models()]
        
        if self.category_model_class not in models:
            raise ValidationError(_(f'Category model class not found in the {app_name} app!'))
        elif self.manufacturer_model_class not in models:
            raise ValidationError(_(f'Manufacturer model class not found in the {app_name} app!'))
        elif self.model_model_class not in models:
            raise ValidationError(_(f'Model model class not found in the {app_name} app!'))

        category_fields = [f.name for f in app_config.get_model(self.category_model_class)._meta.get_fields()]
        manufacturer_fields = [f.name for f in app_config.get_model(self.manufacturer_model_class)._meta.get_fields()]
        model_fields = [f.name for f in app_config.get_model(self.model_model_class)._meta.get_fields()]
        
        if self.category_name_field not in category_fields:
            raise ValidationError(_(f'Category name field not found in the {self.category_model_class} class!'))
        elif self.manufacturer_name_field not in manufacturer_fields:
            raise ValidationError(_(f'Manufacturer name field not found in the {self.manufacturer_model_class} class!'))
        elif self.model_number_field not in model_fields:
            raise ValidationError(_(f'Model number field not found in the {self.model_model_class} class!'))

    class Meta:
        verbose_name_plural = '- Sources'

## Note: Product sources have model numbers while reference sources have model patterns.
## Note: Have not developed a good way to allow choices for field labels

class TestCategoryMap(models.Model):
    product_category_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="product")
    product_category_id = models.PositiveIntegerField()
    product_category_object = GenericForeignKey('product_category_class', 'product_category_id')
    reference_category_class = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='reference')
    reference_category_id = models.PositiveIntegerField()
    reference_category_object = GenericForeignKey('reference_category_class', 'reference_category_id')

    def __str__(self):
        return(f'({self.product_category_class} | {self.product_category_object.name}) -> ({self.reference_category_class} | {self.reference_category_object.name})')

    def clean(self):
        if not self.product_category_object:
            raise ValidationError(_('Product category id does not exist!'))
        elif not self.reference_category_object:
            raise ValidationError(_('Reference category id does not exist!'))

class Category(models.Model):
    name = models.CharField(max_length=200) 
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    mappings = models.ManyToManyField(
        'self', 
        symmetrical=True, 
        blank=True, 
        through="CategoryMap",
        through_fields=('category','mapped_category')
        )

    def __str__(self):
        return(f'{self.source}::{self.name}')

    def source_type(self):
        return(self.source.source_type)
        
    def clean(self):
        module_name = f"{self.source.app}.models"
        model = self.source.category_model_class
        field = self.source.category_name_field

        module = importlib.import_module(module_name)
        category_model = getattr(module, model)
        check = category_model.objects.filter(**{field: self.name})
    
        if not check:
            raise ValidationError(_('Category not found in the selected source!'))
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ['name','source']

class CategoryMap(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mapped_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="mapped")

    class Meta:
        verbose_name = 'Category Map'
        verbose_name_plural = 'Category Mappings'
        unique_together = ['category','mapped_category']

## Note: If two sources have the same category name, this COULD mean they are actually different (e.g., how a "refrigerator" is defined)
## Note: However, the manufacturer name is always a unique identifier regardless or source or category

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_mapped = models.BooleanField(default=False, editable=False, null=True, verbose_name="Mapped")
    is_primary = models.BooleanField(default=False, verbose_name="Primary", help_text="If checked, other manufacturers will be able to map to this one. If not, this manufacturer will only be able to map to others. Note: you will not be able to change this box after this manufacturer has been mapped or mapped to until you remove the conflicted maps. If you have tried mapping a primary, you will have to navigate your browser away.")

    def __str__(self):
        return(self.name)

    def mapped_to(self):
        mapped_manufacturers = ManufacturerMap.objects.filter(manufacturer=self, map_choice=True).values_list('matched_manufacturer__name', flat=True)
        return(list(mapped_manufacturers))
        
    def clean(self):

        check_count = 0
        sources = Source.objects.all()
        
        for source in sources:
            module_name = f"{source.app}.models"
            model = source.manufacturer_model_class
            field = source.manufacturer_name_field

            module = importlib.import_module(module_name)
            manufacturer_model = getattr(module, model)
            check = manufacturer_model.objects.filter(**{field: self.name})
            check_count += check.count()
        
        if check_count < 1:
            raise ValidationError(_('Manufacturer name not found in any source!'))

        self.is_mapped = self.is_primary

class ManufacturerMap(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="+", limit_choices_to={'is_primary': False})
    matched_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="+", limit_choices_to={'is_primary': True})
    match_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    map_choice = models.BooleanField(default=False)

    def __str__(self):
        return(f"Mapping for {self.manufacturer}")

    def clean(self):
        if self.manufacturer.is_primary:
            raise ValidationError(_('Cannot map a primary manufacturer!'))

        if not self.matched_manufacturer.is_primary:
            raise ValidationError(_('Cannot map to a non-primary manufacturer!'))

    class Meta:
        verbose_name = 'Manufacturer Map'
        verbose_name_plural = 'Manufacturer Mappings'
        unique_together = ['manufacturer','matched_manufacturer']

class ProductModel(models.Model):
    number = models.CharField(max_length=200, verbose_name="Model Number")
    primary_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, limit_choices_to={'is_primary': True}, verbose_name="Manufacturer")
    is_mapped = models.BooleanField(default=False, editable=False, verbose_name="Map Status")

    class Meta:
        unique_together = ['number','primary_manufacturer']

    def __str__(self):
        return(f'{self.primary_manufacturer}::{self.number}')

    def clean(self):

        model_check_count = 0
        manufacturer_check_count = 0
        all_check_count = 0

        sources = Source.objects.filter(source_type="Product")
        
        for source in sources:
            module_name = f"{source.app}.models"
            module = importlib.import_module(module_name)
            
            model_query = Q(**{source.model_number_field: self.number})
            model_model = getattr(module, source.model_model_class)
            matching_models = model_model.objects.filter(model_query)
            model_check_count += matching_models.count()
        
            manufacturer_names = list(ManufacturerMap.objects.filter(matched_manufacturer=self.primary_manufacturer).values_list("manufacturer__name", flat=True)) + [self.primary_manufacturer.name]
            manufacturer_query = Q()
            for manufacturer in manufacturer_names:
                manufacturer_query |= Q(**{source.manufacturer_name_field: manufacturer})
            manufacturer_model = getattr(module, source.manufacturer_model_class)
            matching_manufacturers = manufacturer_model.objects.filter(manufacturer_query)
            manufacturer_check_count += matching_manufacturers.count()

            matching_manufacturers_query = Q()
            for manufacturer in matching_manufacturers:
                matching_manufacturers_query |= Q(**{source.model_manufacturer_field:manufacturer})
            matching_all = model_model.objects.filter(model_query, matching_manufacturers_query)
            all_check_count += matching_all.count()

        if model_check_count < 1:
            raise ValidationError(_('Model number not found in any product source!'))
        elif manufacturer_check_count < 1:
            raise ValidationError(_('Manufacturer not found in any product source!'))
        elif all_check_count < 1:
            raise ValidationError(_('Model number and manufacturer found in a product source, but the model number does not belong to the selected manufacturer!'))
        
class ReferenceModel(models.Model):
    pattern = models.CharField(max_length=200, verbose_name="Model Number Pattern")
    primary_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, limit_choices_to={'is_primary': True}, verbose_name="Manufacturer")
    source = models.ForeignKey(Source, on_delete=models.CASCADE, limit_choices_to={'source_type': 'Reference'}, verbose_name='Reference Source')

    class Meta:
        unique_together = ['pattern','primary_manufacturer']

    def __str__(self):
        return(f'{self.primary_manufacturer}::{self.pattern}')

    def clean(self):
        module_name = f"{self.source.app}.models"
        module = importlib.import_module(module_name)
        
        model_query = Q(**{self.source.model_number_field: self.pattern})
        model_model = getattr(module, self.source.model_model_class)
        matching_models = model_model.objects.filter(model_query)
        
        if not matching_models:
            raise ValidationError(_('Model number not found in the selected reference source!'))

        manufacturer_names = list(ManufacturerMap.objects.filter(matched_manufacturer=self.primary_manufacturer).values_list("manufacturer__name", flat=True)) + [self.primary_manufacturer.name]
        manufacturer_query = Q()
        for manufacturer in manufacturer_names:
            manufacturer_query |= Q(**{self.source.manufacturer_name_field: manufacturer})
        manufacturer_model = getattr(module, self.source.manufacturer_model_class)
        matching_manufacturers = manufacturer_model.objects.filter(manufacturer_query)

        if not matching_manufacturers:
            raise ValidationError(_('Model number found but the selected primary manufacturer is not mapped to any manufacturer in the selected reference source!'))

        matching_manufacturers_query = Q()
        for manufacturer in matching_manufacturers:
            matching_manufacturers_query |= Q(**{self.source.model_manufacturer_field:manufacturer})
        matching_all = model_model.objects.filter(model_query, matching_manufacturers_query)

        if not matching_all:
            raise ValidationError(_('Model number and manufacturer found in the selected reference source, but the model number does not belong to the select manufacturer!'))
        
## Note: Two different manufacturers that are mapped together with the same model number would be the SAME model. Check in test.
## Note: Within the same manufacturer, model number cannot repeat, but theoretically possible across manufacturers
## Note: Within the same source or category, repeating model number is practically nonexistent, but theoretically possible
## Note: The same model pattern from two different sources means two different models

class ModelMap(models.Model):
    product_model = models.OneToOneField(ProductModel, on_delete=models.CASCADE)
    reference_model = models.ForeignKey(ReferenceModel, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    map_choice = models.BooleanField(default=False)

## Note: A mapping is a ProductModel mapped to a ReferenceModel-Source
