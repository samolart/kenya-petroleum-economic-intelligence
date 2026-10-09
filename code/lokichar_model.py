"""06 - South Lokichar illustrative economic model. ALL FISCAL AND COST INPUTS ARE ASSUMPTIONS (public headline facts: ~US$6bn capex commitment, 60-100 kbpd early production, ~560 mmbbl recoverable, first-oil target Dec 2026)."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import brentq
BASE=dict(brent=70.0,diff=6.0,plateau=60.0,capex=6000.0,opex=12.0,tariff=9.0,disc=0.10,royalty=0.10,cr_cap=0.60,gov_pp=0.50,decl=0.10,reserves=560.0,abex=0.03)
YEARS=np.arange(2026,2061)
RAMP={2026:0.0,2027:0.33,2028:0.66}      # share of plateau (first oil Dec-2026 -> no 2026 volume)
CAPEX_PHASE={2026:.15,2027:.35,2028:.30,2029:.20}
def run(**kw):
    a=dict(BASE); a.update(kw); cum=0; rows=[]; plateau_end=2029+8   # plateau 2029-2037 (9 yrs)
    for y in YEARS:
        if y in RAMP: q=a['plateau']*RAMP[y]
        elif y<=plateau_end: q=a['plateau']
        else: q=rows[-1][1]*(1-a['decl'])
        vol=q*365/1000   # mmbbl
        if cum+vol>a['reserves']: vol=max(a['reserves']-cum,0)
        price=a['brent']-a['diff']; rev=vol*price; opx=vol*(a['opex']+a['tariff'])
        if vol>0 and rev<opx and y>plateau_end: vol=0; rev=opx=0     # economic limit
        cum+=vol; cap=a['capex']*CAPEX_PHASE.get(y,0)
        rows.append((y,q if vol>0 else 0,vol,rev,opx,cap)); 
    D=pd.DataFrame(rows,columns=['year','kbpd','mmbbl','revenue','opex','capex'])
    last=D[D.mmbbl>0].year.max(); D.loc[D.year==last+1,'capex']+=a['abex']*a['capex']; D=D[D.year<=last+1].copy()
    D['roy']=D.revenue*a['royalty']; D['pre_fiscal_cf']=D.revenue-D.opex-D.capex
    # PSC-style: cost recovery (opex+capex carried forward) capped at cr_cap of (revenue-royalty)
    pool=0; cr=[]; pp=[]; 
    for _,r in D.iterrows():
        pool+=r.opex+r.capex; avail=r.revenue-r.roy; rec=min(pool,a['cr_cap']*avail); pool-=rec; cr.append(rec); pp.append(max(avail-rec,0))
    D['cost_rec']=cr; D['profit_oil']=pp; D['gov_take']=D.roy+D.profit_oil*a['gov_pp']
    D['contractor_cf']=D.revenue-D.roy-D.profit_oil*a['gov_pp']-D.opex-D.capex
    t=D.year-2026; df=(1+a['disc'])**-t
    out=dict(npv_project=(D.pre_fiscal_cf*df).sum(),npv_contractor=(D.contractor_cf*df).sum(),npv_gov=(D.gov_take*df).sum(),gov_undisc=D.gov_take.sum(),
             cum_mmbbl=D.mmbbl.sum(),life_end=int(last),payback=None)
    def irr(cf):
        f=lambda r:(cf/(1+r)**t.values).sum()
        try: return brentq(f,-0.5,1.0)
        except: return np.nan
    out['irr_project']=irr(D.pre_fiscal_cf); out['irr_contractor']=irr(D.contractor_cf)
    c=D.pre_fiscal_cf.cumsum(); out['payback']=int(D.year[c>0].min()) if (c>0).any() else None
    tot=D.revenue.sum()-D.opex.sum()-D.capex.sum(); out['gov_share_pct']=D.gov_take.sum()/tot*100 if tot>0 else np.nan
    return D,out
