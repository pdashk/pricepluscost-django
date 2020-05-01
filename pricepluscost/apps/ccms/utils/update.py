from ccms.models import Model

from .download import download_ccms
from .serialize import transform_model_data

def update_model_data(obj, **kwargs):
    
    product_group = obj.product_group.name
    oop = obj.ccms_oop

    download = download_ccms(product_group, oop)
    
    defaults = transform_model_data(download)['defaults']

    for k,v in defaults.items():
        setattr(obj, k, v)
    obj.save()

    return True