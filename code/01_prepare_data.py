"""01 - Load, validate, and reconcile LeadAfrik consumption data against independent sources."""
import pandas as pd, numpy as np
RAW='data/raw/'
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
c=pd.read_csv(RAW+'leadafrik-consumption-of-petroleum-fuels-kenya-monthly.csv')
c=c.dropna(subset=['month']).copy()
c['year']=c.year.astype(int); c['m']=c.month.map({m:i+1 for i,m in enumerate(MONTHS)})
c['date']=pd.to_datetime(dict(year=c.year,month=c.m,day=1))
c['provisional']=c.provisional.eq('Yes')
c=c.rename(columns={'fuel_type':'label_as_published','consumption_volume':'kt'})
assert len(c)==189 and c.groupby('label_as_published').size().eq(27).all()
print('dupes',c.duplicated(['date','label_as_published']).sum(),'missing',c.kt.isna().sum(), c[c.kt.isna()].date.dt.strftime('%Y-%m').unique())
w=c.pivot(index='date',columns='label_as_published',values='kt')
s24=w.loc['2024'].sum(); s25=w.loc['2025'].sum()
print(pd.DataFrame({'2024':s24,'2025':s25}).round(1), s24.sum(), s25.sum())
pdp24={'AGO':2193.6,'PMS':1472.7,'LPG':414.9,'IK':37.1,'JET':765.1,'FO':301.9}
M=pd.DataFrame({p:{col:(s24[col]-v)/v*100 for col in w.columns} for p,v in pdp24.items()}).round(1)
print(M)
# ---- save analysis-ready relabelled dataset and reconciliation table ----
import sys; sys.path.insert(0,'code')
from common import load_cons
W=load_cons(); W.round(3).to_csv('data/clean/consumption_relabelled_kt.csv')
rec=pd.DataFrame({'2024_kt':W.loc['2024'].sum(),'2025_kt':W.loc['2025'].sum()}).round(1)
rec['reference_2024']=pd.Series({'Diesel (AGO)':2193.6,'Petrol (PMS)':1472.7,'LPG':414.9,'Kerosene (IK)':37.1,'Jet fuel*':765.1,'Fuel oil/other*':301.9})
rec['reference_2025_KNBS']=pd.Series({'Diesel (AGO)':2419.1,'LPG':475.9,'Total':5700.0})
rec['err_2024_%']=((rec['2024_kt']/rec.reference_2024-1)*100).round(1); rec.to_csv('data/clean/reconciliation.csv'); print(rec)
print('diesel+petrol share 2025 %:',round((W.loc['2025','Diesel (AGO)'].sum()+W.loc['2025','Petrol (PMS)'].sum())/W.loc['2025','Total'].sum()*100,1))
