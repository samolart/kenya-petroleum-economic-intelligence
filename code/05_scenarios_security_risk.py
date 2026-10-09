"""05 - Scenario projections 2025-2035, supply security (days of cover, storage), risk framework."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *
w=load_cons(); base25=w.loc['2025'].sum()   # kt, actual 2025 (LeadAfrik, reconciled)
PR=['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Kerosene (IK)']
# PDP 2025-29 average annual growth by scenario (baseline, optimistic, pessimistic), % - EPRA PDP 2025-2029 Section 4.2
G={'Diesel (AGO)':(3.52,4.28,2.74),'Petrol (PMS)':(3.35,4.08,2.97),'LPG':(7.26,8.82,6.34),'Jet fuel*':(1.87,2.17,1.70),'Kerosene (IK)':(-4.57,-3.86,-5.29)}
FADE=0.8        # ASSUMPTION: 2030-35 growth = 0.8 x the 2025-29 rate (maturing motorisation, e-mobility, slower LPG uptake)
# 2026 price shock (average pump-price rise vs 2025 average, %) by scenario [High-demand, Baseline, Low-demand]: ASSUMPTIONS informed by Mar-Sep 2026 EPRA reviews
SHOCK={'Diesel (AGO)':(10,20,30),'Petrol (PMS)':(8,15,22),'LPG':(5,10,20),'Jet fuel*':(0,0,0),'Kerosene (IK)':(10,20,30)}
# elasticities: PDP-implied (diesel, petrol); assumption for others (LPG -0.15 SR/-0.30 LR; kerosene -0.2/-0.5; jet 0)
EL={'Diesel (AGO)':(-0.185,-0.570),'Petrol (PMS)':(-0.096,-0.259),'LPG':(-0.15,-0.30),'Jet fuel*':(0,0),'Kerosene (IK)':(-0.2,-0.5)}
SC={'High-demand':1,'Baseline':0,'Low-demand':2}   # index into G (opt=1, base=0, pess=2)
SH={'High-demand':0,'Baseline':1,'Low-demand':2}
years=list(range(2025,2036)); rows=[]
for sc in SC:
    for p in PR:
        sr,lr=EL[p]; shock=np.log(1+SHOCK[p][SH[sc]]/100); q=base25[p]
        rows.append((sc,p,2025,q))
        for y in years[1:]:
            g=G[p][SC[sc]]/100*(1 if y<=2029 else FADE)
            adj=0
            if y==2026: adj=sr*shock
            elif y in (2027,2028): adj=(lr-sr)*shock/2    # remainder of long-run response phased over 2 years
            q=q*np.exp(np.log(1+g)+adj); rows.append((sc,p,y,q))
# fuel oil/other (label uncertain) follows PDP path: + to 2027 then decline; avgas held flat at 2025 level
FO={'High-demand':(4.95,-3.13),'Baseline':(4.68,-3.19),'Low-demand':(4.44,-3.26)}
for sc in SC:
    q=base25['Fuel oil/other*']; rows.append((sc,'Fuel oil/other*',2025,q))
    for y in years[1:]:
        q*=1+(FO[sc][0] if y<=2027 else FO[sc][1])/100; rows.append((sc,'Fuel oil/other*',y,q))
    for y in years: rows.append((sc,'Avgas',y,base25['Avgas']))
S=pd.DataFrame(rows,columns=['scenario','product','year','kt']); S.to_csv('data/clean/scenarios_kt.csv',index=False)
tab=S[S.year.isin([2025,2026,2030,2035])].pivot_table(index=['scenario','product'],columns='year',values='kt').round(0); print(tab)
tot=S.groupby(['scenario','year']).kt.sum().unstack().round(0); print(tot)
# no-shock reference (PDP baseline growth only)
# supply security -------------------------------------------------------
ML={k:v for k,v in ML_PER_KT.items()}
dem26={p:S[(S.scenario=='Baseline')&(S['product']==p)&(S.year==2026)].kt.iloc[0] for p in PR}
dem25=base25
daily_ML={}
for p in ['Diesel (AGO)','Petrol (PMS)','Jet fuel*']:
    daily_ML[p]=dem25[p]*ML[p]/365
CAP={'Diesel (AGO)':755.04,'Petrol (PMS)':462.60,'Jet fuel*':231.84,'Kerosene (IK)':52.77}   # PDP Table 5.7, gross licensed tank capacity (ML), Mar 2025
rows=[]
for p in ['Diesel (AGO)','Petrol (PMS)','Jet fuel*']:
    d=daily_ML[p]; rows.append((p,d,CAP[p],CAP[p]/d,30*d,15*d))
SEC=pd.DataFrame(rows,columns=['product','daily_demand_ML(2025)','gross_capacity_ML','gross_days_if_full','ML_for_30d_cover','ML_for_15d_operational']).round(1); print(SEC); SEC.to_csv('data/clean/security_capacity.csv',index=False)
# reported stock cover (days): official/press statements, 2026 (see report for sources)
REP=pd.DataFrame([['Petrol (PMS)',16,13,28],['Diesel (AGO)',19,16,23],['Jet fuel*',49,46,None]],columns=['product','Treasury/MoE ~Apr 2 (days)','MoE report adj. ~Apr 2 (days)','EPRA 21 May (days)']); REP.to_csv('data/clean/reported_cover.csv',index=False)
gap=[]
for p,lo,hi in [('Petrol (PMS)',13,28),('Diesel (AGO)',16,23)]:
    d=daily_ML[p]; gap.append((p,lo,hi,30-hi,30-lo,(30-hi)*d,(30-lo)*d))
GAP=pd.DataFrame(gap,columns=['product','days_low','days_high','shortfall_days_min','shortfall_days_max','shortfall_ML_min','shortfall_ML_max']).round(1); print(GAP); GAP.to_csv('data/clean/stock_gap.csv',index=False)
# LPG storage (PDP method: required storage = planned supply/12, planned supply = demand*(1+30/365))
cap_lpg=44.43; lp=[]
for sc in SC:
    for y in (2025,2026,2027,2028,2029,2030):
        d=S[(S.scenario==sc)&(S['product']=='LPG')&(S.year==y)].kt.iloc[0]; req=d*(1+30/365)/12; lp.append((sc,y,d,req,cap_lpg-req))
LPGS=pd.DataFrame(lp,columns=['scenario','year','demand_kt','required_storage_kt','headroom_kt']).round(1); print(LPGS[LPGS.scenario=='Baseline']); LPGS.to_csv('data/clean/lpg_storage.csv',index=False)
# PDP backtest
bt=pd.DataFrame({'PDP_2025_fc_kt':{'Petrol (PMS)':1554.0,'Diesel (AGO)':2297.6,'LPG':446.2,'Total':5425.5},'Actual_2025_kt':{'Petrol (PMS)':base25['Petrol (PMS)'],'Diesel (AGO)':base25['Diesel (AGO)'],'LPG':base25['LPG'],'Total':base25['Total']}})
bt['error_%']=(bt.Actual_2025_kt/bt.PDP_2025_fc_kt-1)*100; print(bt.round(1)); bt.round(1).to_csv('data/clean/pdp_backtest.csv')
# risk framework --------------------------------------------------------
cv={'Diesel (AGO)':7.3,'Petrol (PMS)':9.2,'LPG':10.7,'Jet fuel*':5.6}
fe={'Diesel (AGO)':2.75,'Petrol (PMS)':3.50,'LPG':3.09,'Jet fuel*':3.55}       # best sMAPE from tournament
cover={'Diesel (AGO)':19,'Petrol (PMS)':16,'LPG':np.nan,'Jet fuel*':49}          # lowest official-ish April figure; LPG not reported
price={'Diesel (AGO)':30.8,'Petrol (PMS)':20.0,'LPG':np.nan,'Jet fuel*':np.nan}  # Mar->Sep 2026 pump change; LPG/jet not regulated/observed
infra={'Diesel (AGO)':1,'Petrol (PMS)':1,'LPG':4,'Jet fuel*':1}                  # PDP: adequate storage except LPG (needs capacity by 2027)
conc={'Diesel (AGO)':4,'Petrol (PMS)':4,'LPG':4,'Jet fuel*':3}                   # reliance on Gulf-origin supply (G-to-G for petrol/diesel); judgement
def rk(v,lo,hi,rev=False):
    x=np.clip((v-lo)/(hi-lo),0,1); return 1+4*(1-x if rev else x)
R=pd.DataFrame(index=list(cv))
R['Demand volatility']=[rk(cv[p],5,12) for p in R.index]
R['Forecast uncertainty']=[rk(fe[p],2.0,6.0) for p in R.index]
R['Stock cover']=[rk(cover[p],10,30,True) if not np.isnan(cover[p]) else 4.0 for p in R.index]   # LPG: no published cover -> 4 (data gap penalty)
R['Price shock']=[rk(price[p],0,30) if not np.isnan(price[p]) else 3.0 for p in R.index]           # unobserved -> neutral 3
R['Infrastructure gap']=[infra[p] for p in R.index]; R['Supply concentration']=[conc[p] for p in R.index]
W1={'Stock cover':.25,'Price shock':.20,'Infrastructure gap':.15,'Demand volatility':.15,'Supply concentration':.15,'Forecast uncertainty':.10}
Weq={k:1/6 for k in W1}; Wst={'Stock cover':.4,'Price shock':.2,'Infrastructure gap':.1,'Demand volatility':.1,'Supply concentration':.1,'Forecast uncertainty':.1}
for nm,wt in [('Score (base weights)',W1),('Score (equal)',Weq),('Score (stock-heavy)',Wst)]: R[nm]=sum(R[k]*v for k,v in wt.items())
R['Rating']=pd.cut(R['Score (base weights)'],[0,2.4,3.2,5],labels=['LOW','MEDIUM','HIGH']); print(R.round(2).to_string()); R.round(2).to_csv('data/clean/risk_scores.csv')
# figures
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.5,3.6)); col={'High-demand':'#2e7d32','Baseline':'#1f4e79','Low-demand':'#c0392b'}
for sc in SC: ax.plot(tot.columns,tot.loc[sc]/1000,'o-',ms=3,c=col[sc],label=sc)
ax.fill_between(tot.columns,tot.loc['Low-demand']/1000,tot.loc['High-demand']/1000,color='grey',alpha=.12)
ax.set_ylabel('Million tonnes'); ax.legend(frameon=False); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f6_scenarios.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.2)); 
for sc in SC: ax.plot(LPGS[LPGS.scenario==sc].year,LPGS[LPGS.scenario==sc].required_storage_kt,'o-',c=col[sc],label=sc)
ax.axhline(cap_lpg,c='k',ls='--'); ax.text(2025.05,cap_lpg+.7,'Installed LPG storage Mar-2025: 44.43 kt (PDP)',fontsize=7)
ax.set_ylabel('Required LPG storage, kt'); ax.legend(frameon=False); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f7_lpg_storage.png',dpi=200); plt.close()
