# Kenya Petroleum Economic Intelligence & Forecasting System (portfolio build)

An evidence-based analysis of Kenya's petroleum demand, prices, supply security, infrastructure and upstream project economics, 2026-2035.

**Deliverables**
- `out/Kenya_Petroleum_Market_Outlook_2026-2035.docx` - the final report
- `out/Kenya_Petroleum_Methods_and_Code_Report.docx` - every step, tool and line of code
- `out/Kenya_Petroleum_Executive_Brief.docx` - 2-page brief
- `out/Kenya_Petroleum_Economic_Model.xlsx` - live-formula model
- `code/` - pipeline (01-07), `data/raw` (inputs as supplied), `data/clean` (all derived tables), `figures/`
- `DATA_DICTIONARY.md`, `DATA_QUALITY_REPORT.md`, `LIMITATIONS.md`

**Run:** `./run_all.sh` (Python 3.10+, pandas, numpy, scipy, matplotlib, python-docx).

**Headline data-quality finding:** the LeadAfrik monthly-consumption CSV has mislabelled product columns. The column labelled "LPG" is petrol and "Other" is LPG (exact match to EPRA PDP 2024 actuals; 2025 matches KNBS Economic Survey 2026). The project relabels them (see `code/common.py`).

**Dashboard:** `dashboard/Kenya_Petroleum_Dashboard.html`, a self-contained interactive page (open in any browser).

**Not built:** Streamlit app, SQL warehouse (see LIMITATIONS.md).

Source data licence: LeadAfrik Data, CC BY 4.0 (attribute LeadAfrik Data; underlying figures are KNBS/EPRA).
