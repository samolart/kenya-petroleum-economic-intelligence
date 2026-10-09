"""10 - Build Kenya_Petroleum_Economic_Model.xlsx with live formulas (change an assumption -> model updates)."""
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from common import *
wb=Workbook(); BLUE=Font(color='0000FF'); HB=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F4E79'); INP=PatternFill('solid',fgColor='FFF2CC'); BOLD=Font(bold=True)
def hdr(ws,row,vals,col=1):
    for i,v in enumerate(vals):
        c=ws.cell(row=row,column=col+i,value=v); c.font=HB; c.fill=HF; c.alignment=Alignment(horizontal='center',wrap_text=True)
def inp(c): c.font=BLUE; c.fill=INP
def widths(ws,ws_w):
    for i,w in enumerate(ws_w): ws.column_dimensions[L(i+1)].width=w
# ---------------- README ----------------
ws=wb.active; ws.title='README'; widths(ws,[110])
for i,t in enumerate(['Kenya Petroleum Economic Model (companion to the Market Outlook 2026-2035)','',
 'How it works: yellow cells with blue text are inputs (sheet Assumptions and the project inputs on Project_Economics). Everything else is a formula.',
 'Change the scenario selector (Assumptions!C3: 1 = Low-demand, 2 = Baseline, 3 = High-demand) and the Scenarios, Supply_Security, LPG_Storage and Dashboard sheets update.',
 'Sheets: Assumptions | Demand_Data | Prices | Scenarios | Supply_Security | LPG_Storage | Project_Economics | Sensitivity (static results from the Python pipeline) | Dashboard',
 'Data: LeadAfrik extract of KNBS Leading Economic Indicators, with the product columns RELABELLED after reconciliation to EPRA PDP 2024 and KNBS 2025 (see Data Quality Report). Jet fuel* and Fuel oil/other* identities are probable, not confirmed.',
 'Scenario growth rates: EPRA Petroleum Development Plan 2025-2029. Price shocks, 2030-35 fade, LPG/kerosene/jet elasticities and all South Lokichar costs and fiscal terms are the author\'s ASSUMPTIONS.',
 'South Lokichar: illustrative public-information model; NOT official or confidential project economics.',
 'Sensitivity sheet values are static outputs of the Python model (they include break-even solves that Excel cannot do without Goal Seek). The Project_Economics sheet reproduces the base case live.']):
    ws.cell(row=i+1,column=1,value=t).alignment=Alignment(wrap_text=True)
ws['A1'].font=Font(bold=True,size=14)
# ---------------- Demand_Data ----------------
W=load_cons(); wd=wb.create_sheet('Demand_Data'); hdr(wd,1,['Month','Year']+list(W.columns))
for i,(dt,r) in enumerate(W.iterrows()):
    wd.cell(row=i+2,column=1,value=dt.to_pydatetime()).number_format='mmm-yy'; wd.cell(row=i+2,column=2,value=dt.year)
    for j,v in enumerate(r.values): c=wd.cell(row=i+2,column=3+j,value=None if pd.isna(v) else float(v)); c.number_format='#,##0.0'
n=len(W)+1; widths(wd,[10,7]+[14]*9)
wd.cell(row=n+3,column=1,value='Annual totals (kt) - complete years only').font=BOLD
for k,y in enumerate((2024,2025)):
    wd.cell(row=n+4+k,column=1,value=y)
    for j in range(len(W.columns)): col=L(3+j); c=wd.cell(row=n+4+k,column=3+j,value=f'=SUMIFS({col}2:{col}{n},$B$2:$B${n},$A{n+4+k})'); c.number_format='#,##0.0'
wd.cell(row=n+6,column=1,value='Growth 2025/24').font=BOLD
for j in range(len(W.columns)): col=L(3+j); c=wd.cell(row=n+6,column=3+j,value=f'={col}{n+5}/{col}{n+4}-1'); c.number_format='0.0%'
wd.cell(row=n+7,column=1,value='Share 2025').font=BOLD
for j in range(len(W.columns)): col=L(3+j); c=wd.cell(row=n+7,column=3+j,value=f'={col}{n+5}/${L(3+len(W.columns)-1)}{n+5}'); c.number_format='0.0%'
wd.freeze_panes='C2'; ANN25=n+5   # row of 2025 totals
cols={p:L(3+i) for i,p in enumerate(W.columns)}
# ---------------- Prices ----------------
pr=load_prices(); wp=wb.create_sheet('Prices'); hdr(wp,1,['Month']+list(pr.columns)); widths(wp,[10]+[22]*5)
for i,(dt,r) in enumerate(pr.iterrows()):
    wp.cell(row=i+2,column=1,value=dt.to_pydatetime()).number_format='mmm-yy'
    for j,v in enumerate(r.values): wp.cell(row=i+2,column=2+j,value=float(v)).number_format='#,##0.00'
