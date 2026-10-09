import pandas as pd, numpy as np
from docx_helpers import *
from common import ML_PER_KT
C='data/clean/'; FG='figures/'
d=new_doc()
S=pd.read_csv(C+'scenarios_kt.csv'); tot=S.groupby(['scenario','year']).kt.sum().unstack()
dsum=pd.read_csv(C+'demand_summary.csv',index_col=0); prof=pd.read_csv(C+'product_profiles.csv',index_col=0)
W=pd.read_csv(C+'consumption_relabelled_kt.csv',index_col=0,parse_dates=True)
# ---------- cover ----------
for _ in range(5): d.add_paragraph()
P(d,'KENYA PETROLEUM MARKET OUTLOOK',bold=True,size=30,align='c').runs[0].font.color.rgb=NAVY
P(d,'Demand, Prices, Supply Security and Investment Scenarios, 2026–2035',size=15,align='c')
P(d,'An evidence-based analytical report',italic=True,size=12,align='c')
for _ in range(4): d.add_paragraph()
P(d,'October 2026',size=12,align='c')
P(d,'Data: EPRA, KNBS (as published), LeadAfrik structured datasets, official and press-reported 2026 market data. Every assumption is labelled; scenario outputs are analytical constructs, not official forecasts or ministry classifications.',italic=True,size=9.5,align='c')
d.add_page_break()
# ---------- contents ----------
H(d,'Contents')
for t in ['Executive summary','Key figures at a glance','1. Introduction and 2026 market context','2. Market structure and institutions','3. Data and methodology','4. Historical demand (product profiles, seasonality, substitution)','5. Price dynamics (national, regional, pass-through)','6. Import dependence and the landed-cost bill','7. Price elasticity of demand','8. Demand forecasts','9. Scenario analysis 2025–2035 and sensitivities','10. Supply security and the cost of reserves','11. Infrastructure requirements','12. Upstream project economics: South Lokichar','13. Risk assessment','14. Structural change: energy transition and cooking fuels','15. Stress test: a repeat supply shock','16. Monitoring framework and early-warning indicators','17. Key findings','18. Policy considerations and implementation priorities','19. Limitations','20. Coverage of the original project brief','Glossary','Annex A–E: data tables, forecast metrics, assumptions, sources']:
    p=d.add_paragraph(t,style='List Bullet'); p.paragraph_format.space_after=Pt(1)
d.add_page_break()
# ---------- exec summary ----------
H(d,'Executive summary')
P(d,'Kenya’s petroleum market entered 2026 on a strong growth path and was then hit by one of the largest external shocks in its recent history. **Domestic demand rose 12.0% to 5.71 million tonnes in 2025** on the dataset used here (the Economic Survey 2026 reports +9.9% to 5.7 Mt; the difference is explained in Section 3). Diesel and petrol made up **71.4%** of demand, exactly the share KNBS reports. From 28 February 2026, the Gulf war and the effective closure of the Strait of Hormuz lifted landed fuel costs by roughly half, produced pump-queue shortages in April, and pushed Nairobi diesel from KSh 166.54 to KSh 242.92 per litre by May.')
P(d,'**Headline findings**',bold=True)
B(d,[
 '**Demand was accelerating before the shock.** 2025 growth by product: diesel +10.3% (2.42 Mt), petrol +12.5% (1.66 Mt), LPG +14.7% (476 kt). Jan–Feb 2026 total demand was still +7.1% year on year. No monthly volume data exist in the dataset after February 2026 (March is blank), so the effect of the shock on volumes is **not yet observed**; it is scenario-modelled here.',
 '**The published data labels are wrong in the main dataset.** The columns labelled “LPG” and “Other” are actually petrol and LPG. This was identified by matching each column to EPRA’s 2024 actuals (diesel, petrol, LPG and kerosene match to the decimal). Anyone using the labels as published would report LPG demand 3.5 times too high and petrol demand about half its true level.',
 '**Statistical forecasting is possible only for about 12 months.** With 26 monthly observations, a seasonal-naive-with-growth model beat every alternative for diesel, LPG and total demand (out-of-sample sMAPE 2.6–3.1%, versus 5–8% for naïve forecasts). Its no-shock counterfactual for March 2026–February 2027 is **6.37 Mt (80% interval 6.04–6.69 Mt)**. Beyond that, horizons to 2035 are scenario projections, not statistical forecasts.',
 '**Baseline demand reaches 6.3 Mt in 2030 and 7.2 Mt in 2035** (range 6.6–7.8 Mt in 2035 across low and high cases), a 2.3% annual average rate from the 2025 base. LPG grows fastest (to about 860 kt by 2035); kerosene keeps shrinking. The baseline is conservative relative to 2024–25 momentum: if underlying growth runs 2 points a year higher, 2035 demand would be 8.4 Mt (+17.5%).',
 '**Supply security, not tank space, was the binding constraint.** Licensed tank capacity equals roughly 73–96 days of 2025 demand if full, yet reported stocks in April–May 2026 were 13–28 days against the 30-day planning standard (15 operational plus 15 strategic). The gap was about 55–110 million litres for diesel and 13–107 million litres for petrol. Holding 30 days of petrol and diesel would tie up about US$390 million of product (KSh 51 billion) at August 2026 landed costs; 90 days, US$1.2 billion.',
 '**LPG is the one product with a physical infrastructure gap.** Required storage exceeds the 44.4 kt installed (March 2025) from 2026 in the baseline, reaching a 10.8 kt shortfall in 2029. Even if the 10 kt Lake Gas facility is commissioned, the gap re-opens by 2029.',
 '**Pump prices passed through most, not all, of the shock.** Petrol’s landed cost rose 50% (February to August 2026); the Nairobi pump price rose 20%. In shilling terms that is about 82% of the VAT-inclusive cost increase, the remainder cushioned by stabilisation support. At constant 2026 volumes, the higher landed cost adds about US$0.7 billion (KSh 89 billion) to the petrol import bill alone.',
 '**South Lokichar is oil-price-sensitive and fiscal-term-sensitive.** In an illustrative model (60 kbpd plateau, US$6 bn capex, US$70 Brent), the project earns an NPV10 of US$1.6 bn and 15% IRR with a break-even of US$60/bbl. A Monte Carlo on uncertain price, output and cost gives a 30% chance of negative project NPV; under the tougher fiscal case, the chance that the contractor’s NPV is negative is 73%. Whether a private developer earns an adequate return depends on fiscal terms that are not public: contractor break-even ranges from US$73 to US$82 across the two terms tested.',
 '**Risk ranking (analytical framework):** LPG HIGH; petrol and diesel MEDIUM; jet fuel LOW. Weight sensitivity tests leave LPG on top in all three weightings.'])
P(d,'**What policymakers should watch:** (1) stock cover by product against the 30-day standard; (2) March–December 2026 volume data when published, compared with the forecast intervals in Section 8; (3) diesel pass-through and stabilisation costs; (4) LPG storage commissioning; (5) concentration of supply on Gulf-origin cargoes; (6) Brent and the shilling.')
d.add_page_break()
H(d,'Key figures at a glance')
T(d,['Indicator','Value','Where'],[
 ['Total domestic demand 2025','5,712 kt (+12.0%; KNBS 5.7 Mt, +9.9%)','§3, §4'],
 ['Diesel + petrol share of demand 2025','71.4% (KNBS 71.4%)','§4'],
 ['Diesel / petrol / LPG demand 2025','2,419 / 1,657 / 476 kt','§4'],
 ['Jan–Feb 2026 total demand growth','+7.1% YoY (pre-shock)','§4'],
 ['Forecast Mar-26–Feb-27 (no-shock counterfactual)','6,365 kt; 80% PI 6,040–6,690','§8'],
 ['Baseline demand 2030 / 2035','6.31 Mt / 7.16 Mt (CAGR 2.3%)','§9'],
 ['Low–high demand range 2035','6.64–7.85 Mt','§9'],
 ['Nairobi diesel price Mar-26 → May-26 → Sep-26','KSh 166.54 → 242.92 → 217.86','§5'],
 ['Petrol landed cost Feb-26 → Aug-26','US$582 → US$874 per m³ (+50%)','§5, §6'],
 ['Petrol pass-through (KSh, VAT-incl.)','≈ 82%','§5'],
 ['Reported stock cover, Apr–May 2026','Petrol 13–28 days; diesel 16–23 days','§10'],
 ['Cost of 30 / 90 days of petrol + diesel stock','US$392 m / US$1,175 m (KSh 51 / 152 bn)','§10'],
 ['LPG storage headroom 2026 / 2029 (baseline)','−1.0 kt / −10.8 kt','§11'],
 ['South Lokichar base project NPV10 / IRR / break-even','US$1.55 bn / 15% / US$60 per bbl','§12'],
 ['Probability project NPV10 < 0 (Monte Carlo)','30%','§12'],
 ['Risk ratings','LPG high; petrol, diesel medium; jet low','§13']],widths=[7,7,2.5])
d.add_page_break()
# ---------- 1 ----------
H(d,'1. Introduction and 2026 market context')
P(d,'This report builds an integrated analysis of Kenya’s petroleum market: historical demand, price dynamics, import dependence, demand forecasts, scenarios to 2035, supply security, infrastructure needs, upstream project economics, a risk framework, structural change and a monitoring system. It is designed to be traceable: each number is tied to a source or to an explicit assumption, and what could not be established is stated. A companion Methods and Code Report documents every step, and an Excel model lets the reader change assumptions and see the results.')
H(d,'1.1 Objectives',2)
B(d,['Quantify what happened to demand in 2024–25 and how reliable the underlying data are.','Provide an out-of-sample-tested forecast for the next 12 months and transparent scenarios to 2035.','Measure supply-security exposure against the planning standard and cost the options for reserves.','Identify infrastructure gaps, product by product.','Illustrate the economics and risks of Kenya’s first large upstream project using explicit assumptions.','Define indicators that would give early warning of the next shock.'])
H(d,'1.2 The 2026 shock',2)
P(d,'The report’s original frame (growth to 2035 from a stable 2025 base) had to be reset because of events in 2026, drawn from news reports of official statements:')
T(d,['Date','Event','Source type'],[
 ['28 Feb 2026','US–Israel attacks on Iran begin; Strait of Hormuz flows effectively halted','News reports'],
 ['Mar 2026','Brent up roughly 60% in a month; Reuters poll lifts 2026 Brent forecast from US$63.85 to US$82.85','Reuters poll, press'],
 ['Mar 2026','EPRA cycle (15 Mar–14 Apr): Nairobi petrol KSh 178.28, diesel 166.54, kerosene 152.78, with subsidies on diesel and kerosene','EPRA via press'],
 ['Late Mar–Apr 2026','Queues, rationing and dry pumps reported in Nairobi, Nakuru, Eldoret, Kisumu, Nyeri; public statements on stock cover diverge (three months → 16 days petrol / 19 days diesel)','Press, Treasury statements'],
 ['14 May 2026','EPRA review: petrol +KSh 16.65 to 214.25; diesel +KSh 46.29 to 242.92','EPRA via press'],
 ['21 May 2026','EPRA states stock cover of 28 days (petrol) and 23 days (diesel)','EPRA via press'],
 ['Jul–Aug 2026','Landed cost of super petrol US$949/m³ (Jul), US$874/m³ (Aug); diesel pump price eased to 222.86 then 217.86','EPRA via press'],
 ['Late Aug–early Sep 2026','Brent about US$91–99','Market reports'],
 ['15 Sep–14 Oct 2026','Prices unchanged: petrol 214.03, diesel 217.86, kerosene 191.38, with stabilisation support','EPRA via press']],widths=[3.2,10.3,3.3],note='Several of these statements were contested; see Sections 10 and 19.')
