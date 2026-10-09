import pandas as pd, json, numpy as np
D='/tmp/claude-0/-home-claude/ea50cc6e-6bb1-50b3-8527-5bdf9fcfc6e6/scratchpad/repo/data/clean/'
r=lambda f,**k: pd.read_csv(D+f+'.csv',**k)
def nn(x):
    if isinstance(x,float): return None if np.isnan(x) else round(x,3)
    return x
def recs(df): return [{k:nn(v) for k,v in row.items()} for row in df.to_dict('records')]
c=r('consumption_relabelled_kt').dropna(subset=['Total'])
cons={'dates':c['date'].tolist(),'series':{k:[nn(v) for v in c[k]] for k in c.columns if k!='date'}}
seas=r('seasonal_index')
f=r('forecast_12m')
fc={}
for s,g in f.groupby('series'): fc[s]={'model':g.model.iloc[0],'rows':recs(g[['date','fc','lo80','hi80','lo95','hi95']])}
sc=r('scenarios_kt')
scen={}
for (s,p),g in sc.groupby(['scenario','product']): scen.setdefault(s,{})[p]={int(y):round(v,1) for y,v in zip(g.year,g.kt)}
ds=r('demand_summary').rename(columns={'Unnamed: 0':'product'})
rs=r('risk_scores').rename(columns={'Unnamed: 0':'product'})
grid=r('lokichar_grid_npv_project').rename(columns={'Unnamed: 0':'brent'})
mc=r('lokichar_montecarlo')
h,e=np.histogram(mc.npv_project,bins=36)
mcs=r('lokichar_mc_summary').rename(columns={'Unnamed: 0':'stat'})
out=dict(cons=cons,seas=recs(seas),fc=fc,scen=scen,ds=recs(ds),risk=recs(rs),
 price=recs(r('price_index_jan25_100')),pump=recs(r('pump_path_2026')),reg=recs(r('regional_spread_may26')),
 cover=recs(r('reported_cover')),gap=recs(r('stock_gap')),cap=recs(r('security_capacity')),
 lpg=recs(r('lpg_storage')),grid=recs(grid),tor=recs(r('lokichar_tornado')),
 lsc=recs(r('lokichar_scenarios')),mchist={'counts':h.tolist(),'edges':[round(x) for x in e]},mcs=recs(mcs),
 sens=recs(r('scenario_sensitivity')),tour=recs(r('forecast_tournament')),pt=recs(r('passthrough')),
 prof=recs(r('product_profiles')))
json.dump(out,open('data.json','w'),separators=(',',':'))
import os;print(os.path.getsize('data.json'))
print(r('lokichar_cashflow_base').head(3)); print(mc.npv_project.describe())
print(r('price_index_jan25_100').tail(2)); print(c.tail(2))