m=len(pr)+1; wp.cell(row=m+2,column=1,value='Change Jan-25 to Mar-26').font=BOLD
for j in range(len(pr.columns)): c=wp.cell(row=m+2,column=2+j,value=f'={L(2+j)}{m}/{L(2+j)}2-1'); c.number_format='0.0%'
wp.cell(row=m+3,column=1,value='CV').font=BOLD
for j in range(len(pr.columns)): c=wp.cell(row=m+3,column=2+j,value=f'=STDEV({L(2+j)}2:{L(2+j)}{m})/AVERAGE({L(2+j)}2:{L(2+j)}{m})'); c.number_format='0.0%'
wp.cell(row=m+5,column=1,value='Note: national averages to Mar-2026. 2026 Nairobi maxima after the Gulf-war shock are in the report (Diesel 242.92 in May-26; 217.86 in Sep-26).')
# ---------------- Assumptions ----------------
wa=wb.create_sheet('Assumptions',1); widths(wa,[44,14,14,14,14,50])
wa['A1']='ASSUMPTIONS (yellow = input)'; wa['A1'].font=Font(bold=True,size=13)
wa['A3']='Scenario selector (1=Low-demand, 2=Baseline, 3=High-demand)'; wa['B3']='Selected'; wa['C3']=2; inp(wa['C3'])
wa['D3']='=CHOOSE(C3,"Low-demand","Baseline","High-demand")'
prods=['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Kerosene (IK)']
hdr(wa,5,['Underlying growth 2025-29, % per year','','Low (pessimistic)','Baseline','High (optimistic)','Selected / source'])
G={'Diesel (AGO)':(2.74,3.52,4.28),'Petrol (PMS)':(2.97,3.35,4.08),'LPG':(6.34,7.26,8.82),'Jet fuel*':(1.70,1.87,2.17),'Kerosene (IK)':(-5.29,-4.57,-3.86)}
for i,p in enumerate(prods):
    r=6+i; wa.cell(row=r,column=1,value=p)
    for j,v in enumerate(G[p]): c=wa.cell(row=r,column=3+j,value=v); inp(c)
    wa.cell(row=r,column=6,value=f'=INDEX(C{r}:E{r},$C$3)').number_format='0.00'
wa['A11']='Source: EPRA Petroleum Development Plan 2025-2029 (Section 4).'
hdr(wa,12,['2026 average pump-price rise vs 2025, %','','Low-demand','Baseline','High-demand','Selected'])
SH={'Diesel (AGO)':(30,20,10),'Petrol (PMS)':(22,15,8),'LPG':(20,10,5),'Jet fuel*':(0,0,0),'Kerosene (IK)':(30,20,10)}
for i,p in enumerate(prods):
    r=13+i; wa.cell(row=r,column=1,value=p)
    for j,v in enumerate(SH[p]): c=wa.cell(row=r,column=3+j,value=v); inp(c)
    wa.cell(row=r,column=6,value=f'=INDEX(C{r}:E{r},$C$3)')
wa['A18']='Author assumptions informed by Mar-Sep 2026 EPRA reviews (Nairobi diesel +30.8%, petrol +20.1% Mar-cycle to Sep-cycle).'
hdr(wa,19,['Price elasticity of demand','','Short-run','Long-run','','Source'])
EL={'Diesel (AGO)':(-0.185,-0.570,'PDP-implied'),'Petrol (PMS)':(-0.096,-0.259,'PDP-implied'),'LPG':(-0.15,-0.30,'Assumption'),'Jet fuel*':(0,0,'Assumption'),'Kerosene (IK)':(-0.2,-0.5,'Assumption')}
for i,p in enumerate(prods):
    r=20+i; wa.cell(row=r,column=1,value=p)
    for j in range(2): c=wa.cell(row=r,column=3+j,value=EL[p][j]); inp(c)
    wa.cell(row=r,column=6,value=EL[p][2])