P(d,'Kenya’s retail prices are regulated monthly by EPRA (announced on the 14th). Refined products are procured mainly through a government-to-government (G-to-G) framework with Gulf suppliers, set up in 2023; Kenya has no operating refinery and imports all refined products.')
# ---------- 2 ----------
H(d,'2. Market structure and institutions')
H(d,'2.1 The supply chain',2)
P(d,'The downstream chain runs from Kipevu Oil Terminal 2 at Mombasa (commissioned 2022; four berths) through common-user storage and the Kenya Pipeline Company’s multiproduct network to Nairobi, Nakuru, Eldoret and Kisumu, then by road to more than 5,800 retail stations and to neighbouring countries in transit (EPRA PDP 2025–29). Imports arrive as refined product; there is no operating refinery (KPRL is mothballed) and no commercial crude production.')
T(d,['Stage','Main elements (as described in the PDP)','Stress point in 2026'],[
 ['Import','Kipevu Oil Terminal 2 (KOT2); G-to-G contracts with Gulf suppliers; open tender for part of volume','Gulf-origin concentration; Hormuz closure'],
 ['Storage','Licensed depots at Mombasa, Nairobi, Nakuru, Eldoret, Kisumu; gross licensed capacity: diesel 755 ML, petrol 463 ML, jet 232 ML, kerosene 53 ML (Mar 2025); LPG 44.4 kt','Stocks held, not tank space'],
 ['Transport','KPC Line 1 (Mombasa–Nairobi), Line 2 (Nairobi–Eldoret), Line 3 (Sinendet–Kisumu) and Line 5; rail and road','Lines 2 and 3 at maximum utilisation'],
 ['Distribution','OMCs, >5,800 stations; regulated price build-up','Dry pumps, rationing'],
 ['Pricing','EPRA monthly maximum prices (15th–14th); VAT 16%; stabilisation support when prices spike','Pass-through ≈ 82%']],widths=[2.4,9.4,5])
H(d,'2.2 Regulation and the stock standard',2)
P(d,'The Petroleum Development Plan (PDP) assumes a 30-day stock cover: 15 days of minimum operational stocks plus 15 days of strategic reserve. It notes that in practice only the minimum operating stocks are maintained under the 2008 regulations, and that a strategic stocks regulation was in draft. This matters for the 2026 episode: the standard that the plan uses was not backed by a funded, legally operating strategic reserve.')
H(d,'2.3 Upstream',2)
P(d,'Kenya produces no commercial crude yet. The South Lokichar fields (Turkana) were acquired by Gulf Energy from Tullow in 2025; officials have targeted first oil by December 2026. Section 12 models the project economics under stated assumptions.')
# ---------- 3 ----------
H(d,'3. Data and methodology')
H(d,'3.1 Data inventory',2)
T(d,['Dataset','Coverage','Use','Status'],[
 ['LeadAfrik: consumption of petroleum fuels (KNBS LEI)','189 rows; Jan 2024–Mar 2026; 7 product columns','Core demand data','Used after relabelling; March 2026 blank'],
 ['LeadAfrik: national average retail prices (KNBS LEI)','75 rows; Jan 2025–Mar 2026; petrol, diesel, kerosene, LPG, charcoal','Price analysis','Used; complete'],
 ['LeadAfrik: Kenya pump prices by town (EPRA)','Header only','Regional spreads','Empty; replaced by press-reported EPRA maxima'],
 ['EPRA Petroleum Development Plan 2025–2029','Demand equations, scenarios, base year 2024, storage','Elasticities, growth rates, capacity','Used (primary document)'],
 ['KNBS Economic Survey 2026 (via press)','2025 demand, imports, exports','Validation anchors','Secondary'],
 ['EPRA monthly price reviews 2026 (via press)','Nairobi and regional maxima; landed costs','2026 price path and pass-through','Secondary'],
 ['Ministry / Treasury / EPRA statements (via press)','Stock cover days, Mar–May 2026','Supply security','Secondary; contested']],widths=[5,4.7,3.4,3.7])
H(d,'3.2 Data-quality finding: mislabelled product columns',2)
P(d,'Seven product columns were checked against independent anchors. Four match exactly; the labels on two (and the identity of two others) do not correspond to the products named:')
T(d,['Label as published','2024 sum (kt)','Matches','Reference value (kt)','Error','Confidence'],[
 ['AGO (Light Diesel Oil)','2,193.6','Diesel','2,193.6 (EPRA PDP)','0.0%','Confirmed'],
 ['LPG','1,472.7','**Petrol (PMS)**','1,472.7 (EPRA PDP)','0.0%','Confirmed'],
 ['Other','414.9','**LPG**','414.9 (EPRA PDP)','0.0%','Confirmed'],
 ['Illuminating Kerosene','37.1','Kerosene','37.1 (EPRA PDP)','0.1%','Confirmed'],
 ['Motor Spirit','732.3','Jet fuel (probable)','765.1 (EPRA PDP)','−4.3%','Medium'],
 ['Jet Oil','250.1','Fuel oil / other (probable)','301.9 (EPRA PDP)','−17.2%','Low–medium'],
 ['Aviation Gasoline','1.1','Avgas','n/a','—','Plausible']],widths=[3.8,2.2,3.4,3.4,1.6,2.2],
 note='Independent 2025 check: relabelled 2025 diesel = 2,419.1 kt (KNBS: 2,419.1); LPG = 476.0 kt (KNBS 475.9; +14.7%); diesel + petrol = 71.4% of the 5,712 kt total (KNBS: 71.4%). The total (5,712 kt) matches KNBS’s 5.7 Mt.')
P(d,'Because the labels are wrong, the report uses the relabelled columns and marks the two uncertain ones with an asterisk (Jet fuel*, Fuel oil/other*). Totals are unaffected. The label error probably arose when the source table was parsed; it should be reported to the data provider. The behaviour of the two uncertain columns reinforces the caution: the “jet fuel*” column fell year on year in 11 of 14 comparable months, and “fuel oil/other*” moved by +167% in one month and −16% in another. Neither pattern is conclusive, but both suggest that conclusions about these two products should wait for confirmation.')
P(d,'**Why 2025 growth is 12.0% here but 9.9% in the Economic Survey.** The 2025 total matches KNBS (5.71 vs 5.7 Mt), but the 2024 base in this dataset is 5.10 Mt versus about 5.20 Mt implied by KNBS. The difference (~96 kt) sits in the two uncertain columns, which also differ from EPRA’s annual values. Product-level growth for diesel, petrol and LPG is unaffected.')
H(d,'3.3 Validation steps applied',2)
B(d,['Structural: row counts (189 = 7 × 27), uniqueness of (month, product), removal of footer attribution lines.','Completeness: March 2026 blank for all products; 21 rows flagged provisional.','Reasonableness: annual sums per column against EPRA PDP 2024 actuals (full column × product error matrix).','Cross-source: relabelled 2025 values against KNBS Economic Survey 2026 (diesel, LPG, share of diesel+petrol, total).','Internal consistency: PDP planned supply minus demand equals exactly 30 days of demand; PDP LPG storage logic reproduced before being reused.','Out-of-sample: all forecasts evaluated on rolling origins; the PDP’s own 2025 forecast back-tested.'])
H(d,'3.4 Methods overview',2)
B(d,['Demand analytics: YoY and MoM growth, 3- and 12-month averages, shares, coefficient of variation, calendar-month seasonal indices.',
 'Forecast tournament: eight candidate models, rolling-origin evaluation (origins 18–25, horizons 1–6), model chosen per series on sMAPE. Prediction intervals come from the selected model’s own out-of-sample errors.',
 'Elasticities: our own regression (reported but rejected) and elasticities implied by EPRA’s published demand equations.',
 'Scenarios: growth rates from the PDP’s three scenarios, a 2026 price-shock adjustment using elasticities, a fade factor after 2029; one-at-a-time sensitivity tests.',
 'Supply security: days of cover, tank capacity versus requirement, inventory value, LPG storage using the PDP’s own method.',
 'Project economics: annual discounted cash-flow model with production-sharing-style fiscal logic, break-evens, sensitivity grid, tornado and Monte Carlo.',
 'Risk: transparent scoring with weight-sensitivity tests.'])
# ---------- 4 ----------
H(d,'4. Historical demand')
H(d,'4.1 Overview',2)
F(d,FG+'f1_monthly_demand.png','Figure 1. Monthly consumption by product, January 2024–February 2026 (thousand tonnes; March 2026 not available).')
T(d,['Product','2024 (kt)','2025 (kt)','Growth','Share 2025','Jan–Feb 2026 YoY','Monthly CV'],[
 ['Diesel (AGO)','2,193.6','2,419.1','+10.3%','42.3%','+9.0%','7.3%'],
 ['Petrol (PMS)','1,472.7','1,657.5','+12.5%','29.0%','+12.4%','9.2%'],
 ['LPG','414.9','476.0','+14.7%','8.3%','+11.0%','10.7%'],
 ['Jet fuel*','732.3','701.3','−4.2%','12.3%','−10.0%','5.6%'],
 ['Fuel oil/other*','250.1','413.3','+65.2%','7.2%','+0.2%','31.9%'],
 ['Kerosene (IK)','37.1','44.1','+18.9%','0.8%','+21.6%','12.3%'],
 ['**Total**','5,101.8','5,712.5','+12.0%','100%','+7.1%','7.8%']],widths=[3.2,2.0,2.0,1.8,2.0,2.8,2.0])
