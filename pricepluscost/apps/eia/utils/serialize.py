from datetime import datetime, timedelta

from .download import get_rates_for_series

# https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
def _last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def transform_series_data(series_id, **kwargs):
    '''
    Given API KEY and series id, downloads electricity rates and performs transformations for loading into eia app
    Output is list of dictionaries with arguments the same as model fields, except "name" and "series_id"
    '''
    download = get_rates_for_series(series_id)

    rolling = download['data'][:12]
    rates = [r for [d,r] in rolling]
    
    iso3166 = download['iso3166']
    rolling_average = round(sum(rates)/len(rates), 5)
    average_start_date = datetime.strptime(rolling[-1][0], '%Y%m')
    average_end_date = _last_day_of_month(datetime.strptime(rolling[0][0], '%Y%m'))  
    source_update_date = datetime.strptime(download['updated'],'%Y-%m-%dT%H:%M:%S%z')
    
    output = {
        'iso3166': iso3166,
        'rolling_average' : rolling_average,
        'average_start_date': average_start_date,
        'average_end_date': average_end_date,
        'source_update_date': source_update_date,
        } 
            
    return(output)