oth=[('2030-35 growth fade factor (x 2025-29 rate)',0.8,'Assumption'),('Exchange rate, KSh per USD',129.2,'Assumption (flat)'),('Fuel oil growth to 2027, % per year',4.68,'EPRA PDP'),('Fuel oil growth after 2027, % per year',-3.19,'EPRA PDP'),
     ('Stock-cover standard, days',30,'EPRA PDP (15 operational + 15 strategic)'),('Installed LPG storage, kt (Mar-2025)',44.43,'EPRA PDP'),('Additional LPG storage commissioned, kt (e.g. Lake Gas 10)',0,'Input; status unverified'),
     ('ML per kt: diesel',2608.2/2193.6,'PDP-implied'),('ML per kt: petrol',2044.11/1472.7,'PDP-implied'),('ML per kt: jet',972.49/765.1,'PDP-implied'),('ML per kt: kerosene',47.17/37.1,'PDP-implied')]
for i,(a,b,s) in enumerate(oth):
    r=26+i; wa.cell(row=r,column=1,value=a); c=wa.cell(row=r,column=3,value=b); inp(c); wa.cell(row=r,column=6,value=s)
FADE,FX,FO1,FO2,COVER,LPGCAP,LPGADD,MLD,MLP,MLJ,MLK=[f'Assumptions!$C${26+i}' for i in range(11)]
# ---------------- Scenarios ----------------
sc=wb.create_sheet('Scenarios'); widths(sc,[8]+[13]*9)
sc['A1']='Demand projection 2025-2035 (kt) - driven by the scenario selector'; sc['A1'].font=Font(bold=True,size=13); sc['A2']='=Assumptions!D3'
hdr(sc,4,['Year']+prods+['Fuel oil/other*','Avgas','Total','YoY total'])
pcol={'Diesel (AGO)':2,'Petrol (PMS)':3,'LPG':4,'Jet fuel*':5,'Kerosene (IK)':6}
for k,y in enumerate(range(2025,2036)):
    r=5+k; sc.cell(row=r,column=1,value=y)
    for i,p in enumerate(prods):
        col=pcol[p]; cl=L(col)
        if y==2025: f=f"=Demand_Data!{cols[p]}{ANN25}"
        else:
            g=f'Assumptions!$F${6+i}'; sh=f'Assumptions!$F${13+i}'; sr=f'Assumptions!$C${20+i}'; lr=f'Assumptions!$D${20+i}'
            f=f"={cl}{r-1}*EXP(LN(1+{g}*IF($A{r}<=2029,1,{FADE})/100)+IF($A{r}=2026,{sr}*LN(1+{sh}/100),IF(OR($A{r}=2027,$A{r}=2028),({lr}-{sr})*LN(1+{sh}/100)/2,0)))"
        sc.cell(row=r,column=col,value=f).number_format='#,##0'
    sc.cell(row=r,column=7,value=(f"=Demand_Data!{cols['Fuel oil/other*']}{ANN25}" if y==2025 else f"=G{r-1}*(1+IF($A{r}<=2027,{FO1},{FO2})/100)")).number_format='#,##0'
    sc.cell(row=r,column=8,value=(f"=Demand_Data!{cols['Avgas']}{ANN25}" if y==2025 else f"=H{r-1}")).number_format='#,##0.0'
    sc.cell(row=r,column=9,value=f'=SUM(B{r}:H{r})').number_format='#,##0'
    if y>2025: sc.cell(row=r,column=10,value=f'=I{r}/I{r-1}-1').number_format='0.0%'
sc['A17']='CAGR 2025-35'; sc['I17']='=(I15/I5)^(1/10)-1'; sc['I17'].number_format='0.00%'
sc['A19']='Check: 2025 total should equal KNBS 5.7 Mt:'; sc['I19']='=I5'; sc['I19'].number_format='#,##0'
# ---------------- Supply_Security ----------------
ss=wb.create_sheet('Supply_Security'); widths(ss,[34,16,16,16,16,16,16])
ss['A1']='Supply security: days of cover and storage'; ss['A1'].font=Font(bold=True,size=13)
hdr(ss,3,['Product','2025 demand (kt)','Daily demand (ML)','Gross licensed capacity (ML)','Days of demand if tanks full','Stock for standard cover (ML)','Reported cover (days) - input'])
sp=[('Diesel (AGO)','B',MLD,755.04,19),('Petrol (PMS)','C',MLP,462.60,16),('Jet fuel*','E',MLJ,231.84,49)]
for i,(p,col,ml,cap,rep) in enumerate(sp):
    r=4+i; ss.cell(row=r,column=1,value=p); ss.cell(row=r,column=2,value=f'=Scenarios!{col}5').number_format='#,##0'
    ss.cell(row=r,column=3,value=f'=B{r}*{ml}/365').number_format='0.00'; c=ss.cell(row=r,column=4,value=cap); inp(c)
    ss.cell(row=r,column=5,value=f'=D{r}/C{r}').number_format='0'; ss.cell(row=r,column=6,value=f'=C{r}*{COVER}').number_format='0'; c=ss.cell(row=r,column=7,value=rep); inp(c)