P(d,'**Interpretation.** Demand is dominated by transport fuels. Diesel (42%) and petrol (29%) move with road transport and freight; LPG (8%) is climbing quickly with the clean-cooking programme. The fastest percentage movers are small or uncertain categories: fuel oil/other* (volatile, CV 32%) and kerosene (<1% of volume).')
F(d,FG+'f2_annual.png','Figure 2. Annual consumption and 2025 growth by product.')
F(d,FG+'f3_yoy.png','Figure 3. Year-on-year growth by month, 2025–Feb 2026.')
P(d,'Growth was broad-based and sustained through 2025: total demand grew between 6.1% and 16.7% year on year in every month from January 2025 to February 2026, peaking in April 2025 (+16.7%) and June 2025 (+16.1%). The two largest products grew in every one of those 14 months (diesel +1.4% to +18.9%; petrol +5.3% to +23.9%).')
H(d,'4.2 Product profiles',2)
trend=dsum['trend%']
for pr,txt in [
 ('Diesel (AGO)','Diesel is the backbone of freight, public transport, agriculture and standby power. Monthly volumes ranged from 165.8 kt (June 2024) to 219.7 kt (October 2025). Year-on-year growth was positive in every comparable month. Its low volatility (CV 7.3%) and high share make it the most important single series for planning. The log-linear trend implies about 9% annual growth over the sample, close to the 10.3% annual-sum growth.'),
 ('Petrol (PMS)','Petrol demand peaked in December 2025 at 155.3 kt (December index 1.15) and troughed at 106.8 kt in June 2024. It grew faster than diesel (+12.5%), consistent with rising motorisation. It is also the most seasonal of the large products: June is 10% below the annual mean, December 15% above.'),
 ('LPG','LPG reached a record 43.7 kt in January 2026. Annual growth of 14.7% is the highest of the large products and matches the PDP’s expectation that LPG would be the fastest-growing fuel (7.3% a year baseline). Only one month of the 14 comparable (March 2025, −1.7%) showed a decline. LPG stays priced at about KSh 3,140 per 13 kg cylinder.'),
 ('Jet fuel*','Identified by magnitude only. Volumes were stable (54–67 kt a month) and fell year on year in 11 of 14 comparable months (−12.5% to +10.5%). A decline would be surprising for a growing aviation sector, which is one reason to treat the identification as unconfirmed.'),
 ('Fuel oil/other*','The most volatile series (CV 32%): from 13.1 kt (June 2024) to 41.8 kt (November 2025). Fuel oil use in thermal power generation is hydrology-dependent and could explain such swings, but this has not been verified. The PDP expects fuel oil to rise to 2027 and then decline.'),
 ('Kerosene (IK)','Kerosene is under 1% of demand (3.5 kt a month on average) and was expected by the PDP to decline 4.6% a year. In 2025, volume rose 18.9% (37.1 → 44.1 kt), which is not consistent with a steady decline; the series is small and noisy (best month YoY +57.8%, worst −11.8%).')]:
    P(d,f'**{pr}.** '+txt)
T(d,['Product','Mean (kt/month)','Max (month)','Min (month)','YoY range','Months with YoY growth','Log-trend (% pa)'],[[i,f"{prof.loc[i,'mean_kt']:.1f}",f"{prof.loc[i,'max_kt']:.1f} ({prof.loc[i,'max_month']})",f"{prof.loc[i,'min_kt']:.1f} ({prof.loc[i,'min_month']})",f"{prof.loc[i,'worst_yoy%']:+.1f} to {prof.loc[i,'best_yoy%']:+.1f}%",f"{prof.loc[i,'share_months_growing%']:.0f}%",f"{trend.loc[i]:+.1f}"] for i in prof.index],widths=[3,2.2,3.0,3.0,3.0,2.4,2.0],note='Computed on 26 months (Jan 2024–Feb 2026); YoY on the 14 months from Jan 2025.')
H(d,'4.3 Seasonality',2)
si=pd.read_csv(C+'seasonal_index.csv',index_col=0)
mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
T(d,['Month','Diesel','Petrol','LPG','Jet*','Total'],[[mn[i]]+[f"{si.loc[i+1,c]:.2f}" for c in ['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Total']] for i in range(12)],widths=[2,2.2,2.2,2.2,2.2,2.2],note='Seasonal index = month ÷ calendar-year mean, averaged over 2024 and 2025 (two observations per month; indicative only).')
F(d,FG+'f13_seasonal_overlay.png','Figure 4. Diesel and petrol by calendar month, 2024 (dotted) and 2025 (solid).')
P(d,'Demand is lowest in February and June (indices 0.90–0.94) and highest in July–October and December. The June trough is common to all large products. Because only two observations exist per month, the forecasting models shrink the seasonal component by half.')
H(d,'4.4 Drivers',2)
P(d,'The literature and the PDP identify price, income (GDP per capita), exchange rate, vehicle population, population and urbanisation, and substitute prices as drivers. Macroeconomic series (GDP, CPI) were not available monthly here, so the driver analysis is qualitative: 2025’s growth coincided with falling international crude prices, stable pump prices (diesel average KSh 169 per litre, a 1.9% coefficient of variation), 4.1% inflation, and expanding vehicle imports; transport inflation eased to 3.2%. The PDP’s own demand equations use fuel price, lagged demand and economic activity as drivers (Section 7).')
H(d,'4.5 Substitution: LPG and kerosene',2)
P(d,'The research question “is Kenya moving structurally away from kerosene?” cannot be answered from this window. Both fuels grew: LPG +14.7%, kerosene +18.9% (from a tiny 37 kt base, 0.8% of demand). The month-level year-on-year correlation is −0.28; the level correlation is +0.59 (common trend). The PDP projects kerosene falling 4.6% a year; the 2025 uptick is a reason to monitor, not evidence against the long-run decline.')
P(d,'**LPG versus charcoal.** The LPG-to-charcoal price ratio (per kg) fell 9.4% from January 2025 to March 2026 because charcoal prices rose 10.7% while LPG stayed flat. The cost of delivered cooking energy, under stated stove-efficiency assumptions, is below:')
ck=pd.read_csv(C+'cooking_cost_per_MJ.csv'); ck=ck[ck.month=='2026-03']
T(d,['LPG stove efficiency','Charcoal stove efficiency','LPG, KSh per useful MJ','Charcoal, KSh per useful MJ','LPG ÷ charcoal'],[[f"{r.LPG_stove_eff:.0%}",f"{r.charcoal_stove_eff:.0%}",f"{r.LPG_KSh_per_useful_MJ:.1f}",f"{r.charcoal_KSh_per_useful_MJ:.1f}",f"{r.LPG_over_charcoal:.2f}"] for r in ck.itertuples()],widths=[3.4,3.6,3.4,3.8,2.4],note='March 2026 prices: LPG KSh 3,134.75 per 13 kg (KSh 241/kg); charcoal KSh 94/kg. Energy content assumed 46 MJ/kg (LPG) and 29 MJ/kg (charcoal); efficiencies are the author’s illustrative assumptions, not measured values.')
P(d,'LPG is cheaper per unit of useful energy than charcoal unless the charcoal stove is efficient (30%) and the LPG stove is inefficient (45%). This supports the continued relative-price case for adoption but should not be read as a precise cost estimate; the 2026 shock, for which no LPG price data exist, may have moved the ratio.')
d.add_page_break()
# ---------- 5 ----------
H(d,'5. Price dynamics')
H(d,'5.1 National prices to March 2026',2)
F(d,FG+'f5_prices.png','Figure 5. Pump prices: LeadAfrik national averages to March 2026 and EPRA Nairobi maxima (via press reports) thereafter.')
P(d,'Through March 2026, administered prices were remarkably flat: petrol ranged KSh 175.30–187.37 per litre and diesel KSh 163.89–172.75 (CV below 2.5%); LPG ranged KSh 3,122–3,158 per 13 kg (CV 0.3%). Over the 15 months the changes are +1.2% (petrol), −0.1% (diesel), +0.3% (LPG), +10.7% (charcoal). Prices took only 7–8 distinct values: administered pricing means demand sees price changes in steps rather than as a continuous signal.')
F(d,FG+'f12_price_index.png','Figure 6. Price indices, January 2025 = 100.')
P(d,'Real versus nominal: monthly CPI was not available in this environment, so prices are nominal. With 2025 inflation reported at 4.1%, flat nominal prices imply a real decline of roughly 4% in 2025, which is consistent with strong volume growth, but this cannot be tested here.')
H(d,'5.2 The 2026 price path',2)
T(d,['EPRA cycle (Nairobi max)','Petrol KSh/L','Diesel KSh/L','Kerosene KSh/L','Diesel vs Mar-26 cycle'],[
 ['15 Mar–14 Apr 2026','178.28','166.54','152.78','—'],['15 May–14 Jun 2026','214.25','242.92','152.78','+45.9%'],
 ['15 Jul–14 Aug 2026','214.03','222.86','191.38','+33.8%'],['15 Aug–14 Sep 2026','214.03','217.86','191.38','+30.8%'],['15 Sep–14 Oct 2026','214.03','217.86','191.38','+30.8%']],widths=[4.6,2.6,2.6,2.8,3.6],
 note='Source: EPRA announcements as reported in the press. The April and June cycles were not retrieved. Nairobi maxima are not identical to the LeadAfrik national averages.')
