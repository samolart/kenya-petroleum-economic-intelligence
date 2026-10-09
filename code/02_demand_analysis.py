import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from common import *
w=load_cons(); P=PRODUCTS[:6]; W=w.dropna()  # drop Mar-2026 (blank)
out={}
# annual, shares, growth
ann=w.loc['2024':'2025'].groupby(lambda d:d.year).sum()
ann.loc['growth%']=(ann.loc[2025]/ann.loc[2024]-1)*100
share=(ann.loc[[2024,2025]].div(ann.loc[[2024,2025],'Total'],axis=0)*100)
print(ann.round(1).T); print(share.round(1).T)
# Jan-Feb YTD growth 2026 vs 2025
ytd=(W.loc['2026-01':'2026-02'].sum().values/W.loc['2025-01':'2025-02'].sum().values-1)*100
ytd=pd.Series(ytd,index=W.columns); print('YTD26 growth',ytd.round(1).to_dict())
# YoY monthly, MoM, rolling, CV, seasonality
yoy=W.pct_change(12)*100; mom=W.pct_change()*100
r3=W.rolling(3).mean(); r12=W.rolling(12).mean()
cv=(W.loc['2024':'2025'].std()/W.loc['2024':'2025'].mean()*100)
# detrended seasonal index: ratio to centred 12-month mean not feasible (n=26) -> use ratio to calendar-year mean, avg over 2024,2025
si=pd.concat([W.loc[str(y)].div(W.loc[str(y)].mean()) for y in (2024,2025)]); si=si.groupby(si.index.month).mean()
print('CV%',cv.round(1).to_dict()); print(si[['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Total']].round(3))
# trend growth: log-linear trend per product (annualised)
t=np.arange(len(W)); tr={}
for p in W.columns:
    b=np.polyfit(t,np.log(W[p].values),1)[0]; tr[p]=(np.exp(12*b)-1)*100
print('trend ann%',{k:round(v,1) for k,v in tr.items()})
pd.DataFrame({'ann2024':ann.loc[2024],'ann2025':ann.loc[2025],'growth%':ann.loc['growth%'],'share24':share.loc[2024],'share25':share.loc[2025],'ytd26%':ytd,'CV%':cv,'trend%':pd.Series(tr)}).round(2).to_csv('data/clean/demand_summary.csv')
yoy.round(2).to_csv('data/clean/yoy.csv'); si.round(4).to_csv('data/clean/seasonal_index.csv')
# correlation LPG vs kerosene, petrol vs diesel (levels and yoy)
print('corr LPG-IK levels',W['LPG'].corr(W['Kerosene (IK)']).round(2),'yoy',yoy['LPG'].corr(yoy['Kerosene (IK)']).round(2))
# figures
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.5,3.6))
for p in ['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*']: ax.plot(W.index,W[p],marker='o',ms=3,label=p)
ax.set_ylabel('Thousand tonnes / month'); ax.legend(ncol=4,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.15)); ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig('figures/f1_monthly_demand.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(len(P)); 
ax.bar(x-.2,ann.loc[2024,P],.4,label='2024'); ax.bar(x+.2,ann.loc[2025,P],.4,label='2025')
for i,p in enumerate(P): ax.text(i+.2,ann.loc[2025,p]+30,f"{ann.loc['growth%',p]:+.0f}%",ha='center',fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(P,rotation=15); ax.set_ylabel('kt / year'); ax.legend(frameon=False); fig.tight_layout(); fig.savefig('figures/f2_annual.png',dpi=200); plt.close()
fig,ax=plt.subplots(figsize=(7.5,3.2)); 
for p in ['Diesel (AGO)','Petrol (PMS)','LPG','Total']: ax.plot(yoy.index,yoy[p],label=p)
ax.axhline(0,c='k',lw=.6); ax.set_ylabel('YoY growth, %'); ax.legend(ncol=4,frameon=False); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig('figures/f3_yoy.png',dpi=200); plt.close()