hdr(ss,9,['Product','Reported cover (days)','Shortfall vs standard (days)','Shortfall (ML)','Status (author thresholds)'])
for i,(p,_,_,_,_) in enumerate(sp):
    r=10+i; ss.cell(row=r,column=1,value=p); ss.cell(row=r,column=2,value=f'=G{4+i}')
    ss.cell(row=r,column=3,value=f'=MAX({COVER}-B{r},0)'); ss.cell(row=r,column=4,value=f'=C{r}*C{4+i}').number_format='0.0'
    ss.cell(row=r,column=5,value=f'=IF(B{r}>={COVER},"GREEN",IF(B{r}>=15,"AMBER","RED"))')
ss['A14']='Thresholds: GREEN >= standard (30 d); AMBER 15-29; RED < 15. Author framework, not official. Reported cover inputs are from press reports of Ministry/Treasury statements (Apr-2026): petrol 16, diesel 19, jet 49.'
ss['A16']='Inventory value of cover (USD m) at Aug-2026 landed cost'; ss['A16'].font=BOLD
ss['A17']='Landed cost petrol (USD/m3)'; ss['B17']=874.26; inp(ss['B17']); ss['A18']='Landed cost diesel (USD/m3)'; ss['B18']=957.05; inp(ss['B18'])
ss['A19']='Days of cover to value'; ss['B19']=90; inp(ss['B19'])
ss['A20']='Inventory value (USD m)'; ss['B20']='=B19*(C5*B17+C4*B18)/1000'; ss['B20'].number_format='#,##0'
ss['A21']='Inventory value (KSh bn)'; ss['B21']=f'=B20*{FX}/1000'; ss['B21'].number_format='#,##0.0'
ss['A22']='Annual carrying cost at financing rate (USD m)'; ss['B22']='=B20*C22'; ss['C22']=0.10; inp(ss['C22']); ss['B22'].number_format='#,##0.0'
# ---------------- LPG_Storage ----------------
ls=wb.create_sheet('LPG_Storage'); widths(ls,[10,18,22,18,16])
ls['A1']='LPG storage requirement (PDP method: planned supply = demand x (1+cover/365); storage = supply / 12)'; ls['A1'].font=BOLD
hdr(ls,3,['Year','LPG demand (kt)','Required storage (kt)','Installed + new (kt)','Headroom (kt)'])
for k,y in enumerate(range(2025,2036)):
    r=4+k; ls.cell(row=r,column=1,value=y); ls.cell(row=r,column=2,value=f'=Scenarios!D{5+k}').number_format='#,##0'
    ls.cell(row=r,column=3,value=f'=B{r}*(1+{COVER}/365)/12').number_format='0.0'; ls.cell(row=r,column=4,value=f'={LPGCAP}+{LPGADD}').number_format='0.0'
    ls.cell(row=r,column=5,value=f'=D{r}-C{r}').number_format='+0.0;-0.0'
# ---------------- Project_Economics ----------------
pe=wb.create_sheet('Project_Economics'); widths(pe,[44,14]+[12]*17)
pe['A1']='South Lokichar - ILLUSTRATIVE scenario model (assumptions are the author\'s; not official project economics)'; pe['A1'].font=Font(bold=True,size=12)
IN=[('Brent, US$/bbl (real, flat)',70),('Differential to Brent, US$/bbl',6),('Plateau production, kbpd',60),('Capex, US$ m',6000),('Opex, US$/bbl',12),('Transport tariff, US$/bbl',9),('Discount rate',0.10),('Royalty, % of revenue',0.10),('Cost-recovery cap, % of net revenue',0.60),('Government share of profit oil',0.50),('Annual decline after plateau',0.10),('Recoverable reserves, mmbbl',560),('Abandonment, % of capex',0.03)]
names=['brent','diff','plat','capex','opex','tariff','disc','roy','cap','gpp','decl','res','abex']
REF={}
for i,((a,b),nm) in enumerate(zip(IN,names)):
    r=3+i; pe.cell(row=r,column=1,value=a); c=pe.cell(row=r,column=2,value=b); inp(c); REF[nm]=f'$B${r}'