P(d,'Relative to the March 2026 cycle, by September 2026 petrol was 20.1% higher, diesel 30.8% and kerosene 25.3%. Diesel peaked at 45.9% above March in May. Because diesel feeds transport and freight costs, its larger rise matters more for inflation than the petrol rise suggests.')
H(d,'5.3 Regional price spreads',2)
reg=pd.read_csv(C+'regional_spread_may26.csv')
T(d,['Town (May-26 cycle)','Petrol KSh/L','Diesel KSh/L','Kerosene KSh/L','Petrol premium over Mombasa','%'],[[r.town,f"{r.petrol_may26:.2f}",f"{r.diesel_may26:.2f}",'' if pd.isna(r.kerosene_may26) else f"{r.kerosene_may26:.2f}",f"{r.petrol_vs_mombasa:+.2f}",f"{r.petrol_vs_mombasa/211.09*100:+.1f}%"] for r in reg.itertuples()],widths=[3.4,2.5,2.5,2.7,3.6,1.6],note='Source: EPRA maxima as reported in the press. Mombasa (the import point) is the lowest-price reference. In the September cycle, Mandera petrol was KSh 234.68 versus KSh 210.87 in Mombasa (+KSh 23.81, +11.3%).')
P(d,'The regulated price structure embeds a transport gradient: prices rise with distance from Mombasa, from +1.5% in Nairobi to +11.3% in Mandera for petrol (unchanged between the May and September cycles at about KSh 24 per litre). The north-eastern border towns therefore face the highest absolute pump prices and the highest exposure to shocks, a distributional point for any stabilisation design. The Mombasa–Nairobi gap (about KSh 3 per litre) is small relative to the 2026 price movements (KSh 36–76 per litre).')
H(d,'5.4 Pass-through from international prices to the pump',2)
P(d,'A formal regression of Kenyan pump prices on Brent and USD/KES could not be run: monthly Brent and exchange-rate series were not available in this environment, and administered pump prices change in steps. Instead, EPRA’s own landed-cost statements give a transparent two-point calculation for petrol:')
T(d,['Exchange-rate assumption','Landed-cost rise (KSh/L)','Incl. 16% VAT','Pump-price rise (KSh/L)','Pass-through (ex-VAT)','Pass-through (vs VAT-incl.)'],[
 ['125','36.52','42.36','35.75','0.98','0.84'],['129.2 (central)','37.75','43.79','35.75','0.95','0.82'],['135','39.44','45.75','35.75','0.91','0.78']],widths=[3.2,3.0,2.4,3.0,2.6,3.0],
 note='Landed cost US$582.11/m³ (Feb-2026) → US$874.26/m³ (Aug-2026); Nairobi petrol KSh 178.28 → 214.03. Exchange rate is an assumption (flat); excise and margins are treated as fixed.')
P(d,'Petrol’s landed cost rose 50% while the pump price rose 20%. In absolute shilling terms about 82% of the VAT-inclusive increase was passed on; the difference is consistent with government stabilisation support (for example, a KSh 938 million allocation in the August cycle and per-litre subsidies of KSh 6.53 on diesel in the March cycle). Percentage pass-through is low because taxes and margins are fixed-per-litre components. The 2025 landed costs reported by EPRA (about US$620/m³ in September–October 2025) show that the price level before the shock was already about 6% above February 2026.')
# ---------- 6 ----------
H(d,'6. Import dependence and the landed-cost bill')
P(d,'Kenya imports **100%** of its refined petroleum: the Mombasa refinery (KPRL) is mothballed and there is no commercial crude production. Because dependence is structural, a ratio of imports to demand adds little at product level. What does differentiate products is source concentration and logistics. Petrol, diesel and kerosene are procured through G-to-G contracts with Gulf suppliers, which is why the Hormuz closure transmitted directly to Kenya.')
B(d,['**Volumes (KNBS Economic Survey 2026, via press):** imports 5.5 Mt in 2025 (+12.2%); exports 983.5 kt, of which re-exports 940.6 kt; net imports about 4.5 Mt; domestic demand 5.7 Mt.',
 '**An unreconciled gap.** Net imports (4.5 Mt) are about 1.2 Mt below domestic demand (5.7 Mt). Stock drawdown, LPG channels, and category definitions could explain part; the Survey tables should be checked directly before relying on a ratio.',
 '**Import bill.** Press reports for 2025 differ (about KSh 511–529 billion), so no figure is used.'])
H(d,'6.1 What the 2026 landed-cost increase means for the import bill',2)
bl=pd.read_csv(C+'landed_cost_bill.csv')
T(d,['Product','2026 baseline volume (ML)','Landed cost: from → to (US$/m³)','Bill at lower cost (US$ m)','Bill at higher cost (US$ m)','Increase (US$ m)','Increase (KSh bn)'],[[r['product'],f"{r.volume_ML_2026base:,.0f}",f"{r.landed_a_USD_m3:.0f} → {r.landed_b_USD_m3:.0f}",f"{r.bill_a_USDm:,.0f}",f"{r.bill_b_USDm:,.0f}",f"{r.increase_USDm:,.0f}",f"{r.increase_KShbn:.0f}"] for _,r in bl.iterrows()],widths=[2.4,2.6,3.2,2.4,2.4,2.0,2.0],note='Constant 2026 baseline volumes; petrol compares Feb-26 with Aug-26 landed cost; diesel compares Jul-26 with Aug-26 because the February 2026 diesel landed cost was not retrieved, so the diesel increase is a lower bound for the full shock. KSh at 129.2 per US$. Illustrative arithmetic, not a customs-based import bill.')
P(d,'At constant volumes, the petrol shock alone adds roughly US$0.7 billion a year (about KSh 89 billion). Diesel adds at least US$0.3 billion even on a Jul-to-Aug comparison. The exchange-rate channel is separate: each 1% depreciation of the shilling raises the shilling cost of the whole bill by 1%.')
# ---------- 7 ----------
H(d,'7. Price elasticity of demand')
P(d,'**Own estimate (rejected).** A log-log regression of monthly demand on price with a time trend, using the 14 months for which both exist, gives *positive* price elasticities: diesel +1.65 (95% CI 0.72 to 2.58; Newey-West) and petrol +0.69 (−0.33 to 1.71). Positive signs mean the regression is capturing the common trend and the July–October seasonal demand peak, which coincided with a mid-2025 price increase, not demand response. Prices took only 7–8 distinct values over the sample. The data cannot identify an elasticity, and none is reported as a finding. This failure is informative: administered, infrequently changing prices with a short window and strong trend growth give no usable price variation.')
P(d,'**Elasticities implied by EPRA’s demand equations** (PDP 2025–29, Section 3.4), evaluated at 2024 base values:')
T(d,['Product','Coefficient on price','Short-run elasticity','Lag coefficient','Long-run elasticity'],[
 ['Diesel','−2.7057 ML per KSh/L','−0.185','0.6754','−0.57'],['Petrol','−1.0243 ML per KSh/L','−0.096','0.6284','−0.26']],widths=[2.8,4.4,3.2,2.8,3.0],
 note='Short-run = coefficient × price / quantity (178.30/2,608 ML diesel; 191.8/2,044 ML petrol). Long-run = short-run / (1 − lag coefficient).')
P(d,'**Reading.** A 10% sustained rise in diesel price cuts diesel demand by about 1.9% within the year and about 5.7% in the long run, holding other factors constant. Demand for transport fuel is inelastic in the short run; shocks show up first as price and stock stress, not as demand destruction. These elasticities are used in the scenarios. The shock of 2026 (diesel +20% on average in the baseline) therefore removes about 3.3% of diesel demand in the first year and a further 7% over 2027–28 if prices stay high.')
P(d,'For LPG, kerosene and jet fuel, no elasticities are available from the PDP text retrieved; the scenarios use assumed values (LPG −0.15/−0.30; kerosene −0.2/−0.5; jet 0), which should be replaced when estimates are available.')
d.add_page_break()
# ---------- 8 ----------
H(d,'8. Demand forecasts')
H(d,'8.1 Forecasting tournament',2)
P(d,'Eight models were evaluated on rolling origins (train on the first 18–25 months, forecast up to six months ahead; 33 forecast-error observations per model and series). Metrics: MAE, RMSE, MAPE, sMAPE, MASE. Note that SARIMA/ARIMAX and full Holt-Winters are not estimable with two seasonal cycles and no long exogenous series.')
tt=pd.read_csv(C+'forecast_tournament.csv'); piv=tt.pivot(index='model',columns='series',values='sMAPE')[['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Total']]
T(d,['Model (sMAPE, %)']+list(piv.columns),[[m]+[f'{v:.2f}' for v in piv.loc[m]] for m in piv.index],widths=[5.2,2.2,2.2,2.0,2.2,2.0],note='Lower is better. Best per series: diesel, LPG, total = seasonal naive × growth; petrol = log-trend + shrunk seasonal; jet = mean of last 6 months.')
best=tt.loc[tt.groupby('series').sMAPE.idxmin()].set_index('series')
T(d,['Series','Selected model','MAE (kt)','RMSE (kt)','MAPE %','sMAPE %','MASE'],[[s,best.loc[s,'model'],f"{best.loc[s,'MAE']:.1f}",f"{best.loc[s,'RMSE']:.1f}",f"{best.loc[s,'MAPE']:.2f}",f"{best.loc[s,'sMAPE']:.2f}",f"{best.loc[s,'MASE']:.2f}"] for s in ['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Total']],widths=[3,5,1.8,1.8,1.6,1.6,1.4])
P(d,'Why the simple models win: with a strongly trending, short series, the models that carry forward both last year’s seasonal shape and the recent growth rate dominate. Naïve and seasonal-naive forecasts without growth adjustment have sMAPE of 5–12%, because they ignore the 10%+ annual trend. Damped-trend ETS (sMAPE 4.3–6.7%) and ARIMA(0,1,1) (4.8–7.2%) adapt to the trend but lose the seasonal pattern.')
F(d,FG+'f11_backtest.png','Figure 7. One-month-ahead out-of-sample forecasts from the selected models (red dots) against actual (line).',w=15)
P(d,'**Caution on model selection.** With eight origins and overlapping errors, the selected model’s advantage is indicative. The winning growth-adjusted seasonal naive assumes that the growth of the latest six months persists; that is a reasonable description of a market on a 10–12% growth path and exactly the assumption the 2026 shock puts in doubt.')
H(d,'8.2 Twelve-month forecast (a no-shock counterfactual)',2)
F(d,FG+'f4_forecasts.png','Figure 8. Out-of-sample selected-model forecasts with 80% and 95% prediction intervals, March 2026–February 2027.',w=15)
T(d,['Product','Mar-26–Feb-27 central (kt)','80% interval','95% interval'],[
 ['Diesel (AGO)','2,737','2,570–2,904','2,482–2,993'],['Petrol (PMS)','1,904','1,795–2,014','1,736–2,072'],['LPG','554','530–578','518–590'],['Jet fuel*','684','646–723','625–744'],['**Total (all products)**','6,365','6,040–6,690','5,868–6,861']],widths=[4.2,4.6,3.6,3.6],
 note='Intervals: forecast ± 1.28 / 1.96 × RMSE of the selected model’s rolling-origin errors at each horizon (beyond horizon 6, scaled by √(h/6)). Because errors are few, treat intervals as approximate and likely too narrow.')
