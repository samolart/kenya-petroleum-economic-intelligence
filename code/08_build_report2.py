import pandas as pd, glob
from docx_helpers import *
d=new_doc()
for _ in range(5): d.add_paragraph()
P(d,'KENYA PETROLEUM MARKET OUTLOOK',bold=True,size=26,align='c').runs[0].font.color.rgb=NAVY
P(d,'Methods and Code Report',bold=True,size=20,align='c')
P(d,'Every step taken, every tool used, every assumption, and the complete code',size=13,align='c',italic=True)
for _ in range(3): d.add_paragraph()
P(d,'Companion to the Kenya Petroleum Market Outlook 2026–2035  |  October 2026',size=11,align='c')
d.add_page_break()
H(d,'1. Purpose and how to use this report')
P(d,'This report documents how the Market Outlook was produced so that every number can be traced and re-run. It covers the environment, a chronological log of what was done (including what failed), the data and its quality audit, the exact method of each analysis, an assumptions register, deviations from the original project brief, and a full code appendix. The repository (data/raw, data/clean, code, figures) reproduces everything with one command: ./run_all.sh.')
H(d,'2. Tools and environment')
T(d,['Tool','Used for'],[
 ['Python 3.12, pandas, numpy','Data loading, cleaning, reshaping, all calculations'],
 ['scipy (optimize, brentq)','Fitting ETS and ARIMA by numerical optimisation; root finding for break-even oil prices'],
 ['matplotlib','All nine figures'],
 ['python-docx','Building both Word reports from the same numbers'],
 ['LibreOffice, pdftoppm','Rendering the reports to check layout'],
 ['Web search and page fetch','Retrieving the EPRA Petroleum Development Plan (PDF), 2026 price reviews, stock-cover statements, oil-market news, South Lokichar facts'],
 ['Not available','statsmodels (not installable; no network in the code sandbox). ETS, ARIMA(0,1,1) and Newey-West OLS were therefore written directly with numpy/scipy. Excel and a self-contained HTML dashboard were built instead; SQL and Streamlit were not used.']],widths=[5,11.5])
