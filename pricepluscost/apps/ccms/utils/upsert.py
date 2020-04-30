from ccms.models import BrandName, Model

from .serialize import transform_model_data

def upsert_brand(brand_name):
    '''
    Creates brand entry if it does not exist. Does nothing if it does.
    Returns brand_id
    '''

    obj, created = BrandName.objects.get_or_create(name=brand_name)
    
    return(obj)
    
def upsert_model(data, auto_upsert_brand=True):
    '''
    Given transformed output from ccms.utils.serialize, upserts into Django (unique on ccms_oop)
    Will lookup brand_id and if does not exist will automatically create brand entry or raise exception.
    Output is True is successful.
    '''
    try:
        brand_name = data['brand_name']
        brand = BrandName.objects.get(name=brand_name)
    except:
        if auto_upsert_brand:
            brand = upsert_brand(brand_name)
        else:
            raise Exception("Brand name does not exist in our records. Please create this entry first or select auto_upsert_brand=True")
    
    ccms_oop = data['ccms_oop']

    defaults = data['defaults']
    defaults['brand_name'] = brand

    obj, created = Model.objects.update_or_create(ccms_oop=ccms_oop, defaults=defaults)

    return True