P(d,'These forecasts are trained only on pre-shock data (to February 2026). They answer “what if 2024–25 growth had continued?”, not “what will 2026 be?”. The actual March–September 2026 volumes should be compared with these intervals as soon as they are published; a systematic miss below the 95% lower bound would quantify demand destruction and rationing.')
H(d,'8.3 How good was the official plan? A back-test of the PDP',2)
bt=pd.read_csv(C+'pdp_backtest.csv',index_col=0)
T(d,['Product','PDP baseline forecast for 2025 (kt)','Actual 2025 (kt)','Error (actual vs forecast)'],[[i,f"{bt.loc[i,'PDP_2025_fc_kt']:,.1f}",f"{bt.loc[i,'Actual_2025_kt']:,.1f}",f"{bt.loc[i,'error_%']:+.1f}%"] for i in bt.index],widths=[4,4.8,3.4,4],note='PDP forecasts from Table 4.4 (kt); the PDP was published in mid-2025.')
P(d,'The PDP’s baseline underestimated 2025 demand by 5.3% in total, with diesel 5.3% low and petrol and LPG 6.7% low. The direction matters for planning: infrastructure and stock requirements built on the PDP baseline start 5–7% short of the observed base. A reasonable use is to treat the PDP optimistic scenario as the central planning case until volumes normalise.')
# ---------- 9 ----------
H(d,'9. Scenario analysis, 2025–2035')
P(d,'**Design.** Baseline, high-demand and low-demand scenarios use EPRA’s PDP growth rates for 2025–2029 (diesel 3.52/4.28/2.74% per year; petrol 3.35/4.08/2.97%; LPG 7.26/8.82/6.34%; jet 1.87/2.17/1.70%; kerosene −4.57/−3.86/−5.29%, for baseline/optimistic/pessimistic). Growth for 2030–35 is **assumed** to be 80% of the 2029 rate. A 2026 price shock reduces demand using the elasticities in Section 7: baseline diesel price +20%, petrol +15%, LPG +10%, kerosene +20%; high-demand case +10/+8/+5/+10%; low-demand +30/+22/+20/+30%. The long-run response is phased over 2027–28. Fuel oil follows the PDP’s up-then-down path; avgas is held flat.')
T(d,['Total demand (Mt)','2025','2026','2030','2035','CAGR 2025–35'],[[sc]+[f'{tot.loc[sc,y]/1000:.2f}' for y in (2025,2026,2030,2035)]+[f'{((tot.loc[sc,2035]/tot.loc[sc,2025])**.1-1)*100:.1f}%'] for sc in ['Low-demand','Baseline','High-demand']],widths=[3.8,2.2,2.2,2.2,2.2,3.0])
F(d,FG+'f6_scenarios.png','Figure 9. Total petroleum demand by scenario (Mt).')
pv=S[S.year.isin([2025,2030,2035])].pivot_table(index=['product','scenario'],columns='year',values='kt').round(0)
rows=[]
for p in ['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Kerosene (IK)','Fuel oil/other*']:
    rows.append([p,f"{pv.loc[(p,'Baseline'),2025]:,.0f}"]+[f"{pv.loc[(p,s),2030]:,.0f}" for s in ('Low-demand','Baseline','High-demand')]+[f"{pv.loc[(p,s),2035]:,.0f}" for s in ('Low-demand','Baseline','High-demand')])
T(d,['Product (kt)','2025','2030 Low','2030 Base','2030 High','2035 Low','2035 Base','2035 High'],rows,widths=[3.2,1.6,1.9,1.9,1.9,1.9,1.9,1.9])
P(d,'**Reading.** (a) The baseline 2026 total is only +1.6% because the price shock offsets underlying growth; the low-demand case is flat. (b) The PDP baseline is conservative relative to recent experience: the PDP’s 2025 baseline (5,426 kt) was **5.3% below** actual 2025 demand (5,712 kt). The scenarios inherit that conservatism: the high-demand case is closer to the momentum seen in 2024–25. (c) These are assumption-driven projections, not statistically estimated forecasts.')
H(d,'9.1 Sensitivity of the baseline to key assumptions',2)
ssn=pd.read_csv(C+'scenario_sensitivity.csv')
T(d,['Case (one change at a time)','Total 2030 (kt)','Total 2035 (kt)','2035 vs baseline'],[[r.case,f"{r.total_2030_kt:,.0f}",f"{r.total_2035_kt:,.0f}",f"{r[3]:+.1f}%"] for r in ssn.itertuples(index=False)],widths=[7.5,2.8,2.8,3.2])
P(d,'The biggest swing factor is **underlying growth**, not the 2026 shock: adding 2 points a year (closer to 2024–25 experience) raises 2035 demand by 17.5%, while lowering growth by 1 point cuts it by 7.8%. Removing the 2026 price shock raises 2035 demand by 6.0%; doubling the elasticities lowers it by 5.5%. Planning should therefore focus on tracking underlying growth in 2026–27 data.')
H(d,'9.2 What the scenarios imply for stock and storage requirements',2)
rows=[]
for p in ['Diesel (AGO)','Petrol (PMS)','Jet fuel*']:
    r=[p]
    for sc_,y in [('Baseline',2025),('Baseline',2030),('High-demand',2030),('Baseline',2035),('High-demand',2035)]:
        q=S[(S.scenario==sc_)&(S.year==y)&(S['product']==p)].kt.iloc[0]; r.append(f"{q*ML_PER_KT[p]/365*30:,.0f}")
    rows.append(r)
T(d,['ML required for 30-day cover','2025','2030 Base','2030 High','2035 Base','2035 High'],rows,widths=[4.6,2.2,2.5,2.5,2.5,2.5],note='30 × daily demand, using PDP-implied litres per tonne. Compare with gross licensed capacity: diesel 755 ML, petrol 463 ML, jet 232 ML.')
P(d,'Even under the high-demand case in 2035, the 30-day requirement for each white fuel is well below today’s gross licensed capacity, so the storage question is about ownership, financing and location (inland versus coastal), not total tank volume, with the exception of LPG (Section 11).')
d.add_page_break()
# ---------- 10 ----------
H(d,'10. Supply security')
H(d,'10.1 Stock cover against the planning standard',2)
P(d,'The PDP’s standard is 30 days: 15 days of minimum operational stock plus 15 days of strategic reserve. Reported stock-cover figures in 2026 (official statements as carried by the press) were:')
T(d,['Product','Treasury / Ministry report, ~2 April','Ministry report, adjusted, ~2 April','EPRA, 21 May','Gap to 30 days (days)'],[
 ['Petrol','16 days','13 days','28 days','2 to 17'],['Diesel','19 days','16 days','23 days','7 to 14'],['Jet fuel','49 days','46 days','—','none']],widths=[2.6,4.0,3.6,2.6,3.2],
 note='Figures were publicly contested and not independently verified here. The adjusted figures reflect the Ministry’s own estimate of remaining days as at 2 April.')
P(d,'At 2025 average daily demand (petrol 6.3 million litres, diesel 7.9 million litres), the shortfall against 30 days is **13–107 million litres of petrol and 55–110 million litres of diesel**, depending on which statement is used. Importantly, the spread between statements (13 to 28 days for petrol) is itself a finding: Kenya lacked a single, published, audited daily stock-cover indicator at the moment it was most needed.')
H(d,'10.2 Tanks were not the constraint',2)
sc=pd.read_csv(C+'security_capacity.csv')
T(d,['Product','Daily demand 2025 (ML)','Gross licensed capacity (ML)','Days of demand if every tank were full','Stock needed for 30 days (ML)'],[[r['product'],f"{r['daily_demand_ML(2025)']:.1f}",f"{r['gross_capacity_ML']:.0f}",f"{r['gross_days_if_full']:.0f}",f"{r['ML_for_30d_cover']:.0f}"] for _,r in sc.iterrows()],widths=[3.0,3.2,3.4,4.0,3.2],
 note='Capacity: PDP Table 5.7 (licensed facilities, March 2025). Gross capacity overstates usable space (tank bottoms, working stock, product segregation, transit volumes). Conversion litres per tonne are those implied by the PDP base year.')
P(d,'Gross capacity covers 73–96 days of demand against a 30-day requirement, so the 2026 stress came from **inventory and procurement** (what was in the tanks and when cargoes arrived), not from lack of tank space. This changes the investment message: building strategic reserves means financing and owning product, not just tanks.')
H(d,'10.3 What reserves would cost',2)
inv=pd.read_csv(C+'inventory_cost.csv')
T(d,['Days of petrol + diesel cover','Volume (ML)','Inventory value (US$ m)','Inventory value (KSh bn)','Carrying cost at 10% (US$ m a year)','(KSh bn a year)'],[[f"{r.days_of_cover:.0f}",f"{r.volume_ML:,.0f}",f"{r.inventory_USDm:,.0f}",f"{r.inventory_KShbn:,.1f}",f"{r.carry_10pct_USDm_pa:,.0f}",f"{r.carry_10pct_KShbn_pa:,.1f}"] for r in inv.itertuples()],widths=[3.2,2.2,3.0,3.0,3.4,2.0],note='Valued at August 2026 landed costs (petrol US$874/m³; diesel US$957/m³) and 2025 average daily demand; 129.2 KSh per US$. Financing cost only; excludes storage fees, losses and rotation. Illustrative arithmetic.')
P(d,'The strategic half of the PDP standard (15 days of petrol and diesel) would tie up about US$196 million (KSh 25 billion) in product at 2026 prices, costing roughly US$20 million (KSh 2.5 billion) a year to finance at 10%. Bringing cover to 90 days, as some commentators have argued, would require about US$1.2 billion (KSh 152 billion) in inventory and about KSh 15 billion a year in financing, around 85% of licensed white-fuel capacity. Because inventory is priced at the cost of the day, a reserve bought during a price spike costs far more than one built gradually in calm markets: an argument for a rules-based, gradual build.')
H(d,'10.4 Supply-security traffic light (analytical framework)',2)
P(d,'Thresholds are the author’s, not official: GREEN ≥ 30 days (PDP standard); AMBER 15–29 days; RED < 15 days. Using the lowest reported April figure: petrol AMBER/RED boundary (13–16 days), diesel AMBER (16–19), jet GREEN (46–49), LPG **not reported** (no published stock cover; flagged as a data gap). A supply–demand balance sheet by product (opening stock, imports, production, consumption, exports, closing stock) could not be constructed because monthly stock and import-by-product data were not available; this is the most valuable data to request from EPRA and KRA.')
# ---------- 11 ----------
H(d,'11. Infrastructure requirements')
P(d,'**White fuels.** The PDP concludes that storage is adequate for petrol, diesel, kerosene and jet fuel through 2029, and recommends upgrading Mombasa–Nairobi Line 5, building a Line 7 by 2028 and a Sinendet–Kisumu pipeline by 2029. Two PDP statements are worth noting: Line 2 (Nairobi–Eldoret) and Line 3 (Sinendet–Kisumu) already run at maximum utilisation; and the planning supply for 2025 is 6,420 million litres against white-fuel demand of 5,933 million litres, the difference being exactly 30 days of demand.')
P(d,'**LPG.** Using the PDP’s own method (required storage = planned supply ÷ 12, where planned supply = demand × (1 + 30/365)), and demand from this report’s scenarios:')
L=pd.read_csv(C+'lpg_storage.csv'); Lb=L[L.scenario=='Baseline'].set_index('year')
T(d,['Year','Baseline demand (kt)','Required storage (kt)','Installed (kt)','Headroom (kt)'],[[str(y),f"{Lb.loc[y,'demand_kt']:.0f}",f"{Lb.loc[y,'required_storage_kt']:.1f}",'44.4',f"{Lb.loc[y,'headroom_kt']:+.1f}"] for y in (2025,2026,2027,2028,2029,2030)],widths=[2,4,4,3,3],note='Installed capacity as at March 2025 (PDP). The 10 kt Lake Gas facility, expected by June 2025 in the PDP, is not in the 44.4 kt; its commissioning status was not verified.')
F(d,FG+'f7_lpg_storage.png','Figure 10. Required LPG storage by scenario against installed capacity.',w=14.5)
Lx=L[L.year.isin([2026,2028,2030])].pivot(index='scenario',columns='year',values='headroom_kt')
P(d,'Baseline demand overtakes installed LPG storage in 2026 (−1.0 kt) and the shortfall reaches 10.8 kt in 2029 (EPRA’s own estimate is +8.7 kt needed by 2029 because its demand base was lower). If Lake Gas is operating, headroom is about +9 kt in 2026 but turns negative again in 2029 (−0.8 kt). By 2030 the shortfall is 14 kt in the baseline (without Lake Gas). The PDP also flags rail-linked secondary storage (10 kt at Nairobi) and a 30 kt PPP project at KPRL as responses. LPG’s overall policy importance, +14.7% a year with a clean-cooking mandate, makes this the clearest investment gap.')
T(d,['LPG headroom (kt), no new capacity','2026','2028','2030'],[[sc_]+[f"{Lx.loc[sc_,y]:+.1f}" for y in (2026,2028,2030)] for sc_ in ['Low-demand','Baseline','High-demand']],widths=[6,3,3,3])
H(d,'11.1 Infrastructure summary',2)
T(d,['Element','Status (PDP, 2025)','Assessment in this report'],[
 ['White-fuel tank capacity','Adequate to 2029','Adequate through 2035 even under high demand; the constraint is inventory ownership'],
 ['KPC Lines 2 and 3','At maximum utilisation','Throughput risk if demand follows the high case; Line 7 and Sinendet–Kisumu timing matter'],
 ['Line 5 upgrade, Line 7 (2028)','Planned','Supported by demand growth in all scenarios'],
 ['LPG import/storage','44.4 kt; ~4 kt spare in 2025','Short from 2026 in the baseline; urgent'],
 ['Strategic reserve','15 days operational only in practice','Policy and financing gap, not a physical one']],widths=[4.5,4.5,7.7])
