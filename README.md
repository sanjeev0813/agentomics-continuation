## Agentomics Continuation

This project extends the Agentomics framework to simulate how micro-level household and firm decisions aggregate into macroeconomic outcomes, with optional policy/shock scenarios.

## Setup

- Python: 3.10+ (3.11/3.12 recommended)
- Install dependencies:
  1) cd agentomics-continuation-main
  2) pip install -r requirements.txt

## Run Options

- Baseline run (non-interactive; saves plots + summary):
  python -m agentomics.simulation

- Scenario menu (interactive; writes a scenario-specific report):
  python scenario_runner.py

Notes:
- Data samples live in ./data (UNRATE.csv, CPIAUCSL.csv) for simple validation/alignment utilities.
- Figures are saved to the project root as PNGs.

## Expected Output

- Reports
  - report.txt (baseline summary)
  - report_<scenario-name>.txt (e.g., report_high-interest_rate_shock.txt)

- Figures
  - report_unemployment.png
  - report_avg_wage.png
  - report_house_price.png
  - report_gini.png

- Console/Logs
  - Start banner with config (agents, steps, LLM ON/OFF)
  - Step progress and end-of-run summary

## LLM / Ollama (Optional)

- You do not need an Ollama server to run.
- If an Ollama server is available (default http://localhost:11434) and the `ollama` Python package is installed, some decisions may consult the LLM; otherwise the code automatically falls back to deterministic/heuristic logic.
- To point at a different host: set OLLAMA_HOST (e.g., export OLLAMA_HOST=http://127.0.0.1:11435).
- Default model when available: qwen2.5:7b-instruct.

## What to Look For

- Unemployment (report_unemployment.png): direction and persistence of labor-market slack/tightness.
- Average wage (report_avg_wage.png): labor-market tightness and firms’ pricing power.
- House price (report_house_price.png): conditions sensitive to credit/rates.
- Inequality (report_gini.png): distributional effects over time.
- Reports (report.txt / report_<scenario>.txt): final unemployment, savings, firm counts, market stats.

## What Conclusions We Can Draw and Why

- Household dynamics: shocks like higher interest rates or unemployment reduce hiring and dampen consumption; stimulus tends to raise savings/consumption.
- Firm behavior: under weak demand/tighter conditions, vacancies and wage growth fall; with supportive conditions, hiring and wages firm up.
- Macro outcomes: compare baseline vs. shocks to see contractionary (higher unemployment, softer prices) vs. expansionary (lower unemployment, firmer wages/prices) patterns.
- Justification: micro rules (and optional LLM heuristics) aggregate via labor/housing/financial markets to produce the observed macro time series; comparing scenarios reveals consistent causal directions.

## Troubleshooting

- Import errors: ensure you ran `pip install -r requirements.txt`.
- Plots not visible: figures are written as PNGs in the project root; open the files directly.
- LLM slow/unavailable: stop Ollama or set OLLAMA_HOST correctly; the simulation will proceed with deterministic rules.

## Quick Start Checklist

- [ ] pip install -r requirements.txt
- [ ] python -m agentomics.simulation  (baseline: saves report.txt + PNGs)
- [ ] OR python scenario_runner.py     (interactive scenarios: saves report_<...>.txt)
