import os, sys, django, tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricepluscost.settings")
django.setup()

from django.conf import settings
from eia.models import State
from eia.utils.upsert import upsert_series_data

EIA_SERIES = [
    ('Alabama','ELEC.PRICE.AL-RES.M'),
    ('Alaska','ELEC.PRICE.AK-RES.M'),
    ('Arizona','ELEC.PRICE.AZ-RES.M'),
    ('Arkansas','ELEC.PRICE.AR-RES.M'),
    ('California','ELEC.PRICE.CA-RES.M'),
    ('Colorado','ELEC.PRICE.CO-RES.M'),
    ('Connecticut','ELEC.PRICE.CT-RES.M'),
    ('Delaware','ELEC.PRICE.DE-RES.M'),
    ('Florida','ELEC.PRICE.FL-RES.M'),
    ('Georgia','ELEC.PRICE.GA-RES.M'),
    ('Hawaii','ELEC.PRICE.HI-RES.M'),
    ('Idaho','ELEC.PRICE.ID-RES.M'),
    ('Illinois','ELEC.PRICE.IL-RES.M'),
    ('Indiana','ELEC.PRICE.IN-RES.M'),
    ('Iowa','ELEC.PRICE.IA-RES.M'),
    ('Kansas','ELEC.PRICE.KS-RES.M'),
    ('Kentucky','ELEC.PRICE.KY-RES.M'),
    ('Louisiana','ELEC.PRICE.LA-RES.M'),
    ('Maine','ELEC.PRICE.ME-RES.M'),
    ('Maryland','ELEC.PRICE.MD-RES.M'),
    ('Massachusetts','ELEC.PRICE.MA-RES.M'),
    ('Michigan','ELEC.PRICE.MI-RES.M'),
    ('Minnesota','ELEC.PRICE.MN-RES.M'),
    ('Mississippi','ELEC.PRICE.MS-RES.M'),
    ('Missouri','ELEC.PRICE.MO-RES.M'),
    ('Montana','ELEC.PRICE.MT-RES.M'),
    ('Nebraska','ELEC.PRICE.NE-RES.M'),
    ('Nevada','ELEC.PRICE.NV-RES.M'),
    ('New Hampshire','ELEC.PRICE.NH-RES.M'),
    ('New Jersey','ELEC.PRICE.NJ-RES.M'),
    ('New Mexico','ELEC.PRICE.NM-RES.M'),
    ('New York','ELEC.PRICE.NY-RES.M'),
    ('North Carolina','ELEC.PRICE.NC-RES.M'),
    ('North Dakota','ELEC.PRICE.ND-RES.M'),
    ('Ohio','ELEC.PRICE.OH-RES.M'),
    ('Oklahoma','ELEC.PRICE.OK-RES.M'),
    ('Oregon','ELEC.PRICE.OR-RES.M'),
    ('Pennsylvania','ELEC.PRICE.PA-RES.M'),
    ('Rhode Island','ELEC.PRICE.RI-RES.M'),
    ('South Carolina','ELEC.PRICE.SC-RES.M'),
    ('South Dakota','ELEC.PRICE.SD-RES.M'),
    ('Tennessee','ELEC.PRICE.TN-RES.M'),
    ('Texas','ELEC.PRICE.TX-RES.M'),
    ('Utah','ELEC.PRICE.UT-RES.M'),
    ('Vermont','ELEC.PRICE.VT-RES.M'),
    ('Virginia','ELEC.PRICE.VA-RES.M'),
    ('Washington','ELEC.PRICE.WA-RES.M'),
    ('West Virginia','ELEC.PRICE.WV-RES.M'),
    ('Wisconsin','ELEC.PRICE.WI-RES.M'),
    ('Wyoming','ELEC.PRICE.WY-RES.M'),
    ('District of Columbia','ELEC.PRICE.DC-RES.M'),
    ('United States','ELEC.PRICE.US-RES.M'),
]

def download_states(EIA_SERIES=EIA_SERIES):
    
    for series in tqdm.tqdm(EIA_SERIES):
    
        loaded = upsert_series_data(
            EIA_API_KEY=settings.EIA_API_KEY, 
            name=series[0],
            series_id=series[1]
            )
        
        if not loaded:
            print(f"There was an error loading {series}")

if __name__ == "__main__":
    download_states()