H(d,'3. Chronological log of work')
steps=[
 ('Step 1 – Inventory of inputs','Three CSVs were uploaded: monthly consumption (191 lines), national average retail prices (77 lines), town-level pump prices (4 lines: three comment lines plus a header, **no data rows**). The pump-price file was recorded as empty and excluded.'),
 ('Step 2 – Earlier access attempts (before the files arrived)','The LeadAfrik API was blocked to automated access (robots rule) and the web page exposed only 48 of 189 rows; the code sandbox had no internet. No numbers were estimated from partial data. The user supplied the three CSVs instead.'),
 ('Step 3 – Structural validation','Footer attribution lines removed; 189 rows = 7 products × 27 months confirmed; no duplicate (month, product); only March 2026 blank (7 values); 21 rows flagged provisional (Jan–Mar 2026). Prices: 75 rows = 5 series × 15 months, complete.'),
 ('Step 4 – Reasonableness check that exposed the label error','Annual sums per column were compared with EPRA PDP 2024 actuals (diesel 2,193.6 kt; petrol 1,472.7; LPG 414.9; kerosene 37.1; jet 765.1; fuel oil 301.9). The column labelled “LPG” summed to 1,472.7 kt, equal to PDP petrol; “Other” summed to 414.9, equal to PDP LPG. A full 7×6 matrix of column-versus-product errors was computed (code 01); exact matches (0.0%) were unique per product. The relabelling was then confirmed against 2025 KNBS facts: diesel 2,419.1 kt; LPG 475.9 kt (+14.7%); diesel+petrol 71.4% of demand; total 5.7 Mt. All four independent checks held.'),
 ('Step 5 – External context gathering','EPRA PDP 2025–2029 read in full (demand equations, scenario growth rates, base-year data, storage capacity, LPG balance). Economic Survey 2026 figures located in press coverage. The discovery that a Gulf war began on 28 Feb 2026, with fuel shortages and a price spike, changed the framing of the whole report: the dataset ends one month into the shock. Pump-price reviews (March–September 2026), EPRA landed-cost statements, stock-cover statements and South Lokichar status were searched individually.'),
 ('Step 6 – Demand analytics (code 02)','Annual totals, shares, growth, month-on-month and year-on-year changes, rolling means, coefficient of variation, calendar-month seasonal indices, log-linear trends, LPG–kerosene correlations; figures 1–3.'),
 ('Step 7 – Forecast tournament (code 03)','Eight models, rolling-origin evaluation, selection by sMAPE, 12-month forecasts with 80/95% intervals; figure 4.'),
 ('Step 8 – Prices, elasticity and pass-through (code 04)','Price statistics; own log-log regression with Newey-West errors (result: wrong sign, rejected); elasticities derived from the PDP equations; petrol pass-through from EPRA landed costs; figure 5.'),
 ('Step 9 – Scenarios, supply security and risk (code 05)','Three scenarios to 2035; PDP back-test; stock-cover gaps; capacity versus requirement; LPG storage by the PDP’s own method; risk scores with weight sensitivity; figures 6–7.'),
 ('Step 10 – Project economics (code 06)','Discounted cash-flow model for South Lokichar with two fiscal cases, break-evens, price×output grid and tornado; figures 8–9.'),
 ('Step 11 – Extended analysis (code 09)','Product profiles; regional price spreads from press-reported EPRA maxima; price indices; cooking-fuel cost per useful MJ (illustrative efficiencies); landed-cost import-bill arithmetic; inventory value and carrying cost of 15/30/60/90 days of cover; petrol-displacement arithmetic; one-at-a-time scenario sensitivities; 2,000-draw Monte Carlo on South Lokichar; additional figures 10–13.'),
 ('Step 12 – Excel model (code 10)','Workbook with live formulas (scenarios, supply security, LPG storage, project cash flow with cost-recovery pool, IRR/NPV) and static sensitivity tables. Recalculated in LibreOffice and compared with Python: scenario totals identical (6,305.7 kt in 2030; 7,157.3 kt in 2035); project NPV10 1,550.5 vs 1,551; government NPV 2,812.5 vs 2,813; contractor NPV −1,262 vs −1,260. A first version differed (1,370) because the Excel plateau ended in 2036 while the Python model runs to 2037; the Excel model was corrected and re-verified.'),
 ('Step 13 – Report assembly and verification (codes 07, 08, 11)','Reports generated from the CSV outputs; numbers in text cross-checked against the CSVs; full clean re-run of the pipeline (exit status 0) to confirm reproducibility; layout checked by rendering to PDF.')]
for t,x in steps: P(d,'**'+t+'.** '+x)
H(d,'4. Data audit and reconciliation')
rec=pd.read_csv('data/clean/reconciliation.csv')
T(d,['Product (corrected)','2024 sum (kt)','2025 sum (kt)','Reference 2024 (PDP)','Reference 2025 (KNBS)','Error 2024'],[[r['product'],f"{r['2024_kt']:,.1f}",f"{r['2025_kt']:,.1f}",'' if pd.isna(r.reference_2024) else f"{r.reference_2024:,.1f}",'' if pd.isna(r.reference_2025_KNBS) else f"{r.reference_2025_KNBS:,.1f}",'' if pd.isna(r['err_2024_%']) else f"{r['err_2024_%']:+.1f}%"] for _,r in rec.iterrows()],widths=[3.6,2.4,2.4,3.0,3.2,2.0])
P(d,'**Relabelling map applied (code/common.py):** “LPG” → Petrol (PMS); “Other” → LPG; “Motor Spirit” → Jet fuel* (probable); “Jet Oil” → Fuel oil/other* (probable); AGO, kerosene and avgas unchanged. Evidence strength: four exact matches; the jet and fuel-oil assignments rest on magnitude (−4.3% and −17.2% from the PDP annual figures). These differences are consistent with LEI versus annual-survey definitions, but this has not been confirmed.')
H(d,'5. Methods in detail')
H(d,'5.1 Demand analytics',2)
B(d,['Growth: YoY = x_t / x_{t−12} − 1; MoM = x_t / x_{t−1} − 1. Rolling means over 3 and 12 months (12-month undefined before month 12).','Volatility: coefficient of variation of monthly volumes over 2024–25 (std / mean).','Seasonality: ratio of each month to its calendar-year mean, averaged over 2024 and 2025 (two observations per month).','Trend: slope of ln(volume) on time; annualised as exp(12 × slope) − 1.','Unit conversion: million litres per kt from the PDP base year (diesel 1.189, petrol 1.388, jet 1.271).'])
H(d,'5.2 Forecast tournament',2)
T(d,['Model','Definition'],[
 ['Naive','Last observation carried forward'],['Mean (last 6m)','Mean of the latest six months'],['Drift','Last value + average historical change'],['Seasonal naive','Value 12 months earlier'],
 ['Seasonal naive × growth','Seasonal naive scaled by (sum of latest 6 months / sum of the same 6 months a year earlier)'],
 ['Damped-trend ETS','Additive level + damped trend, smoothing parameters and damping fitted by minimising squared one-step errors (L-BFGS-B)'],
 ['ARIMA(0,1,1)','MA parameter fitted by conditional sum of squares; forecast flat from the one-step forecast'],
 ['Log-trend + seasonal (shrunk)','Log-linear trend plus month-of-year residual means, shrunk 50%']],widths=[4.5,12])
