"""09 - Extended analysis: product profiles, regional price spreads, landed-cost import bill, inventory carrying cost,
energy-transition arithmetic, scenario sensitivities, South Lokichar Monte Carlo, cooking-fuel cost comparison."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *; from lokichar_model import run, BASE
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
w=load_cons().dropna(); p=load_prices(); W=w
# ---- A. product profile tables: monthly YoY and 3m avg ----
yoy=(W.pct_change(12)*100).round(1); r3=W.rolling(3).mean().round(1)
yoy.to_csv('data/clean/monthly_yoy_table.csv'); r3.to_csv('data/clean/rolling3_table.csv')
prof=[]
for pr in ['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Fuel oil/other*','Kerosene (IK)']:
    s=W[pr]; y=yoy[pr].dropna()
    prof.append((pr,s.max(),s.idxmax().strftime('%b-%y'),s.min(),s.idxmin().strftime('%b-%y'),s.mean(),s.std(),y.max(),y.min(),(y>0).mean()*100))
pd.DataFrame(prof,columns=['product','max_kt','max_month','min_kt','min_month','mean_kt','std_kt','best_yoy%','worst_yoy%','share_months_growing%']).round(1).to_csv('data/clean/product_profiles.csv',index=False)
# ---- B. regional price spreads (Nairobi max, EPRA reviews as reported; KSh/L) ----
reg=pd.DataFrame([
 ['Nairobi',214.03,217.86,191.38],['Mombasa',210.87,214.58,188.09],['Kisumu',213.69,218.08,191.63],['Nakuru',212.92,217.27,190.81],
 ],columns=['town','petrol_sep26','diesel_sep26','kerosene_sep26'])
reg2=pd.DataFrame([['Nairobi',214.25,242.92,152.78],['Mombasa',211.09,239.64,149.49],['Mandera',234.90,265.10,174.96],['Nyeri',216.12,244.93,np.nan],['Embu',215.69,244.46,154.31],['Moyale',229.10,258.86,np.nan]],columns=['town','petrol_may26','diesel_may26','kerosene_may26'])
reg2['petrol_vs_mombasa']=reg2.petrol_may26-211.09; reg2['diesel_vs_mombasa']=reg2.diesel_may26-239.64
reg2['petrol_vs_mombasa_%']=reg2.petrol_vs_mombasa/211.09*100
reg2.round(2).to_csv('data/clean/regional_spread_may26.csv',index=False); reg.to_csv('data/clean/regional_prices_sep26.csv',index=False)
sep_extra={'Mandera petrol (Sep-26)':234.68,'Mombasa petrol (Sep-26)':210.87}
sp=sep_extra['Mandera petrol (Sep-26)']-sep_extra['Mombasa petrol (Sep-26)']
pd.Series({'mandera_minus_mombasa_petrol_sep26':sp,'pct':sp/210.87*100}).to_csv('data/clean/regional_spread_sep26.csv')
# ---- C. price indices and cooking-fuel cost comparison ----
idx=(p/p.iloc[0]*100).round(1); idx.to_csv('data/clean/price_index_jan25_100.csv')
rows=[]
for lpg_eff,ch_eff in [(.55,.20),(.55,.25),(.55,.30),(.45,.30)]:
    for mon in ['2025-01-01','2026-03-01']:
        lp=p.loc[mon,'L.P.G']/13; ch=p.loc[mon,'Charcoal']
        rows.append((mon[:7],lpg_eff,ch_eff,lp/(46*lpg_eff),ch/(29*ch_eff)))
CK=pd.DataFrame(rows,columns=['month','LPG_stove_eff','charcoal_stove_eff','LPG_KSh_per_useful_MJ','charcoal_KSh_per_useful_MJ']); CK['LPG_over_charcoal']=CK.LPG_KSh_per_useful_MJ/CK.charcoal_KSh_per_useful_MJ; CK.round(2).to_csv('data/clean/cooking_cost_per_MJ.csv',index=False)
# ---- D. landed-cost import-bill illustration (constant 2026 baseline volumes) ----
S=pd.read_csv('data/clean/scenarios_kt.csv'); b26=S[(S.scenario=='Baseline')&(S.year==2026)].set_index('product').kt
FX=129.2
bill=[]
for prod,usd_m3_a,usd_m3_b,lab in [('Petrol (PMS)',582.11,874.26,'Feb-26 vs Aug-26'),('Diesel (AGO)',855.59,957.05,'Jul-26 vs Aug-26 (diesel Feb-26 landed cost not retrieved)')]:
    ml=b26[prod]*ML_PER_KT[prod]; a=ml*usd_m3_a/1000; b=ml*usd_m3_b/1000   # ML * USD/m3 /1000 = USD m
    bill.append((prod,ml,usd_m3_a,usd_m3_b,a,b,b-a,(b-a)*FX/1000,lab))
BILL=pd.DataFrame(bill,columns=['product','volume_ML_2026base','landed_a_USD_m3','landed_b_USD_m3','bill_a_USDm','bill_b_USDm','increase_USDm','increase_KShbn','comparison']).round(1); BILL.to_csv('data/clean/landed_cost_bill.csv',index=False)
# ---- E. inventory value & carrying cost of strategic stock ----
dm={'Petrol (PMS)':(W.loc['2025','Petrol (PMS)'].sum()*ML_PER_KT['Petrol (PMS)']/365,874.26),'Diesel (AGO)':(W.loc['2025','Diesel (AGO)'].sum()*ML_PER_KT['Diesel (AGO)']/365,957.05)}
inv=[]
for days in (15,30,60,90):
    val=sum(d*days*u/1000 for d,u in dm.values()); vol=sum(d*days for d,_ in dm.values())
    inv.append((days,vol,val,val*FX/1000,val*0.10,val*0.10*FX/1000))
INV=pd.DataFrame(inv,columns=['days_of_cover','volume_ML','inventory_USDm','inventory_KShbn','carry_10pct_USDm_pa','carry_10pct_KShbn_pa']).round(1); INV.to_csv('data/clean/inventory_cost.csv',index=False)
# ---- F. energy-transition arithmetic (petrol displaced, baseline 2035) ----
q35=S[(S.scenario=='Baseline')&(S.year==2035)&(S['product']=='Petrol (PMS)')].kt.iloc[0]; d35=S[(S.scenario=='Baseline')&(S.year==2035)&(S['product']=='Diesel (AGO)')].kt.iloc[0]
ET=[]
for share in (.02,.05,.10,.20):
    kt=q35*share; ml=kt*ML_PER_KT['Petrol (PMS)']; ET.append((share*100,kt,ml,ml*0.874,ml*0.874*FX/1000))
ET=pd.DataFrame(ET,columns=['petrol_displaced_%','kt','ML','import_saving_USDm_at_Aug26_landed','KShbn']).round(1); ET.to_csv('data/clean/ev_displacement.csv',index=False)
# ---- G. scenario sensitivities (2030/2035 baseline total) ----
G={'Diesel (AGO)':3.52,'Petrol (PMS)':3.35,'LPG':7.26,'Jet fuel*':1.87,'Kerosene (IK)':-4.57}
EL={'Diesel (AGO)':(-0.185,-0.570),'Petrol (PMS)':(-0.096,-0.259),'LPG':(-0.15,-0.30),'Jet fuel*':(0,0),'Kerosene (IK)':(-0.2,-0.5)}
SH={'Diesel (AGO)':20,'Petrol (PMS)':15,'LPG':10,'Jet fuel*':0,'Kerosene (IK)':20}
base25=W.loc['2025'].sum()
def total(year,fade=.8,shock=1.,elm=1.,gadd=0.):
    tot=base25['Avgas']+0
    # fuel oil follows PDP path
    q=base25['Fuel oil/other*']
    for y in range(2026,year+1): q*=1+(4.68 if y<=2027 else -3.19)/100
    tot+=q
    for pr,g in G.items():
        sr,lr=EL[pr]; sr*=elm; lr*=elm; sh=np.log(1+SH[pr]*shock/100); q=base25[pr]
        for y in range(2026,year+1):
            gg=(g+gadd)/100*(1 if y<=2029 else fade); adj=sr*sh if y==2026 else ((lr-sr)*sh/2 if y in (2027,2028) else 0)
            q*=np.exp(np.log(1+gg)+adj)
        tot+=q
    return tot
SS=[('Baseline',total(2030),total(2035))]
for nm,kw in [('Fade 0.6 (slower post-2029)',dict(fade=.6)),('Fade 1.0 (no fade)',dict(fade=1.0)),('No 2026 price shock',dict(shock=0)),('Shock x1.5',dict(shock=1.5)),('Elasticities x0.5',dict(elm=.5)),('Elasticities x2',dict(elm=2)),
              ('Underlying growth +2 pts/yr (2025 momentum)',dict(gadd=2.0)),('Underlying growth -1 pt/yr',dict(gadd=-1.0))]:
    SS.append((nm,total(2030,**kw),total(2035,**kw)))
SS=pd.DataFrame(SS,columns=['case','total_2030_kt','total_2035_kt']); SS['vs_baseline_2035_%']=(SS.total_2035_kt/SS.total_2035_kt.iloc[0]-1)*100; SS.round(1).to_csv('data/clean/scenario_sensitivity.csv',index=False); print(SS.round(1))
# ---- H. Monte Carlo on South Lokichar (project NPV10) ----
rng=np.random.default_rng(42); N=2000; out=[]
for _ in range(N):
    br=float(np.clip(rng.lognormal(np.log(70),0.22),35,140)); df=rng.uniform(3,10); pl=rng.triangular(40,60,100); cx=rng.triangular(5000,6000,8500)
    ox=rng.triangular(15,21,28); r=run(brent=br,diff=df,plateau=pl,capex=cx,opex=ox*12/21,tariff=ox*9/21)[1]
    out.append((br,df,pl,cx,ox,r['npv_project'],r['npv_contractor'],r['npv_gov']))
MC=pd.DataFrame(out,columns=['brent','diff','plateau','capex','opex_tariff','npv_project','npv_contractor','npv_gov']); MC.round(1).to_csv('data/clean/lokichar_montecarlo.csv',index=False)
q=MC[['npv_project','npv_contractor','npv_gov']].quantile([.1,.5,.9]).round(0); q.loc['P(NPV<0)']=(MC[['npv_project','npv_contractor','npv_gov']]<0).mean().round(3); q.loc['mean']=MC[['npv_project','npv_contractor','npv_gov']].mean().round(0); q.to_csv('data/clean/lokichar_mc_summary.csv'); print(q)
cor=MC.drop(columns=['npv_contractor','npv_gov']).corr()['npv_project'].drop('npv_project').round(2); cor.to_csv('data/clean/lokichar_mc_corr.csv'); print(cor)
fig,ax=plt.subplots(figsize=(7.5,3.2)); ax.hist(MC.npv_project/1000,bins=45,color='#1f4e79',alpha=.85); ax.axvline(0,c='k',lw=.8); ax.axvline(MC.npv_project.median()/1000,c='#c0392b',ls='--',label='median')
ax.set_xlabel('Project NPV10, US$ bn'); ax.set_ylabel('Draws'); ax.legend(frameon=False); fig.tight_layout(); fig.savefig('figures/f10_montecarlo.png',dpi=200); plt.close()
# ---- I. extra figures ----
R=pd.read_csv('data/clean/forecast_rolling_errors.csv'); tt=pd.read_csv('data/clean/forecast_tournament.csv'); best=tt.loc[tt.groupby('series').sMAPE.idxmin()].set_index('series').model
fig,axs=plt.subplots(1,2,figsize=(7.8,3.2))
for ax,s in zip(axs,['Diesel (AGO)','Total']):
    r=R[(R.series==s)&(R.model==best[s])&(R.h==1)]; dates=W.index[r.origin.values]
    ax.plot(W.index,W[s],c='#1f4e79',lw=1,label='actual'); ax.plot(dates,r.fc.values,'o',c='#c0392b',ms=4,label='1-month-ahead forecast'); ax.set_title(f'{s}: 1-step out-of-sample',fontsize=8.5); ax.grid(alpha=.25); ax.tick_params(labelsize=7)
axs[0].legend(frameon=False,fontsize=7); fig.autofmt_xdate(); fig.tight_layout(); fig.savefig('figures/f11_backtest.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.2)); 
for c in ['petrol','diesel','kerosene','charcoal']: pass
pi=p.rename(columns={'Motor Gasoline Premium':'Petrol','Light Diesel Oil':'Diesel','Illuminating Kerosene':'Kerosene','L.P.G':'LPG (13kg)','Charcoal':'Charcoal'}); pi=pi/pi.iloc[0]*100
for c in pi.columns: ax.plot(pi.index,pi[c],label=c)
ax.set_ylabel('Index, Jan-2025 = 100'); ax.legend(ncol=5,frameon=False,fontsize=7); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f12_price_index.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.4)); tab=W.loc['2024':'2025'].copy(); tab['m']=tab.index.month; tab['y']=tab.index.year
for pr,c in [('Diesel (AGO)','#1f4e79'),('Petrol (PMS)','#c0392b')]:
    for y,ls in [(2024,':'),(2025,'-')]:
        t=tab[tab.y==y]; ax.plot(t.m,t[pr],ls,c=c,label=f'{pr} {y}')
ax.set_xticks(range(1,13)); ax.set_xlabel('Month'); ax.set_ylabel('kt'); ax.legend(ncol=2,frameon=False,fontsize=7); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f13_seasonal_overlay.png',dpi=200); plt.close()
print(BILL.to_string()); print(INV.to_string()); print(ET.to_string()); print(CK.to_string())
