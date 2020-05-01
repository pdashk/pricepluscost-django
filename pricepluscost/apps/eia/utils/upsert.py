from eia.models import State

from .serialize import transform_series_data

def upsert_series_data(name, series_id=None, **kwargs):
    '''
    Given API KEY and name, with optional series id, downloads electricity rates, performs transformations for loading into eia app, then upserts data
    If series id not provided, then will look it up in objects. If not in objects, will raise exception.
    If series id is provided, then it will upsert, including the series_id field.
    Output is True is successful.
    '''
    if not series_id:
        try:
            series_id = State.objects.get(name=name).series_id
        except:
            raise Exception("Name could not be found. Please include a series id or check name entries.")
    
    defaults = transform_series_data(series_id)

    defaults['series_id'] = series_id

    obj, created = State.objects.update_or_create(name=name, defaults=defaults)

    return True