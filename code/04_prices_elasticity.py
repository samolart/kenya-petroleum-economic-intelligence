"""04 - Price analytics, elasticity (own estimate + PDP-implied) and landed-cost pass-through."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *
w=load_cons(); p=load_prices(); print(p.round(2).to_string())
pr=p.rename(columns={'Motor Gasoline Premium':'petrol','Light Diesel Oil':'diesel','Illuminating Kerosene':'kerosene','L.P.G':'lpg13','Charcoal':'charcoal'})
pr['lpg_kg']=pr.lpg13/13; pr['lpg_charcoal_ratio']=pr.lpg_kg/pr.charcoal
stats=pd.DataFrame({'min':pr.min(),'max':pr.max(),'mean':pr.mean(),'cv%':pr.std()/pr.mean()*100,'chg_%_Jan25_Mar26':(pr.iloc[-1]/pr.iloc[0]-1)*100}).round(2); print(stats); stats.to_csv('data/clean/price_stats.csv')
print('distinct petrol/diesel price levels:',pr.petrol.nunique(),pr.diesel.nunique())
# ---- own log-log estimate, OLS with Newey-West(2) SE ----
def ols(y,X,lag=2):
    X=np.column_stack([np.ones(len(y)),X]); b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b; n,k=X.shape
    S=(X*e[:,None]).T@(X*e[:,None])
    for L in range(1,lag+1):
        G=(X[L:]*e[L:,None]).T@(X[:-L]*e[:-L,None]); S+=(1-L/(lag+1))*(G+G.T)
    XtXi=np.linalg.inv(X.T@X); V=XtXi@S@XtXi*n/(n-k); se=np.sqrt(np.diag(V)); return b,se,e
res=[]
for prod,col in [('Diesel (AGO)','diesel'),('Petrol (PMS)','petrol')]:
    d=pd.concat([np.log(w[prod]).rename('q'),np.log(pr[col]).rename('p')],axis=1).dropna()
    t=np.arange(len(d)); m=np.array([(i+1) in () for i in range(len(d))])
    b,se,e=ols(d.q.values,np.column_stack([d.p.values,t]))
    res.append((prod,len(d),b[1],se[1],b[1]-1.96*se[1],b[1]+1.96*se[1],b[2]*12*100))
    print(prod,len(d),'price elasticity',round(b[1],2),'NW se',round(se[1],2))
E_=pd.DataFrame(res,columns=['product','n','elasticity','se_NW','lo95','hi95','trend_%pa']).round(2); E_.to_csv('data/clean/own_elasticity.csv',index=False); print(E_)
# ---- PDP-implied elasticities (EPRA PDP 2025-29, Section 3.4; base-year 2024 values) ----
pdp=pd.DataFrame([
 ['Petrol (PMS)',-1.0243,191.8,2044.11,0.6284],
 ['Diesel (AGO)',-2.7057,178.30,2608.20,0.6754]],columns=['product','coef_ML_per_KSh','price24','q24_ML','lag_coef'])
pdp['SR_elasticity']=pdp.coef_ML_per_KSh*pdp.price24/pdp.q24_ML; pdp['LR_elasticity']=pdp.SR_elasticity/(1-pdp.lag_coef)
print(pdp.round(3)); pdp.round(3).to_csv('data/clean/pdp_implied_elasticity.csv',index=False)
# ---- landed cost -> pump pass-through (petrol), Nairobi max pump price vs EPRA landed cost (USD/m3) ----
# EPRA review text: Feb-2026 landed 582.11 (price cycle 15 Mar-14 Apr: Nairobi petrol 178.28, diesel 166.54);
# Aug-2026 landed petrol 874.26 / diesel 957.05 (cycle 15 Sep-14 Oct: petrol 214.03, diesel 217.86)
# diesel Feb-2026 landed not retrieved -> petrol only. FX assumption 129.2 KSh/USD (flat), sensitivity 125-135.
lc0,lc1=582.11,874.26; pp0,pp1=178.28,214.03
rows=[]
for fx in (125,129.2,135):
    dl=(lc1-lc0)/1000*fx; dp=pp1-pp0
    rows.append((fx,dl,dl*1.16,dp,dp/dl,dp/(dl*1.16)))
PT=pd.DataFrame(rows,columns=['USDKES','landed_change_KSh_L','landed_change_incl_VAT','pump_change','passthrough_ex_VAT','passthrough_vs_VAT_inclusive']).round(2); print(PT); PT.to_csv('data/clean/passthrough.csv',index=False)
# ---- Post-March 2026 pump price path (Nairobi, news reports of EPRA reviews) ----
path=pd.DataFrame([['Mar-26 cycle (15 Mar-14 Apr)',178.28,166.54,152.78],['May-26 cycle (15 May-14 Jun)',214.25,242.92,152.78],
   ['Jul-26 cycle (15 Jul-14 Aug)',214.03,222.86,191.38],['Aug-26 cycle (15 Aug-14 Sep)',214.03,217.86,191.38],['Sep-26 cycle (15 Sep-14 Oct)',214.03,217.86,191.38]],
   columns=['cycle','petrol','diesel','kerosene']); path.to_csv('data/clean/pump_path_2026.csv',index=False)
fig,ax=plt.subplots(figsize=(7.5,3.4)); 
ax.plot(pr.index,pr.petrol,'o-',label='Petrol (LeadAfrik national avg)',c='#1f4e79'); ax.plot(pr.index,pr.diesel,'o-',label='Diesel',c='#c0392b')
d2=pd.to_datetime(['2026-03-15','2026-05-15','2026-07-15','2026-08-15','2026-09-15'])
ax.plot(d2,path.petrol,'s--',c='#1f4e79',alpha=.7,label='Petrol (Nairobi max, EPRA via press)'); ax.plot(d2,path.diesel,'s--',c='#c0392b',alpha=.7,label='Diesel (Nairobi max)')
ax.axvline(pd.Timestamp('2026-02-28'),c='grey',ls=':'); ax.text(pd.Timestamp('2026-03-02'),245,'Gulf war\n28 Feb 2026',fontsize=7)
import matplotlib.dates as mdates; ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3)); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%y')); ax.set_ylabel('KSh per litre'); ax.legend(frameon=False,fontsize=7,loc='upper left'); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f5_prices.png',dpi=200); plt.close()