P(d,'**Evaluation.** Rolling-origin: for each origin o from 18 to 25 (training on the first o months), forecast up to 6 months ahead (fewer near the end of the sample). This produces 33 forecast errors per series and model. Metrics: MAE, RMSE, MAPE, sMAPE = mean(2|e| / (|a| + |f|)), MASE (MAE scaled by the in-sample seasonal-naive MAE). Selection criterion: lowest sMAPE per series. **Intervals:** forecast ± z × RMSE of the selected model’s errors at that horizon (z = 1.2816 for 80%, 1.96 for 95%); for horizons beyond 6, RMSE at horizon 6 × √(h/6). **Why not SARIMA/ARIMAX/Holt-Winters:** two seasonal cycles are too few to estimate seasonal states reliably and no long monthly exogenous series (GDP, FX, Brent) was available.')
H(d,'5.3 Elasticities and pass-through',2)
P(d,'Own estimate: ln Q_t = β0 + β1 ln P_t + β2 t + ε_t, 14 monthly observations (Jan 2025–Feb 2026), Newey-West (lag 2) standard errors. Result: β1 = +1.65 (diesel) and +0.69 (petrol), wrong sign, so it was rejected. PDP-implied elasticities: short-run ε = coefficient × P / Q at base-year values; long-run ε = ε_SR / (1 − φ), where φ is the lagged-dependent-variable coefficient (0.6754 diesel; 0.6284 petrol). Pass-through: Δ(pump price) / Δ(landed cost), landed cost converted at an assumed exchange rate, with and without 16% VAT.')
H(d,'5.4 Scenarios',2)
P(d,'For product p, scenario s and year t: Q_t = Q_{t−1} × exp[ln(1 + g_{p,s,t}) + adj_t], where g is the PDP growth rate for 2025–29 and 0.8 × that rate for 2030–35, and adj is the price-shock term: in 2026, ε_SR × ln(1 + ΔP); in 2027 and 2028, (ε_LR − ε_SR) × ln(1 + ΔP) / 2 each. Assumed price shocks and elasticities are listed in the register below.')
H(d,'5.5 Supply security',2)
P(d,'Days of cover = stock / average daily demand, with daily demand = 2025 annual demand (kt) × litres per kt / 365. Stock required for 30 days = 30 × daily demand. LPG storage: required = demand × (1 + 30/365) / 12, which reproduces the PDP’s 2025 figures (482.86 kt planned supply; spare ullage about 4 kt).')
H(d,'5.6 Project economics',2)
P(d,'Annual model, 2026–2060 (stops when production ends). Revenue = barrels × (Brent − differential). Royalty on gross revenue. Cost recovery: opex and capex accumulate in a pool recovered each year up to a cap share of revenue net of royalty. Profit oil = net revenue − cost recovery, split with the government. Government take = royalty + government profit oil share. Contractor cash flow = revenue − royalty − government profit oil − opex − capex. Project (pre-fiscal) cash flow = revenue − opex − capex. NPV discounted at 10% to 2026; IRR by root finding; break-even Brent by root finding of NPV = 0. Tornado: each driver moved one at a time.')
H(d,'5.7 Extended analysis',2)
B(d,['Import-bill arithmetic: volume (ML) = 2026 baseline kt × ML per kt; bill (US$ m) = ML × landed cost (US$/m³) / 1,000; KSh at 129.2. Constant volumes; illustrative.','Inventory cost: days × average daily demand (2025) × landed cost; carrying cost = 10% of inventory value (financing only).','Cooking-fuel cost per useful MJ = (price per kg) / (energy content × stove efficiency); energy content 46 MJ/kg LPG, 29 MJ/kg charcoal; efficiencies are illustrative.','Petrol displacement: share × 2035 baseline petrol kt × ML/kt × Aug-2026 landed cost.','Scenario sensitivities: the scenario function is re-run with one input changed (fade 0.6/1.0; shock 0/1.5×; elasticities 0.5×/2×; underlying growth +2/−1 points).','Regional spread = town price − Mombasa price, in KSh and %.'])
H(d,'5.8 Monte Carlo (South Lokichar)',2)
P(d,'2,000 draws (seed 42) from independent distributions: Brent log-normal(ln 70, 0.22) clipped to [35, 140]; differential U(3, 10); plateau triangular(40, 60, 100); capex triangular(5,000, 6,000, 8,500); opex + tariff triangular(15, 21, 28), split 12:9 between opex and tariff. Each draw runs the full cash-flow model. Reported: P10, median, P90, mean, probability NPV < 0, and Pearson correlation of each input with project NPV. Independence of inputs is a simplification (in reality capex and oil price co-move).')
H(d,'5.9 Excel model structure and verification',2)
T(d,['Sheet','Content','Live?'],[['README','Instructions and caveats','—'],['Dashboard','Key outputs linked to model sheets','Yes'],['Assumptions','Scenario selector (C3), growth, price shocks, elasticities, FX, conversion factors','Inputs'],['Demand_Data','Relabelled monthly data; annual SUMIFS, growth, shares','Yes'],['Prices','National price series; change and CV','Yes'],['Scenarios','2025–2035 by product, driven by selector','Yes'],['Supply_Security','Daily demand, capacity days, 30-day need, shortfall vs reported cover, traffic light, inventory value','Yes'],['LPG_Storage','Required storage vs installed + new capacity','Yes'],['Project_Economics','35-year cash flow, cost-recovery pool, NPV, IRR, government and contractor results','Yes'],['Sensitivity','Static tables from Python (grids, tornado, fiscal cases, scenario sensitivities)','Static']],widths=[3.5,10,3])
P(d,'Verification: the workbook was recalculated headlessly in LibreOffice and no cell returned an error; scenario and project outputs match the Python results to the figures quoted in Step 12.')
H(d,'6. Assumptions register')
T(d,['Assumption','Value','Basis'],[
 ['Litres per tonne','Diesel 1.189; petrol 1.388; jet 1.271; kerosene 1.271 ML/kt','Implied by PDP 2024 base'],
 ['Growth 2025–29','PDP baseline / optimistic / pessimistic by product','EPRA PDP, Section 4'],
 ['Growth 2030–35','0.8 × the 2025–29 rate','Author assumption'],
 ['2026 average price rise (high/base/low)','Diesel 10/20/30%; petrol 8/15/22%; LPG 5/10/20%; kerosene 10/20/30%; jet 0','Author, informed by Mar–Sep 2026 EPRA reviews'],
 ['LPG elasticity (SR/LR)','−0.15 / −0.30','Author assumption'],
 ['Kerosene elasticity (SR/LR)','−0.2 / −0.5','Author assumption'],
 ['Jet elasticity','0','Author assumption'],
 ['Fuel oil path','PDP: +4.68%/yr to 2027, then −3.19%/yr','EPRA PDP'],
 ['USD/KES for pass-through','129.2 (flat); 125–135 tested','Author assumption'],
 ['Stock-cover standard','30 days (15 operational + 15 strategic)','EPRA PDP'],
 ['Traffic-light thresholds','Green ≥ 30; amber 15–29; red < 15 days','Author framework (not official)'],
 ['Risk weights','Stock 25%, price 20%, infrastructure 15%, volatility 15%, concentration 15%, forecast 10%','Author framework; equal and stock-heavy weights tested'],
 ['Monte Carlo distributions','See Section 5.8','Author assumptions'],
 ['Cooking-fuel efficiencies','LPG 45–55%; charcoal 20–30%','Author illustration'],
 ['Inventory financing rate','10%','Author assumption'],
 ['South Lokichar','Brent $70; differential $6; plateau 60 kbpd; capex $6.0 bn; opex $12 + tariff $9; 10% discount; royalty 10%; cost cap 60%/80%; govt profit oil 50%/35%; no corporate tax','Headline facts from press; all else author assumptions']],widths=[4.2,7.6,4.7])
