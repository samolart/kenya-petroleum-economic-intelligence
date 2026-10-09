#!/usr/bin/env bash
# Reproduce every table and figure. Run from the project root. Python 3.10+, pandas, numpy, scipy, matplotlib, python-docx.
set -e
export PYTHONPATH=code
python3 code/01_prepare_data.py
python3 code/02_demand_analysis.py
python3 code/03_forecasting.py
python3 code/04_prices_elasticity.py
python3 code/05_scenarios_security_risk.py
python3 code/06_project_economics.py
python3 code/09_extended_analysis.py
python3 code/07_build_report1.py
python3 code/10_build_excel.py
python3 code/11_build_brief.py
python3 code/08_build_report2.py
