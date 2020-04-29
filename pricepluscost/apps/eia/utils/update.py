from eia.models import State

from .serialize import transform_series_data

def update_state_data(EIA_API_KEY, obj, **kwargs):
    '''
    Given API KEY and State object, downloads electricity rates, performs transformations, then updates object with new data
    All fields except for "name" and "series" are updated.
    Output is True is successful.
    '''

    series_id = obj.series_id
 
    defaults = transform_series_data(EIA_API_KEY, series_id)

    for k,v in defaults.items():
        setattr(obj, k, v)
    obj.save()

    return True