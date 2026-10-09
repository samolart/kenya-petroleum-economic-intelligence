"""03 - Forecasting tournament (rolling-origin) on 26 monthly observations. No statsmodels available: models implemented with numpy/scipy."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import minimize
from common import *
w=load_cons().dropna(); SERIES=['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Total']
def f_naive(y,h): return np.repeat(y[-1],h)
def f_mean6(y,h): return np.repeat(y[-6:].mean(),h)
def f_drift(y,h):
    d=(y[-1]-y[0])/(len(y)-1); return y[-1]+d*np.arange(1,h+1)
def f_snaive(y,h): return np.array([y[-12+((i)%12)] for i in range(h)])
def f_snaive_g(y,h):
    # seasonal naive scaled by YoY growth of the latest 6 months vs same months a year earlier
    g=y[-6:].sum()/y[-18:-12].sum(); return f_snaive(y,h)*g
def f_ets(y,h):  # damped additive trend, SSE-fit
    def run(p):
        a,b,ph=p; l,tr=y[0],y[1]-y[0]; sse=0
        for v in y[1:]:
            f=l+ph*tr; e=v-f; sse+=e*e; ln=f+a*e; tr=ph*tr+b*(ln-l-ph*tr)*1.0 if False else ph*tr+a*b*e; l=ln
        return sse,l,tr
    r=minimize(lambda p:run(p)[0],[.3,.1,.9],bounds=[(.01,1),(.01,1),(.8,.98)],method='L-BFGS-B')
    _,l,tr=run(r.x); ph=r.x[2]; return np.array([l+sum(ph**j for j in range(1,k+1))*tr for k in range(1,h+1)])
def f_arima011(y,h):  # ARIMA(0,1,1) with no drift, CSS
    d=np.diff(y)
    def css(th):
        e=0;s=0
        for x in d: e=x-th[0]*e; s+=e*e
        return s
    th=minimize(css,[-.3],bounds=[(-.95,.95)],method='L-BFGS-B').x[0]
    e=0
    for x in d: e=x-th*e
    f=np.empty(h); f[0]=y[-1]+th*e; f[1:]=f[0]; return f
def f_trend_seas(y,h):  # log-linear trend + month-of-year ratio (needs >=12 obs; ratios from available months)
    n=len(y); t=np.arange(n); b=np.polyfit(t,np.log(y),1); res=np.log(y)-np.polyval(b,t)
    sidx=np.array([res[i::12].mean() if len(res[i::12]) else 0 for i in range(12)]); sidx-=sidx.mean()
    # month position: origin index i%12 matches calendar position because series starts in January
    return np.array([np.exp(np.polyval(b,n+k)+sidx[(n+k)%12]*0.5) for k in range(h)])  # seasonal effect shrunk 50%
MODELS={'Naive':f_naive,'Mean (last 6m)':f_mean6,'Drift':f_drift,'Seasonal naive':f_snaive,'Seasonal naive x growth':f_snaive_g,
        'Damped-trend ETS':f_ets,'ARIMA(0,1,1)':f_arima011,'Log-trend + seasonal (shrunk)':f_trend_seas}
def smape(a,f): return np.mean(2*np.abs(a-f)/(np.abs(a)+np.abs(f)))*100
H=6; rows=[]; errs={}
for s in SERIES:
    y=w[s].values
    for m,fn in MODELS.items():
        for o in range(18,len(y)):          # origin: train on y[:o]; need >=18 so growth-adjusted snaive is defined
            hh=min(H,len(y)-o); f=fn(y[:o],hh); a=y[o:o+hh]
            for k in range(hh): rows.append((s,m,o,k+1,a[k],f[k]))
R=pd.DataFrame(rows,columns=['series','model','origin','h','actual','fc']); R['e']=R.actual-R.fc
R['ape']=np.abs(R.e)/R.actual*100; R['sape']=2*np.abs(R.e)/(R.actual+R.fc)*100
sc=R.groupby(['series','model']).agg(n=('e','size'),MAE=('e',lambda x:np.abs(x).mean()),RMSE=('e',lambda x:np.sqrt((x**2).mean())),MAPE=('ape','mean'),sMAPE=('sape','mean')).reset_index()
# MASE vs in-sample seasonal-naive scale
for s in SERIES:
    y=w[s].values; sc_=np.mean(np.abs(y[12:]-y[:-12])); sc.loc[sc.series==s,'MASE']=sc.loc[sc.series==s,'MAE']/sc_
sc=sc.round(3); sc.to_csv('data/clean/forecast_tournament.csv',index=False)
best=sc.loc[sc.groupby('series').sMAPE.idxmin()][['series','model','MAPE','sMAPE','RMSE','MASE']]; print(best.to_string())
print(sc.pivot(index='model',columns='series',values='sMAPE').round(2))
# ----- final forecasts, Mar-2026 .. Feb-2027, 80/95% intervals from rolling-origin errors of the selected model -----
horizon=12; out=[]
fut=pd.date_range('2026-03-01',periods=horizon,freq='MS')
for s in SERIES:
    mname=best.set_index('series').loc[s,'model']; fn=MODELS[mname]; y=w[s].values
    fc=fn(y,horizon)
    e=R[(R.series==s)&(R.model==mname)]; sig={k:np.sqrt((e[e.h==k].e**2).mean()) for k in range(1,H+1)}
    for k in range(1,horizon+1):
        sg=sig[k] if k<=H else sig[H]*np.sqrt(k/H)
        out.append((s,mname,fut[k-1],fc[k-1],fc[k-1]-1.2816*sg,fc[k-1]+1.2816*sg,fc[k-1]-1.96*sg,fc[k-1]+1.96*sg))
F=pd.DataFrame(out,columns=['series','model','date','fc','lo80','hi80','lo95','hi95']); F.round(1).to_csv('data/clean/forecast_12m.csv',index=False)
print(F[F.series.isin(['Diesel (AGO)','Total'])].round(1).to_string())
# annualised Mar26-Feb27
print(F.groupby('series')[['fc','lo80','hi80','lo95','hi95']].sum().round(0))
# fig
fig,axs=plt.subplots(2,2,figsize=(7.8,5.4)); 
for ax,s in zip(axs.ravel(),['Diesel (AGO)','Petrol (PMS)','LPG','Total']):
    f=F[F.series==s]; ax.plot(w.index,w[s],'o-',ms=3,c='#1f4e79'); ax.plot(f.date,f.fc,c='#c0392b'); 
    ax.fill_between(f.date,f.lo95,f.hi95,color='#c0392b',alpha=.12); ax.fill_between(f.date,f.lo80,f.hi80,color='#c0392b',alpha=.22)
    ax.set_title(f"{s}  [{f.model.iloc[0]}]",fontsize=8.5); ax.grid(alpha=.25); ax.tick_params(labelsize=7)
fig.autofmt_xdate(); fig.tight_layout(); fig.savefig('figures/f4_forecasts.png',dpi=200); plt.close()
R.round(3).to_csv('data/clean/forecast_rolling_errors.csv',index=False)
