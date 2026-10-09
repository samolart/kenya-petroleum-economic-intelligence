# Data quality report
**Consumption file (189 rows = 7 products x 27 months)**
- Structure: 189 data rows + 1 footer attribution line (removed). No duplicate (month, product) rows.
- Missing: March 2026 blank for all 7 products (7 values; flagged provisional). Analysis uses Jan 2024-Feb 2026 (26 months).
- Provisional: 21 rows (Jan-Mar 2026).
- **Mislabelled columns (critical):** exact reconciliation to EPRA PDP 2024 actuals: AGO 2,193.6 kt (exact); column "LPG" 1,472.7 = PDP petrol 1,472.7 (exact); "Other" 414.9 = PDP LPG 414.9 (exact); kerosene 37.1 (exact). 2025: diesel 2,419.1 = KNBS 2,419.1; relabelled LPG 476.0 vs KNBS 475.9; total 5,712 vs KNBS 5.7 Mt; diesel+petrol 71.4% = KNBS 71.4%.
- Unresolved: "Motor Spirit" (732 kt in 2024) vs PDP jet 765.1 (-4.3%) and "Jet Oil" (250 kt) vs PDP fuel oil 301.9 (-17.2%): probable but unconfirmed. 2024 total 5,102 kt vs KNBS ~5,200 kt (-1.9%), so 2025 growth is 12.0% here vs 9.9% in KNBS.
- Outliers: fuel oil/other* (CV 32%) and avgas are volatile; no values removed.
- Units: all thousand tonnes; conversions to litres use PDP-implied factors.
**Price file (75 rows = 5 series x 15 months)** - complete; 8 distinct petrol and 7 distinct diesel price levels (administered steps); footer line removed. Different basis (national average) from Nairobi maxima.
**Town pump-price file** - empty (header only). Not used.
**Secondary sources** - 2026 prices, landed costs and stock-cover figures come from press reports of official statements; the stock figures conflict (petrol 13-28 days). Import-bill figures for 2025 conflict (KSh 511-529 bn) and are not used.
**Not obtained:** monthly Brent, USD/KES, GDP, CPI; PDP storage Tables 5.8-5.14; Economic Survey tables.