H(d,'7. Deviations from the original project brief')
T(d,['Original brief item','What was done','Why'],[
 ['Use LeadAfrik column labels as published','Relabelled petrol/LPG/jet/fuel oil columns','Labels failed reconciliation with EPRA and KNBS'],
 ['SARIMA, ARIMAX, Holt-Winters','ETS (damped), ARIMA(0,1,1), growth-adjusted seasonal naive, shrunk-seasonal trend','26 observations; no exogenous series'],
 ['Forecast to 2035 with intervals','12-month statistical forecast with intervals; 2025–35 scenario projections without statistical intervals','Horizon limited by data'],
 ['Elasticity from own regression','PDP-implied elasticities','Own regression wrong-signed'],
 ['Brent / FX pass-through regression','Two-point landed-cost pass-through','No monthly Brent/FX data'],
 ['Import dependence ratios','Structural 100% dependence; flagged data gap in imports vs demand','Imports are all refined; Survey tables not accessed'],
 ['Stock-cover days by product (incl. LPG)','Petrol, diesel, jet from statements; LPG via storage headroom','No LPG stock cover published'],
 ['Diesel storage 224.5 → 254.7 ML (from an earlier document)','Not used','Could not be verified in the PDP text retrieved'],
 ['South Lokichar Phase 1 20 kbpd / Phase 2 50 kbpd','Not used; 60–100 kbpd press range used','Conflict with press reports, unverified'],
 ['Excel model','Built (live formulas; verified against Python)','Delivered in the second iteration'],
 ['Interactive HTML dashboard (7 tabs)','Delivered','Hand-built with embedded data; open it in any browser'],
 ['Streamlit app, SQL schema','Not built','Not feasible to test in this environment; outputs are CSVs and the Excel model is the interactive tool'],
 ['Regional price spreads','Done from press-reported EPRA maxima (May and September 2026 cycles)','Town-level file was empty; secondary source']],widths=[4.8,6.3,5.4])
