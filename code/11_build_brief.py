from docx_helpers import *
from docx.shared import Cm
d=new_doc()
for sec in d.sections: sec.top_margin=Cm(1.5); sec.bottom_margin=Cm(1.5)
d.styles['Normal'].font.size=Pt(10)
P(d,'KENYA PETROLEUM MARKET',bold=True,size=22).runs[0].font.color.rgb=NAVY
P(d,'Executive Intelligence Brief  |  October 2026',bold=True,size=12)
P(d,'For policymakers. Full analysis, sources and caveats: Kenya Petroleum Market Outlook 2026–2035.',italic=True,size=9)
H(d,'Where the market stands',2)
B(d,['**Demand accelerated into 2026.** 2025 consumption rose 12.0% to 5.71 Mt (KNBS: 5.7 Mt). Diesel and petrol are 71.4% of demand; LPG grew 14.7%. January–February 2026 was still +7.1%.',
 '**Then the Gulf war hit.** From 28 February, landed costs rose about 50%; diesel at the Nairobi pump went from KSh 166.54 to KSh 242.92 by May and sat at KSh 217.86 in September. Pump queues followed in April.',
 '**Tanks were not the problem; stocks were.** Gross licensed capacity covers 73–96 days of demand, but reported stocks were 13–28 days against a 30-day standard. A 30-day cushion of petrol and diesel costs about US$390 m (KSh 51 bn) to hold at today’s prices.',
 '**LPG is the one real infrastructure gap.** Required storage exceeds installed capacity from 2026 and the shortfall reaches about 11 kt by 2029.',
 '**Prices passed through most of the shock.** About 82% of petrol’s VAT-inclusive landed-cost increase reached the pump; support covered the rest.'])
H(d,'Outlook',2)
T(d,['','2025','2026','2030','2035'],[['Low-demand (Mt)','5.71','5.72','5.99','6.64'],['Baseline (Mt)','5.71','5.80','6.31','7.16'],['High-demand (Mt)','5.71','5.90','6.70','7.85']],widths=[4.5,2.5,2.5,2.5,2.5],note='Scenario projections (PDP growth rates, 2026 price shock via elasticities, assumed fade after 2029). The statistical no-shock forecast for Mar-2026–Feb-2027 is 6.37 Mt (80% interval 6.04–6.69 Mt).')
d.add_picture('figures/f6_scenarios.png',width=Cm(11)); d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
P(d,'Underlying growth is the biggest uncertainty: +2 points a year raises 2035 demand 17.5%; −1 point lowers it 7.8%. The official plan’s 2025 baseline was 5.3% below actual.',size=9.5)
d.add_page_break()
H(d,'What to do',2)
T(d,['Priority','Action','Scale'],[['1','Publish one audited daily stock-cover indicator by product','Low cost; immediate'],['2','Fund and legislate the strategic reserve with pre-set release rules; build gradually','15 days of petrol + diesel ≈ US$196 m inventory; ≈ KSh 2.5 bn a year to finance'],['3','Fast-track LPG storage (Lake Gas, KPRL PPP, Nairobi rail-linked)','10–30 kt of additions; baseline gap ≈ 14 kt by 2030'],['4','Diversify supply origins within the G-to-G framework','Procurement design'],['5','Set rules for stabilisation support (trigger, size, exit)','A repeat 20% landed-cost rise ≈ KSh 50 bn a year for petrol alone']],widths=[1.6,8.2,6.8])
H(d,'Upstream: South Lokichar (illustrative)',2)
P(d,'Public-information model with the author’s assumptions (60 kbpd plateau, US$6 bn capex, US$70 Brent): project NPV10 about US$1.6 bn, IRR 15%, break-even US$60/bbl. Monte Carlo: 30% chance of negative project NPV. Under assumed fiscal terms the developer needs US$73–82 Brent to break even, so fiscal terms matter. **Not official project economics.**')
H(d,'Risk ranking (analytical framework, not official)',2)
T(d,['LPG','Petrol','Diesel','Jet fuel'],[['HIGH','MEDIUM','MEDIUM','LOW']],widths=[4,4,4,4])
H(d,'Watch list',2)
B(d,['Stock cover by product against 30 days','March–December 2026 volumes against the forecast bands','Landed cost and the pass-through ratio','LPG storage commissioning','Share of imports from a single region','Brent and the shilling'])
H(d,'Data caveats',2)
P(d,'The main consumption dataset mislabels petrol as “LPG” and LPG as “Other” (reconciled to EPRA and KNBS). Volume data end in February 2026, so the shock’s effect on volumes is not yet observed. 2026 prices and stock figures come from press reports of official statements and were partly contested.',size=9.5)
d.save('out/Kenya_Petroleum_Executive_Brief.docx')