# ---------- 12 ----------
H(d,'12. Upstream project economics: South Lokichar (illustrative)')
callout(d,'**Important.** This is a public-information scenario model. Headline facts are from press reports: Gulf Energy’s US$6 bn investment commitment, 60,000–100,000 barrels/day early production, about 560 million barrels recoverable, first oil targeted for December 2026, and reported tax exemptions and enhanced cost-recovery terms. **Costs, fiscal terms, decline rates and the production profile below are the author’s assumptions, not official or confidential project economics.** Progress against the December 2026 target could not be verified. An earlier document’s reference to 20 and 50 kbpd phases conflicts with press reports and was not used.')
T(d,['Assumption','Base value'],[['Brent (real, flat)','US$70/bbl'],['Crude differential to Brent','US$6/bbl'],['Plateau production','60 kbpd, 2029–2037 (ramp 33% / 66% in 2027 / 2028)'],['Decline after plateau','10% a year; capped at 560 mmbbl; economic limit applied'],['Capex','US$6.0 bn, phased 15/35/30/20% over 2026–29; abandonment 3% of capex'],['Opex + transport tariff','US$12 + US$9 per barrel'],['Discount rate (real)','10%'],['Fiscal case A','Royalty 10%; cost recovery cap 60% of net revenue; government profit-oil share 50%; no corporate tax'],['Fiscal case B','Royalty 10%; cap 80%; government share 35%; no corporate tax']],widths=[5,11.5])
sc2=pd.read_csv(C+'lokichar_scenarios.csv'); fc=pd.read_csv(C+'lokichar_fiscal_cases.csv'); be=pd.read_csv(C+'lokichar_breakeven.csv',index_col=0).iloc[:,0]
P(d,f'**Base case results.** Project (pre-fiscal) NPV10 **US$1.55 bn**, IRR **15%**, payback in 2034, break-even Brent **US${be["be_proj"]:.0f}/bbl** (project). Cumulative production 398 million barrels of the 560 million recoverable (the rest lies beyond the economic limit under a 10% decline). Government take (royalty plus profit oil, case A): NPV10 **US$2.8 bn**, US$7.1 bn undiscounted, about 64% of project net cash flow. Under case A the contractor’s NPV10 is **negative (−US$1.3 bn)** at US$70, with a contractor break-even of **US$82/bbl**; under the more investor-friendly case B the break-even is **US$73/bbl**.')
cf=pd.read_csv(C+'lokichar_cashflow_base.csv'); cfs=cf[cf.year.isin([2026,2027,2028,2029,2030,2032,2035,2037,2040,2045,2050])]
T(d,['Year','kbpd','mmbbl','Revenue (US$ m)','Opex+tariff','Capex','Pre-fiscal CF','Govt take','Contractor CF'],[[int(r.year),f"{r.kbpd:.0f}",f"{r.mmbbl:.1f}",f"{r.revenue:,.0f}",f"{r.opex:,.0f}",f"{r.capex:,.0f}",f"{r.pre_fiscal_cf:,.0f}",f"{r.gov_take:,.0f}",f"{r.contractor_cf:,.0f}"] for r in cfs.itertuples()],widths=[1.4,1.3,1.5,2.4,2.0,1.6,2.2,2.0,2.2],note='Selected years of the base-case cash flow (US$ million; fiscal case A).')
F(d,FG+'f9_lokichar_profile.png','Figure 11. Base-case production and cumulative pre-fiscal cash flow.',w=15)
rows=[[f"{int(r.brent)}",f"{int(r.plateau_kbpd)}",f"{r.NPV_project:,.0f}",f"{r.IRR_project*100:.0f}%" if r.IRR_project==r.IRR_project else 'n/a',f"{r.NPV_gov:,.0f}",str(int(r.payback_year))] for r in sc2.itertuples()]
T(d,['Brent (US$)','Plateau (kbpd)','Project NPV10 (US$ m)','Project IRR','Govt NPV10 (US$ m)','Payback'],rows,widths=[2.4,2.6,3.6,2.4,3.4,2.2])
g=pd.read_csv(C+'lokichar_grid_npv_project.csv',index_col=0)
T(d,['Brent \\ plateau']+[f'{c} of 60 kbpd' for c in g.columns],[[f'US${i}']+[f'{v:,.0f}' for v in g.loc[i]] for i in g.index],widths=[3,2.7,2.7,2.7,2.7,2.7],note='Project NPV10, US$ million.')
F(d,FG+'f8_tornado.png','Figure 12. Tornado: change in project NPV10 for each driver.',w=15)
P(d,'**Reading.** The oil price dominates (a US$55–85 range moves NPV by about US$4.7 bn), then plateau output (US$2.7 bn), capex (US$2.1 bn), the discount rate, operating plus tariff costs, and the crude differential. At Brent US$90, near August–September 2026 levels, the 60 kbpd project is worth US$4.7 bn at the project level; the geopolitical premium is temporary by most forecasts, so a long-run price deck is the right basis for the decision.')
H(d,'12.1 Fiscal terms: who gets what',2)
T(d,['Fiscal case','Brent','Contractor NPV10 (US$ m)','Contractor IRR','Govt NPV10 (US$ m)','Govt share of net cash flow','Contractor break-even Brent'],[[r.fiscal_case.split(' (')[0],f"{int(r.brent)}",f"{r.NPV_contractor:,.0f}",f"{r.IRR_contractor*100:.1f}%",f"{r.NPV_gov:,.0f}",f"{r.gov_share_pct:.0f}%",f"US${r.contractor_breakeven_brent:.0f}"] for r in fc.itertuples()],widths=[2.8,1.4,3.0,2.2,2.8,2.6,2.6],note='Case A: cost cap 60%, government profit oil 50%. Case B: cap 80%, government 35%. Both: royalty 10%, no corporate tax. Assumptions, not contract terms.')
P(d,'The government’s NPV is positive and large in every case, because royalty and early profit oil are paid on revenue before the contractor recovers costs. Under the tougher case A the contractor does not earn its cost of capital below about US$82; this is why the stated fiscal incentives matter. A government facing a developer that needs US$73–82 Brent to break even has less room to raise take, and more to gain from lower costs and shorter timelines.')
H(d,'12.2 Monte Carlo: price, output and cost uncertainty together',2)
P(d,'2,000 random draws of: Brent (log-normal around US$70, σ 22%, bounded US$35–140), differential (US$3–10), plateau output (triangular 40/60/100 kbpd), capex (triangular US$5.0/6.0/8.5 bn, skewed to overruns) and opex plus tariff (triangular US$15/21/28). The distributions are the author’s assumptions.')
mc=pd.read_csv(C+'lokichar_mc_summary.csv',index_col=0)
T(d,['US$ million (NPV10)','P10','Median','P90','Mean','Probability < 0'],[[nm]+[f"{mc.loc[i,col]:,.0f}" for i in ['0.1','0.5','0.9','mean']]+[f"{mc.loc['P(NPV<0)',col]*100:.0f}%"] for nm,col in [('Project (pre-fiscal)','npv_project'),('Contractor (case A)','npv_contractor'),('Government (case A)','npv_gov')]],widths=[4.2,2.2,2.2,2.2,2.2,3],note='Same draws used for all three rows.')
F(d,FG+'f10_montecarlo.png','Figure 13. Distribution of project NPV10 across 2,000 draws.',w=14.5)
mcr=pd.read_csv(C+'lokichar_mc_corr.csv',index_col=0).iloc[:,0]
P(d,f'The project’s median NPV is about US$1.6 bn but the range is wide: P10 is −US$1.7 bn and P90 +US$6.6 bn. There is a 30% chance that the project value is negative and a 73% chance that the contractor’s is negative under fiscal case A. The government’s NPV is positive in every draw, which is the sense in which an upstream project with royalty and profit-oil provisions transfers risk to the developer. Pearson correlations of the inputs with project NPV: Brent {mcr["brent"]:.2f}, plateau output {mcr["plateau"]:.2f}, capex {mcr["capex"]:.2f}, differential {mcr["diff"]:.2f}, opex plus tariff {mcr["opex_tariff"]:.2f}. Oil price explains most of the spread.')
P(d,'**Implications for Kenya.** (1) Project value is mostly a bet on oil prices, so the 2026 price spike should not be allowed to set expectations. (2) The Hormuz shock is also a reminder of the economic value of domestic crude: even 60 kbpd is about 22 million barrels a year, but Kenya’s consumption is of refined products and the crude would need refining or export, so import substitution is not automatic. (3) Delays push revenue later while capex is largely committed, which lowers NPV; the discount-rate bar in the tornado chart gives a sense of the scale, so timing risk matters alongside price risk.')
# ---------- 13 ----------
H(d,'13. Risk assessment (analytical framework)')
P(d,'The framework scores each major product from 1 (low risk) to 5 (high risk) on six components, using observed metrics where available and explicit judgement otherwise.')
T(d,['Component','Definition','Scale / rule','Weight'],[
 ['Demand volatility','Coefficient of variation of monthly demand, 2024–25','5% → 1; 12% → 5 (linear)','15%'],
 ['Forecast uncertainty','Best out-of-sample sMAPE from the tournament','2% → 1; 6% → 5','10%'],
 ['Stock cover','Lowest reported days of cover, Apr 2026','30 days → 1; 10 days → 5; LPG (not reported) → 4','25%'],
 ['Price shock','Pump-price rise Mar→Sep 2026','0% → 1; 30% → 5; unobserved → 3','20%'],
 ['Infrastructure gap','PDP assessment of storage adequacy','Adequate → 1; gap → 4','15%'],
 ['Supply concentration','Reliance on Gulf-origin G-to-G supply (judgement)','Jet 3; others 4','15%']],widths=[3.4,6,5.3,1.6])
