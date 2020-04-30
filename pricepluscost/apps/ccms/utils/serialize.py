from ccms.models import BrandName, ProductGroup


def transform_model_data(data):
    '''
    Given the json output from data download of a single product, will create the defaults (minus Brand) dictionary for Django object creation.
    If product_group does not exist in Django database, then will raise exception.
    
    Uses the '_fields' in ProductGroup object to map to Django model object fields.
    If field is blank, will skip adding to dictionary.
    For CCMS, if there is no value (e.g., for FTC label URL), then the API will not return that key in the JSON blob.
    These keys must produce blank ('') or else None will break other parts. ('' is more accurate than None, where None implies we did not try to search it.)
    Mandatory keys (e.g., model_number) will raise error upon upsertion if not found in CCMS record.
    
    Output will be dictionary with two keys: 
        "brand_name" is the character brand name (to be mapped to foreign key),
        "defaults" the dictionary used for upserting the Django object.
    '''

    try:
        product_group = data['Product_Group_s'] # this field must work, or else our download would not work
        p = ProductGroup.objects.get(name=product_group)
    except:
        raise Exception("Product group does not exist in our records. Please create this entry first.")  
    
    output = {
        'ccms_oop': data['oop'],
        'brand_name': data[p.brand_name_field],
        'defaults': {'product_group': p}
    }

    lookup_fields = [
        'subcategory',
        'additional_identifier',
        'model_number',
        'efficiency_value_1',
        'efficiency_value_2',
        'efficiency_value_3',
        'efficiency_value_4',
        'life',
        'energy_guide',
        ]

    for field in lookup_fields:

        key = f"{field}_field"
        ccms_field = getattr(p, key)

        if ccms_field is not '':
            try:
                output['defaults'][field] = data[ccms_field]
            except:
                output['defaults'][field] = ''

    return(output)