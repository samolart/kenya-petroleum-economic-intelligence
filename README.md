# Kenya Petroleum Economic Intelligence & Forecasting System (portfolio build)

An evidence-based analysis of Kenya's petroleum demand, prices, supply security, infrastructure and upstream project economics, 2026-2035.

**Deliverables**
- **[Read the Final Report: Kenya Petroleum Market Outlook 2026–2035](https://github.com/samolart/kenya-petroleum-economic-intelligence/blob/main/Kenya_Petroleum_Market_Outlook_2026-2035.pdf)**
- **[Methods & Technical Documentation: Every Step, Tool, and Line of Code](https://github.com/samolart/kenya-petroleum-economic-intelligence/blob/main/Kenya_Petroleum_Methods_and_Code_Report.pdf)**
- **[Read the Executive Brief](https://github.com/samolart/kenya-petroleum-economic-intelligence/blob/main/Kenya_Petroleum_Executive_Brief.pdf)**
- **[Explore the Live Formula Model (Interactive Excel)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fsamolart%2Fkenya-petroleum-economic-intelligence%2Frefs%2Fheads%2Fmain%2FKenya_Petroleum_Economic_Model.xlsx&wdOrigin=BROWSELINK)** | **[Download Excel File](https://github.com/samolart/kenya-petroleum-economic-intelligence/blob/main/Kenya_Petroleum_Economic_Model.xlsx)**
- `code/` - pipeline (01-07), `data/raw` (inputs as supplied), `data/clean` (all derived tables), `figures/`
- `DATA_DICTIONARY.md`, `DATA_QUALITY_REPORT.md`, `LIMITATIONS.md`

**Run:** `./run_all.sh` (Python 3.10+, pandas, numpy, scipy, matplotlib, python-docx).

**Headline data-quality finding:** the LeadAfrik monthly-consumption CSV has mislabelled product columns. The column labelled "LPG" is petrol and "Other" is LPG (exact match to EPRA PDP 2024 actuals; 2025 matches KNBS Economic Survey 2026). The project relabels them (see `code/common.py`).

**Dashboard:** `[View Live Dashboard](https://samolart.github.io/kenya-petroleum-economic-intelligence/#overview), a self-contained interactive page (open in any browser).

**Not built:** Streamlit app, SQL warehouse (see LIMITATIONS.md).

Source data licence: LeadAfrik Data, CC BY 4.0 (attribute LeadAfrik Data; underlying figures are KNBS/EPRA).