pe['A17']='Ramp (share of plateau): 2026 0% / 2027 33% / 2028 66%; plateau to 2037; capex phasing 15/35/30/20% in 2026-29'
hdr(pe,19,['Year','Ramp / phase','kbpd (raw)','kbpd (eff.)','mmbbl','Cum. mmbbl','Revenue','Royalty','Opex+tariff','Capex','Pre-fiscal CF','Cost pool','Cost recovered','Profit oil','Govt take','Contractor CF','Disc. factor'])
phase={2026:.15,2027:.35,2028:.30,2029:.20}; ramp={2026:0.0,2027:0.33,2028:0.66}
first=20
for k,y in enumerate(range(2026,2061)):
    r=first+k; pe.cell(row=r,column=1,value=y)
    pe.cell(row=r,column=2,value=ramp.get(y,1.0 if y<=2037 else None))
    pe.cell(row=r,column=3,value=(f"={REF['plat']}*B{r}" if y<=2037 else f"=D{r-1}*(1-{REF['decl']})")).number_format='0.0'
    pe.cell(row=r,column=4,value=f"=IF(E{r}>0,C{r},0)").number_format='0.0'
    prevcum='0' if k==0 else f'F{r-1}'
    pe.cell(row=r,column=5,value=f"=IF(AND(A{r}>2037,C{r}*365/1000*({REF['brent']}-{REF['diff']})<C{r}*365/1000*({REF['opex']}+{REF['tariff']})),0,MIN(C{r}*365/1000,MAX({REF['res']}-{prevcum},0)))").number_format='0.0'
    pe.cell(row=r,column=6,value=f"={prevcum}+E{r}").number_format='0.0'
    pe.cell(row=r,column=7,value=f"=E{r}*({REF['brent']}-{REF['diff']})").number_format='#,##0'
    pe.cell(row=r,column=8,value=f"=G{r}*{REF['roy']}").number_format='#,##0'
    pe.cell(row=r,column=9,value=f"=E{r}*({REF['opex']}+{REF['tariff']})").number_format='#,##0'
    prevvol='0' if k==0 else f'E{r-1}'
    pe.cell(row=r,column=10,value=f"={REF['capex']}*{phase.get(y,0)}+IF(AND({prevvol}>0,E{r}=0),{REF['abex']}*{REF['capex']},0)").number_format='#,##0'
    pe.cell(row=r,column=11,value=f'=G{r}-I{r}-J{r}').number_format='#,##0'
    prevpool='0' if k==0 else f'L{r-1}'
    pe.cell(row=r,column=13,value=f"=MIN({prevpool}+I{r}+J{r},{REF['cap']}*(G{r}-H{r}))").number_format='#,##0'
    pe.cell(row=r,column=12,value=f"={prevpool}+I{r}+J{r}-M{r}").number_format='#,##0'
    pe.cell(row=r,column=14,value=f"=MAX(G{r}-H{r}-M{r},0)").number_format='#,##0'
    pe.cell(row=r,column=15,value=f"=H{r}+N{r}*{REF['gpp']}").number_format='#,##0'
    pe.cell(row=r,column=16,value=f"=G{r}-H{r}-N{r}*{REF['gpp']}-I{r}-J{r}").number_format='#,##0'
    pe.cell(row=r,column=17,value=f"=(1+{REF['disc']})^-(A{r}-2026)").number_format='0.000'
