import os, sys, django, tqdm
from logzero import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricepluscost.settings")
django.setup()

from ccms.models import ProductGroup, Model

from ccms.utils.download import download_ccms
from ccms.utils.serialize import transform_model_data
from ccms.utils.upsert import upsert_model

product_groups = ProductGroup.objects.all().values_list('name', flat=True) 

def download_models(product_groups=product_groups):
    
    for group in product_groups:
        logger.info(f"Starting model downloads for {group}...")
        
        download = download_ccms(group)

        logger.info(f"Starting upsert to Django...")
        loads = []

        for record in tqdm.tqdm(download):
            loaded = upsert_model(transform_model_data(record))
            loads.append(loaded)

            if not loaded:
                logger.warning(f"There was an error loading a record (OOP: {record['oop']})")

        logger.info(f"Successfully loaded {sum(loads)}/{len(download)} models for {group}")

if __name__ == "__main__":
    download_models()