R=pd.read_csv(C+'risk_scores.csv',index_col=0)
T(d,['Product','Volatility','Forecast unc.','Stock cover','Price shock','Infrastructure','Concentration','Score','Rating'],[[i]+[f"{R.loc[i,c]:.1f}" for c in ['Demand volatility','Forecast uncertainty','Stock cover','Price shock','Infrastructure gap','Supply concentration']]+[f"{R.loc[i,'Score (base weights)']:.2f}",R.loc[i,'Rating']] for i in R.index],widths=[2.6,1.7,1.9,1.8,1.8,2.2,2.4,1.4,1.6],
 note='Scores 1 (low) to 5 (high). Ratings: LOW < 2.4; MEDIUM 2.4–3.2; HIGH > 3.2. LPG stock cover (no published figure) scored 4 as a data-gap penalty; unobserved LPG and jet price shocks scored a neutral 3. Concentration and infrastructure scores are judgement based on the PDP and G-to-G sourcing. Not an official classification.')
P(d,'**Robustness.** With equal weights or stock-heavy weights the scores are: LPG 3.56 / 3.63; petrol 3.06 / 3.34; diesel 2.88 / 3.19; jet 1.98 / 1.79. LPG ranks highest and jet lowest in all three weightings; the petrol–diesel order is stable. Petrol’s base-weight score (3.19) sits on the MEDIUM/HIGH boundary and would be rated HIGH under stock-heavy weights. Kerosene (0.8% of demand) and fuel oil (label uncertain) are excluded.')
P(d,'**Product notes.** *LPG*: highest growth, no published stock cover, a storage gap from 2026 and a Gulf supply origin. *Petrol*: shortest cover among the large products (13–16 days in April) and the most seasonal demand. *Diesel*: biggest price shock (+30.8%) and the largest absolute shortfall in litres, but lower demand volatility. *Jet fuel*: highest days of cover; risk is mainly route concentration.')
# ---------- 14 ----------
H(d,'14. Structural change: energy transition and cooking fuels')
P(d,'Over a ten-year horizon, three structural shifts could change the shape of demand: electrification of transport, the clean-cooking transition, and efficiency/modal shifts. Reliable Kenyan projections of electric-vehicle uptake were not available to this analysis, so the arithmetic below is not a forecast: it shows the import saving associated with each level of petrol displacement in 2035.')
ev=pd.read_csv(C+'ev_displacement.csv')
T(d,['Petrol demand displaced in 2035','Volume (kt)','Volume (ML)','Import saving (US$ m a year)','(KSh bn a year)'],[[f"{r._1:.0f}%",f"{r.kt:,.0f}",f"{r.ML:,.0f}",f"{r.import_saving_USDm_at_Aug26_landed:,.0f}",f"{r.KShbn:.1f}"] for r in ev.itertuples()],widths=[4.2,2.4,2.4,4.4,3],note='Baseline 2035 petrol demand 2,137 kt; saving valued at August 2026 landed cost (US$874/m³), 129.2 KSh per US$. Net saving would be lower after the extra electricity generation and imported vehicles.')
P(d,'Each 5% of petrol displaced saves about US$130 million (KSh 17 billion) a year in imports at 2026 prices, small relative to the whole bill but material at the margin for the shilling. The scenario analysis already allows petrol growth to fade after 2029, which is consistent with moderate displacement. The main structural change is on the LPG side: the PDP baseline already has LPG growing 7.3% a year; the observed 14.7% in 2025 suggests this could be exceeded, which would worsen the storage gap in Section 11.')
# ---------- 15 ----------
H(d,'15. Stress test: a repeat supply shock')
P(d,'To show what the relationships estimated above imply for a second shock, the following calculation applies the 2026 petrol relationships to a further 20% rise in landed cost from the August 2026 level (US$874 to US$1,049 per m³):')
dl=(874.26*0.2)/1000*129.2
T(d,['Step','Value'],[['Landed-cost rise','US$175/m³ = KSh '+f'{dl:.1f}'+' per litre at 129.2 KSh/US$'],['VAT-inclusive','KSh '+f'{dl*1.16:.1f}'+' per litre'],['Pass-through at 82%','KSh '+f'{dl*1.16*0.82:.1f}'+' per litre, or +'+f'{dl*1.16*0.82/214.03*100:.1f}'+'% on the KSh 214.03 pump price'],['Support required to hold the pump price flat','KSh '+f'{dl*1.16*0.82:.1f}'+' per litre × 2,346 ML = KSh '+f'{dl*1.16*0.82*2346/1000:.0f}'+' bn a year (petrol only)'],['Short-run demand response (ε −0.096)','−'+f'{0.096*dl*1.16*0.82/214.03*100:.2f}'+'% petrol volume'],['Cover if one cargo-month is lost','petrol: 16 days (April reported figure) → shortfall equal to about 14 days of demand']],widths=[5.5,11],note='Illustrative: assumes the same pass-through as Feb–Aug 2026, constant volumes, and no change in the exchange rate.')
P(d,'Three conclusions follow. First, the demand response is negligible in the short run: a further 20% landed-cost rise reduces petrol volume by only about 1%; the adjustment is therefore entirely by price, subsidy, or rationing. Second, holding pump prices flat would cost on the order of KSh 50 billion a year for petrol alone, before diesel; stabilisation is a material fiscal exposure. Third, the supply buffer matters more than the demand response: with 13–16 days of cover, a delay of two cargo cycles can empty the system, which is what the April experience showed.')
# ---------- 16 ----------
H(d,'16. Monitoring framework and early-warning indicators')
P(d,'The analysis suggests a short list of indicators that an analyst unit could update monthly. Thresholds are the author’s proposals and have no official status.')
T(d,['Indicator','Definition','Proposed trigger','Source / frequency'],[
 ['Stock cover by product','Days of average daily demand held in stock (petrol, diesel, jet, kerosene, LPG)','Amber < 30 days; red < 15 days','EPRA/KPC, daily or weekly'],
 ['Demand versus forecast band','Actual monthly demand against the 80%/95% prediction intervals','Alert when below the 80% lower bound two months running','KNBS LEI, monthly'],
 ['Landed cost','EPRA average landed cost, US$/m³ by product','Alert on +15% in a month or +30% in a quarter','EPRA, monthly'],
 ['Pass-through ratio','Pump-price change ÷ VAT-inclusive landed-cost change (KSh/L)','Alert below 0.7 (rising support cost)','Derived, monthly'],
 ['Stabilisation cost','KSh per litre support × volume','Alert above KSh 5 bn a month','Treasury/EPRA, monthly'],
 ['LPG storage headroom','Installed capacity − required storage','Alert below 2 kt','EPRA, quarterly'],
 ['Source concentration','Share of monthly imports from the largest origin region','Alert above 70%','KRA/EPRA, monthly'],
 ['Pipeline utilisation','KPC throughput ÷ nameplate on Lines 1, 2, 3','Alert above 95%','KPC, monthly'],
 ['Brent and USD/KES','Monthly average; 3-month change','Alert on Brent +20% or KES −3% in a quarter','Market data, daily'],
 ['Data integrity','Reconciliation of LEI product columns to annual survey','Alert on a difference above 3%','KNBS/EPRA, annually']],widths=[3.3,5.6,4.0,3.8])
P(d,'The first two indicators would have given a warning in March 2026: a stock-cover indicator showing under 20 days for petrol and diesel, and a landed-cost jump of more than 30% in a quarter.')
d.add_page_break()
# ---------- 17 ----------
H(d,'17. Key findings')
B(d,['Demand grew 12% in 2025 to 5.71 Mt; transport fuels are 71% of it. The dataset’s own labels mis-assign petrol, LPG and two other columns.',
 'Statistical forecasting is reliable to roughly 12 months; the no-shock counterfactual is 6.4 Mt for March 2026–February 2027 (80% interval 6.0–6.7 Mt). The official PDP baseline underestimated 2025 demand by 5.3%.',
 'Short-run demand response to price is small (diesel −0.19, petrol −0.10); the 2026 shock hit supply security and prices before volumes.',
 'Pass-through of the 2026 landed-cost shock to the pump was about 82% in shilling terms for petrol, cushioned by stabilisation support; the landed-cost shock added about US$0.7 bn a year to the petrol bill at constant volumes.',
 'Tank space is ample (73–96 days of gross capacity); stocks held were 13–28 days. Thirty days of petrol and diesel would cost about US$390 million to hold; 90 days, US$1.2 billion.',
 'LPG storage is short from 2026 in the baseline and the shortfall grows to about 11 kt by 2029 and 14 kt by 2030.',
 'Underlying growth, not the 2026 shock, is the largest uncertainty in the 2035 demand outlook (+17.5% / −7.8% for +2 / −1 points of growth).',
 'South Lokichar economics depend on the oil price and on fiscal terms that are not public: 30% chance of negative project value; the contractor break-even is US$73–82.'])
