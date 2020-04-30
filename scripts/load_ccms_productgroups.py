import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricepluscost.settings")
django.setup()

from ccms.models import ProductGroup

PRODUCT_GROUP_CONFIGS = [
    {
        'name': 'Refrigerators, Refrigerator-Freezers, and Freezers',
        'defaults': {
            'brand_name_field': 'Brand_Name_s__s',
            'model_number_field': 'Individual_Model_Number_Covered_by_Basic_Model_m',
            'efficiency_value_1_field': 'Annual_Energy_Use__Kilowatt_Hours_Year__d',
            'efficiency_value_2_field': '',
            'efficiency_value_3_field': '',
            'efficiency_value_4_field': '',
            'life_field': '',
            'energy_guide_field': 'Link_to_FTC_EnergyGuide_Label_s',
            'subcategory_field': 'Product_Group_Code_Description_s',
            'additional_identifier_field': 'Total_Refrigerated_Volume__ft3__d',
        }
    }
]

def load_product_groups(PRODUCT_GROUP_CONFIGS=PRODUCT_GROUP_CONFIGS):
    
    for config in PRODUCT_GROUP_CONFIGS:
        obj, created = ProductGroup.objects.update_or_create(**config)
        
        if created:
            print(f"Created new product group: {config['name']}")
        else:
            print(f"Product group: {config['name']} already exists. Restored original values.")

    return True

if __name__ == "__main__":
    load_product_groups()