last=first+34
pe['A57']='RESULTS'; pe['A57'].font=BOLD
res=[('Project NPV (pre-fiscal), US$ m',f'=SUMPRODUCT(K{first}:K{last},Q{first}:Q{last})','#,##0'),('Project IRR',f'=IRR(K{first}:K{last},0.1)','0.0%'),('Government NPV, US$ m',f'=SUMPRODUCT(O{first}:O{last},Q{first}:Q{last})','#,##0'),('Government take, undiscounted, US$ m',f'=SUM(O{first}:O{last})','#,##0'),('Contractor NPV, US$ m',f'=SUMPRODUCT(P{first}:P{last},Q{first}:Q{last})','#,##0'),('Contractor IRR',f'=IRR(P{first}:P{last},0.05)','0.0%'),('Cumulative production, mmbbl',f'=SUM(E{first}:E{last})','#,##0'),('Check: python base-case project NPV = 1,551; contractor = -1,260',None,None)]
for i,(a,f,nf) in enumerate(res):
    pe.cell(row=58+i,column=1,value=a)
    if f: c=pe.cell(row=58+i,column=2,value=f); c.number_format=nf
# ---------------- Sensitivity (static from python) ----------------
se=wb.create_sheet('Sensitivity'); widths(se,[30,14,14,14,14,14,14])
se['A1']='Static outputs from the Python pipeline (data/clean/*.csv)'; se['A1'].font=BOLD
g=pd.read_csv('data/clean/lokichar_grid_npv_project.csv',index_col=0); hdr(se,3,['Project NPV10, US$ m: Brent \\ plateau']+[f'{c} of 60 kbpd' for c in g.columns])
for i,idx in enumerate(g.index):
    se.cell(row=4+i,column=1,value=f'US${idx}')
    for j,v in enumerate(g.loc[idx]): se.cell(row=4+i,column=2+j,value=float(v)).number_format='#,##0'
t=pd.read_csv('data/clean/lokichar_tornado.csv'); hdr(se,12,['Tornado driver','Downside (US$ m)','Upside (US$ m)'])
for i,r in enumerate(t.itertuples()): se.cell(row=13+i,column=1,value=r.driver); se.cell(row=13+i,column=2,value=float(r.downside)).number_format='#,##0'; se.cell(row=13+i,column=3,value=float(r.upside)).number_format='#,##0'
f=pd.read_csv('data/clean/lokichar_fiscal_cases.csv'); hdr(se,21,list(f.columns))
for i,r in enumerate(f.itertuples(index=False)):
    for j,v in enumerate(r): se.cell(row=22+i,column=1+j,value=(float(v) if not isinstance(v,str) else v))
ss_=pd.read_csv('data/clean/scenario_sensitivity.csv'); hdr(se,30,list(ss_.columns))
for i,r in enumerate(ss_.itertuples(index=False)):
    for j,v in enumerate(r): se.cell(row=31+i,column=1+j,value=(float(v) if not isinstance(v,str) else v))
# ---------------- Dashboard ----------------
db=wb.create_sheet('Dashboard',1); widths(db,[46,18,18,18])
db['A1']='KENYA PETROLEUM - DASHBOARD'; db['A1'].font=Font(bold=True,size=14); db['A2']='=Assumptions!D3'
rows=[('Total demand 2025 (kt)','=Scenarios!I5','#,##0'),('Total demand 2026 (kt)','=Scenarios!I6','#,##0'),('Total demand 2030 (kt)','=Scenarios!I10','#,##0'),('Total demand 2035 (kt)','=Scenarios!I15','#,##0'),('CAGR 2025-35','=Scenarios!I17','0.00%'),
 ('Diesel 2030 (kt)','=Scenarios!B10','#,##0'),('Petrol 2030 (kt)','=Scenarios!C10','#,##0'),('LPG 2030 (kt)','=Scenarios!D10','#,##0'),('LPG storage headroom 2030 (kt)','=LPG_Storage!E9','+0.0;-0.0'),('LPG storage headroom 2026 (kt)','=LPG_Storage!E5','+0.0;-0.0'),
 ('Diesel shortfall vs standard (ML)','=Supply_Security!D10','#,##0'),('Petrol shortfall vs standard (ML)','=Supply_Security!D11','#,##0'),('Project NPV10, US$ m','=Project_Economics!B58','#,##0'),('Project IRR','=Project_Economics!B59','0.0%'),('Government NPV10, US$ m','=Project_Economics!B60','#,##0'),('Contractor NPV10, US$ m','=Project_Economics!B62','#,##0')]
for i,(a,f_,nf) in enumerate(rows): db.cell(row=4+i,column=1,value=a); c=db.cell(row=4+i,column=2,value=f_); c.number_format=nf
wb.save('out/Kenya_Petroleum_Economic_Model.xlsx'); print('saved')