H(d,'8. Validation and checks performed')
B(d,['Row counts and key uniqueness of the raw files.','Reconciliation of corrected columns to PDP 2024 and KNBS 2025 (exact on four products; total within 0.2% of KNBS 2025).','Hold-out forecasting error reported on rolling origins; the PDP’s own 2025 baseline back-tested against actual 2025 (5.3% under).','Recomputation of PDP LPG storage logic (2025 spare ullage ≈ 4 kt) before applying it to new demand.','Cross-checking of every figure in the narrative against CSV outputs; consistency check of PDP supply (6,420) minus demand (5,933) = 30 days of demand.','Full clean re-run from raw data to final reports and the Excel model.','Second-pass review of every new number in the expanded report against the CSV outputs; this corrected four statements (petrol demand response in the stress test, KSh cost of holding prices flat, diesel first-year demand loss, ARIMA metric range).'])
H(d,'9. Reproducing the work')
code(d,'$ cd project_root\n$ pip install pandas numpy scipy matplotlib python-docx\n$ ./run_all.sh\n# outputs: data/clean/*.csv, figures/*.png, out/Kenya_Petroleum_Market_Outlook_2026-2035.docx')
d.add_page_break()
H(d,'Appendix A. Code listings')
names=[('code/common.py','Shared labels, conversion factors, loaders'),('code/01_prepare_data.py','Validation and reconciliation'),('code/02_demand_analysis.py','Demand analytics and figures 1–3'),('code/03_forecasting.py','Forecast tournament and 12-month forecasts'),('code/04_prices_elasticity.py','Prices, elasticity, pass-through'),('code/05_scenarios_security_risk.py','Scenarios, supply security, risk'),('code/lokichar_model.py','South Lokichar cash-flow function'),('code/06_project_economics.py','South Lokichar scenarios, break-evens, tornado'),('code/09_extended_analysis.py','Extended analysis and Monte Carlo'),('code/10_build_excel.py','Excel model builder')]
for i,(f,desc) in enumerate(names):
    H(d,f'A.{i+1} {f} – {desc}',2); code(d,open(f).read(),size=6.8)
H(d,'Appendix B. Output files')
B(d,[f.split('/')[-1] for f in sorted(glob.glob('data/clean/*.csv'))])
d.save('out/Kenya_Petroleum_Methods_and_Code_Report.docx')
