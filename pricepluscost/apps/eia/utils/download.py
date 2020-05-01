import requests
from logzero import logger
from django.conf import settings

API_KEY = settings.EIA_API_KEY

def get_all_monthly_res_series(verbose=False):
    base_url = 'http://api.eia.gov/category/?api_key={API_KEY}&category_id={category_id}'
    category_id = '1012' # a different id will get other series that are not monthly residential
    query_url = base_url.format(API_KEY=API_KEY, category_id=category_id)
    r = requests.get(query_url).json()
    try:
        results = r['category']['childseries']
        results_m = [result for result in results if result['f'] == 'M']
        if verbose:
            logger.info(f"Collected monthly residential data from EIA.gov ({len(results_m)} different series collected).")
        return(results_m)
    except:
        err = r['data']['error']
        logger.warning(err)

def get_rates_for_series(series_id, verbose=False):
    base_url = 'http://api.eia.gov/series/?api_key={API_KEY}&series_id={series_id}'
    query_url = base_url.format(API_KEY=API_KEY, series_id=series_id)
    r = requests.get(query_url).json()
    try:
        results = r['series'][0]
        if verbose:
            logger.info(f"Completed retail price collection from EIA.gov for series: {series_id}. Collected {len(results['data'])} datapoints lasted updated {results['updated']}")
        return(results)
    except:
        err = r['data']['error']
        logger.warning(err)