# ---------- 18 ----------
H(d,'18. Policy considerations and implementation priorities')
T(d,['Priority','Action','Rationale','Indicative cost / scale','Timing'],[
 ['1','Publish a daily stock-cover indicator by product, audited and owned by one agency','Public confusion in April (13–28 days for petrol) damaged credibility','Low (data and reporting)','Immediate'],
 ['2','Fund and legislate the strategic reserve, with release triggers set in advance and a gradual, rules-based build','Gross tank capacity exists; inventory does not','15 days of petrol + diesel ≈ US$196 m (KSh 25 bn) inventory; ≈ KSh 2.5 bn a year to finance at 10%','6–24 months'],
 ['3','Fast-track LPG storage (Lake Gas commissioning, KPRL PPP, Nairobi rail-linked storage)','Baseline shortfall from 2026; ≈ 14 kt by 2030','Capacity additions of 10–30 kt (PDP projects)','Now–2028'],
 ['4','Diversify supply sources within the G-to-G framework; contingency tenders','Gulf concentration exposed the system','Procurement design','6–12 months'],
 ['5','Set rules for stabilisation support (trigger, size, duration, exit)','Pass-through is partly determined by fiscal support; a repeat shock could cost around KSh 50 bn a year for petrol alone','Fiscal contingency','Before next shock'],
 ['6','Update PDP demand base and add a shock scenario','2025 demand was 5.3% above the PDP baseline','Analytical','Next PDP update'],
 ['7','Build a product-level supply–demand balance (opening stock, imports, consumption, exports, closing stock) from administrative data','Could not be constructed here; core of monitoring','Data sharing between EPRA, KRA, KPC','12 months'],
 ['8','Clarify upstream fiscal terms and test them against price scenarios','Developer break-even US$73–82 vs 60 for the project','Policy/analytical','Before first oil']],widths=[1.3,5.0,4.3,3.9,2.0],size=8)
# ---------- 19 ----------
H(d,'19. Limitations')
B(d,['Only 26 monthly observations (two seasonal cycles). Seasonal indices, model selection and prediction intervals are approximate. March 2026 and later volumes are missing.',
 'Two product columns (jet fuel*, fuel oil/other*) are identified by magnitude matching only; their growth rates (−4.2%, +65%) should not be used for decisions until confirmed with KNBS.',
 'No monthly GDP, CPI, Brent or exchange-rate series was available; the pass-through and driver analyses are limited to two-point and qualitative treatments.',
 'The town-level pump-price file was empty. 2026 prices and stock-cover figures come from press reports of official statements, not primary EPRA or ministry documents; several were contested.',
 'Own elasticity estimates failed (wrong sign); scenario elasticities come from the PDP equations and, for LPG, kerosene and jet, are assumptions.',
 'The South Lokichar model uses assumed costs and fiscal terms. It must not be read as official project economics. The Monte Carlo distributions are the author’s assumptions.',
 'Inventory cost, import-bill and stress-test figures are illustrative arithmetic on stated assumptions, not budget estimates.',
 'An interactive HTML dashboard accompanies this report. No Streamlit application or SQL warehouse has been built. The Excel model reproduces the scenario, supply-security and project-economics logic.'])
# ---------- 20 ----------
H(d,'20. Coverage of the original project brief')
T(d,['Brief module','Delivered','Where','Note'],[
 ['1 Demand intelligence','Yes','§4, Annex A','Product profiles, seasonality, YoY, shares, volatility, trends; drivers qualitative'],
 ['2 Demand forecasting (tournament)','Partly','§8, Annex C','Eight models; SARIMA/ARIMAX/Holt-Winters infeasible with 26 points; 80/95% intervals'],
 ['3 Scenario analysis','Yes','§9, Excel','Three scenarios to 2035 and sensitivities'],
 ['4 Price economics','Partly','§5','Nominal only (no CPI); regional spreads from press'],
 ['5 Elasticity','Partly','§7','Own estimate failed; PDP-implied used'],
 ['6 Cross-price / substitution','Yes (descriptive)','§4.5','LPG–kerosene–charcoal'],
 ['7 Supply security; balance sheet','Partly','§10','Stock-cover and capacity done; product balance sheet not feasible'],
 ['8 Import dependence','Yes (structural)','§6','Import bill illustration; imports vs demand gap flagged'],
 ['9 Oil-price pass-through','Partly','§5.4','Two-point; no monthly Brent/FX'],
 ['10 Market outlook report','Yes','This report','Plus 2-page executive brief'],
 ['11 Infrastructure','Yes','§11','White fuels adequate; LPG gap'],
 ['12 Project economics','Yes','§12','Public-assumption model, Monte Carlo, fiscal cases'],
 ['13 Risk engine','Yes','§13','Transparent scoring; weight sensitivity'],
 ['Excel model','Yes','Excel file','Live formulas; verified against Python'],
 ['Data dictionary, data quality, source reconciliation','Yes','Repository; §3','Includes label-error finding'],
 ['Interactive dashboard (HTML)','Yes','—','Delivered separately; Streamlit and SQL not built']],widths=[4.3,2.0,2.4,8],size=8)
# ---------- glossary ----------
H(d,'Glossary')
T(d,['Term','Meaning'],[
 ['AGO','Automotive gas oil (diesel)'],['PMS','Premium motor spirit (petrol)'],['IK','Illuminating kerosene'],['LPG','Liquefied petroleum gas'],['kt; Mt','Thousand tonnes; million tonnes'],['ML','Million litres'],['PDP','EPRA Petroleum Development Plan 2025–2029'],['EPRA','Energy and Petroleum Regulatory Authority'],['KNBS; LEI','Kenya National Bureau of Statistics; Leading Economic Indicators'],['KPC; KPRL; KOT2','Kenya Pipeline Company; Kenya Petroleum Refineries Ltd; Kipevu Oil Terminal 2'],['G-to-G','Government-to-government fuel supply arrangement'],['OMC','Oil marketing company'],['sMAPE; MASE','Symmetric mean absolute percentage error; mean absolute scaled error'],['NPV10; IRR','Net present value at a 10% discount rate; internal rate of return'],['Prediction interval','Range expected to contain a future observation with the stated probability'],['Pass-through','Share of an input-cost change that appears in the pump price']],widths=[3.5,13])
# ---------- annexes ----------
d.add_page_break()
H(d,'Annex A. Monthly consumption data (relabelled, kt)')
cols=['Diesel (AGO)','Petrol (PMS)','LPG','Jet fuel*','Fuel oil/other*','Kerosene (IK)','Total']
Wn=W.dropna()
T(d,['Month']+['Diesel','Petrol','LPG','Jet*','Fuel oil*','Kerosene','Total'],[[i.strftime('%b-%y')]+[f"{Wn.loc[i,c]:,.1f}" for c in cols] for i in Wn.index],widths=[2.0,2.2,2.2,2.0,2.0,2.2,2.2,2.2],size=8,note='Avgas (≈0.1 kt a month) is included in the total. March 2026 is blank in the source.')
H(d,'Annex B. Year-on-year growth by month (%)')
yy=pd.read_csv(C+'monthly_yoy_table.csv',index_col=0,parse_dates=True).dropna(how='all').iloc[12:]
T(d,['Month']+['Diesel','Petrol','LPG','Jet*','Fuel oil*','Kerosene','Total'],[[i.strftime('%b-%y')]+[f"{yy.loc[i,c]:+.1f}" for c in cols] for i in yy.index],widths=[2.0,2.2,2.2,2.0,2.0,2.2,2.2,2.2],size=8)
H(d,'Annex C. Forecast tournament: all metrics')
tt2=tt.copy()
T(d,['Series','Model','MAE','RMSE','MAPE','sMAPE','MASE'],[[r.series,r.model,f"{r.MAE:.1f}",f"{r.RMSE:.1f}",f"{r.MAPE:.2f}",f"{r.sMAPE:.2f}",f"{r.MASE:.2f}"] for r in tt2.itertuples()],widths=[3,5.2,1.7,1.7,1.7,1.7,1.7],size=7.5,note='MAE and RMSE in kt; MAPE and sMAPE in %. Rolling origins 18–25, horizons 1–6.')
H(d,'Annex D. Assumptions register (summary)')
T(d,['Assumption','Value','Basis'],[['Growth 2025–29','PDP baseline / optimistic / pessimistic by product','EPRA PDP'],['Growth 2030–35','0.8 × 2025–29 rate','Author'],['2026 price rise','Diesel 10/20/30%, petrol 8/15/22%, LPG 5/10/20%, kerosene 10/20/30%','Author, informed by EPRA reviews'],['Elasticities','Diesel −0.185/−0.57; petrol −0.096/−0.26; LPG −0.15/−0.30; kerosene −0.2/−0.5; jet 0','PDP-implied; author'],['Exchange rate','129.2 KSh per US$ (125–135 tested)','Author'],['Stock standard','30 days (15 + 15)','EPRA PDP'],['Litres per tonne','Implied by PDP base year','EPRA PDP'],['Risk weights','25/20/15/15/15/10%','Author'],['Lokichar inputs','See §12','Author; headline facts from press'],['Cooking-fuel efficiencies','LPG 45–55%; charcoal 20–30%; 46 and 29 MJ/kg','Author illustration']],widths=[3.6,8.8,4.3])
H(d,'Annex E. Sources')
B(d,['EPRA, Petroleum Development Plan for the Medium-Term Period 2025–2029 (June 2025): demand equations, scenario growth rates, 2024 actuals, storage capacity, LPG supply-demand balance.',
 'KNBS, Economic Survey 2026, as reported by The Standard, The Star, Business Daily and The Kenya Times (2025 demand 5.7 Mt; diesel 2.4 Mt; LPG 475.9 kt; imports 5.5 Mt).',
 'LeadAfrik Data (CC BY 4.0): monthly consumption of petroleum fuels; national average retail prices (source: KNBS LEIs).',
 'EPRA monthly price reviews, May–September 2026, as reported by Citizen Digital, Kenyans.co.ke, K24, Business Daily, People Daily.',
 'Stock cover and shortage reports: The Standard (2 and 8 April 2026), People Daily and The Star (8 April), Citizen Digital (21 May).',
 'Oil market: Reuters poll (31 March 2026), Bloomberg (9 April), Khaleej Times (late August), ANZ via Engine (8 September).',
 'South Lokichar: Bloomberg/World Oil (11 November 2025), OilPrice, Serrari Group, Business Today.'])
d.save('out/Kenya_Petroleum_Market_Outlook_2026-2035.docx')
