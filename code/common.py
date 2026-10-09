import pandas as pd, numpy as np
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
# Relabelling established in 01_prepare_data.py (exact reconciliation to EPRA PDP 2024 actuals / KNBS 2025)
RELABEL={'AGO (Light Diesel Oil)':'Diesel (AGO)','LPG':'Petrol (PMS)','Other':'LPG',
         'Illuminating Kerosene':'Kerosene (IK)','Aviation Gasoline':'Avgas',
         'Motor Spirit':'Jet fuel*','Jet Oil':'Fuel oil/other*'}
PRODUCTS=['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Fuel oil/other*','Kerosene (IK)','Avgas']
# kt -> million litres: factors implied by EPRA PDP 2025-29 (million litres / kt, 2024 base)
ML_PER_KT={'Diesel (AGO)':2608.20/2193.6,'Petrol (PMS)':2044.11/1472.7,'Jet fuel*':972.49/765.1,'Kerosene (IK)':47.17/37.1}
def load_cons():
    c=pd.read_csv('data/raw/leadafrik-consumption-of-petroleum-fuels-kenya-monthly.csv').dropna(subset=['month'])
    c['date']=pd.to_datetime(dict(year=c.year.astype(int),month=c.month.map({m:i+1 for i,m in enumerate(MONTHS)}),day=1))
    c['product']=c.fuel_type.map(RELABEL); c['kt']=c.consumption_volume
    w=c.pivot(index='date',columns='product',values='kt')[PRODUCTS]
    w['Total']=w[PRODUCTS].sum(axis=1,min_count=7)
    return w
def load_prices():
    p=pd.read_csv('data/raw/leadafrik-national-average-retail-prices-for-selected-fuels-in-kenya.csv').dropna(subset=['month'])
    p['date']=pd.to_datetime(dict(year=p.year.astype(int),month=p.month.map({m:i+1 for i,m in enumerate(MONTHS)}),day=1))
    return p.pivot(index='date',columns='fuel_type',values='average_retail_price')
