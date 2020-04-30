import requests, json
from logzero import logger

def download_ccms(product_group, oop=None):
    base_url = "https://www.regulations.doe.gov/certification-data/solr/ccms/select"
    headers = {"rows" : 20000, "wt": "json", "q": f'Product_Group_s:"{product_group}"',}

    if oop:
        headers['fq'] = f'{{!tag=oop}}oop:"{oop}"'

    query_url = requests.Request("GET", base_url, params=headers).prepare().url
    r = requests.get(query_url).json()

    try:
        docs = r["response"]['docs']
        
        if len(docs) == 0:
            logger.warning("No results were found. Check query.")
        else:
            if oop:
                message_bit = f"data for oop: {oop}"
                docs = docs[0]
            else:
                message_bit = f"data for {len(docs)} products"

            logger.info(f"Successfully downloaded {message_bit}!")
            
            return(docs)

    except:
        err = r['error']['msg']
        logger.warning(err)