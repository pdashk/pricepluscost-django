from django.db import models
from django.contrib.contenttypes.fields import GenericRelation # added for reverse relation with 'maps' app
from maps.models import CategoryMap, ProductBrand, Product # added for reverse relation with 'maps' app

class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    category_id = models.CharField(max_length=200)
    mapping = GenericRelation(CategoryMap, content_type_field='product_category_class', object_id_field='product_category_id') # added for reverse relation with 'maps' app
    
    def __str__(self):
        return(self.name)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    mapping = GenericRelation(ProductBrand, content_type_field='brand_class', object_id_field='brand_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return(self.name)

class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sku = models.CharField(verbose_name="SKU", max_length=100, unique=True)
    upc = models.IntegerField(verbose_name="UPC", unique=True, blank=True)
    product_id = models.IntegerField(verbose_name="Product ID", blank=True)
    name = models.CharField(max_length=500)
    model_number = models.CharField(max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    start_date = models.DateField()
    active = models.BooleanField(default=False)
    active_update_date = models.DateTimeField()
    regular_price = models.FloatField()
    sale_price = models.FloatField()
    price_update_date = models.DateTimeField()
    affiliate_url = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    image_url = models.TextField(verbose_name="Image URL", blank=True)
    image_thumbnail = models.TextField(verbose_name="Image Thumbnail URL", blank=True)
    energy_guide = models.TextField(verbose_name="Energy Guide Label URL", blank=True)
    download_date = models.DateTimeField(auto_now=True)
    mapping = GenericRelation(Product, content_type_field='product_class', object_id_field='product_id') # added for reverse relation with 'maps' app

    def __str__(self):
        return(self.sku)

    def affiliated(self):
        return(self.affiliate_url is None)
    affiliated.boolean = True

# bestbuy api requires data not be stored for more than 3 days

class ProductSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return(str(self.product_id))
    
    class Meta:
        verbose_name = 'Product Specification'
        verbose_name_plural = 'Product Specifications'

# Other Options: related skus, shoponline vs instore, availability, more images