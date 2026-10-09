"""06 - South Lokichar scenarios (model in lokichar_model.py)."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import brentq
from lokichar_model import *
D,o=run(); print({k:(round(v,2) if isinstance(v,float) else v) for k,v in o.items()}); D.round(1).to_csv('data/clean/lokichar_cashflow_base.csv',index=False)
# break-evens
be_proj=brentq(lambda b:run(brent=b)[1]['npv_project'],20,150); be_ctr=brentq(lambda b:run(brent=b)[1]['npv_contractor'],20,200); print('breakeven Brent project/contractor',round(be_proj,1),round(be_ctr,1))
# grid: price x production
prices=[50,60,70,80,90,100]; prod=[.8,.9,1.0,1.1,1.2]
G=pd.DataFrame({f'{int(f*100)}%':[run(brent=b,plateau=60*f)[1]['npv_project'] for b in prices] for f in prod},index=prices).round(0); print(G); G.to_csv('data/clean/lokichar_grid_npv_project.csv')
Gc=pd.DataFrame({f'{int(f*100)}%':[run(brent=b,plateau=60*f)[1]['npv_gov'] for b in prices] for f in prod},index=prices).round(0); Gc.to_csv('data/clean/lokichar_grid_npv_gov.csv')
# tornado on project NPV
base=o['npv_project']; T=[]
for nm,lo,hi,key in [('Oil price (Brent $55-$85)',dict(brent=55),dict(brent=85),'brent'),('Plateau output (-20%/+20% of 60 kbpd)',dict(plateau=48),dict(plateau=72),'plateau'),
    ('CAPEX (+20%/-20%)',dict(capex=7200),dict(capex=4800),'capex'),('Opex+tariff (+20%/-20%)',dict(opex=14.4,tariff=10.8),dict(opex=9.6,tariff=7.2),'opex'),('Discount rate (12%/8%)',dict(disc=.12),dict(disc=.08),'disc'),('Price differential ($10/$2)',dict(diff=10),dict(diff=2),'diff')]:
    T.append((nm,run(**lo)[1]['npv_project']-base,run(**hi)[1]['npv_project']-base))
T=pd.DataFrame(T,columns=['driver','downside','upside']); T['swing']=T.upside.abs()+T.downside.abs(); T=T.sort_values('swing'); print(T.round(0)); T.round(0).to_csv('data/clean/lokichar_tornado.csv',index=False)
# scenario table (fiscal): Brent 50/70/90, plateau 60/100
S=[]
for b in (50,70,90):
    for pl in (60,100):
        _,r=run(brent=b,plateau=pl); S.append((b,pl,r['npv_project'],r['irr_project'],r['npv_contractor'],r['irr_contractor'],r['npv_gov'],r['gov_undisc'],r['payback'],r['cum_mmbbl']))
S=pd.DataFrame(S,columns=['brent','plateau_kbpd','NPV_project','IRR_project','NPV_contractor','IRR_contractor','NPV_gov','gov_undisc','payback_year','cum_mmbbl']); print(S.round(2)); S.round(3).to_csv('data/clean/lokichar_scenarios.csv',index=False)
pd.Series({'be_proj':be_proj,'be_ctr':be_ctr}).to_csv('data/clean/lokichar_breakeven.csv')
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.5,3.3)); ax.barh(T.driver,T.downside,color='#c0392b'); ax.barh(T.driver,T.upside,color='#2e7d32'); ax.axvline(0,c='k',lw=.7)
ax.set_xlabel(f'Change in project NPV10 vs base (US$ m); base = {base:,.0f}'); fig.tight_layout(); fig.savefig('figures/f8_tornado.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.0)); ax.bar(D.year,D.mmbbl,color='#1f4e79'); ax.set_ylabel('mmbbl / year'); ax2=ax.twinx(); ax2.plot(D.year,D.pre_fiscal_cf.cumsum()/1000,c='#c0392b'); ax2.set_ylabel('Cumulative pre-fiscal cash flow, US$ bn'); fig.tight_layout(); fig.savefig('figures/f9_lokichar_profile.png',dpi=200); plt.close()

# alternative fiscal case reflecting press reports of 'enhanced cost recovery' (ASSUMED numbers): cap 80%, govt profit-oil 35%
F=[]
for nm,kw in [('Fiscal case A (cap 60%, gov profit oil 50%)',{}),('Fiscal case B (cap 80%, gov profit oil 35%)',dict(cr_cap=.80,gov_pp=.35))]:
    for b in (60,70,80):
        _,r=run(brent=b,**kw); be=brentq(lambda x:run(brent=x,**kw)[1]['npv_contractor'],20,200)
        F.append((nm,b,r['npv_contractor'],r['irr_contractor'],r['npv_gov'],r['gov_undisc'],r['gov_share_pct'],be))
F=pd.DataFrame(F,columns=['fiscal_case','brent','NPV_contractor','IRR_contractor','NPV_gov','gov_undisc','gov_share_pct','contractor_breakeven_brent']); print(F.round(2)); F.round(3).to_csv('data/clean/lokichar_fiscal_cases.csv',index=False)
