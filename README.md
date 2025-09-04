# Agentomics Continuation — README

# WHAT TO SET UP AND RUN
# • Python: 3.10+ (3.11/3.12 recommended).
# • Project root after unzip: agentomics-continuation-main/
# • Install dependencies:
#     cd agentomics-continuation-main
#     pip install -r requirements.txt
#   NOTE: The code imports `requests` in the LLM helper; if you get
#   “ModuleNotFoundError: requests”, run:  pip install requests
#
# RUN OPTIONS
# • Interactive scenarios (menu + optional quiz):
#     python scenario_runner.py
#   This writes a scenario-specific text report like:
#     report_<scenario-name>.txt  (e.g., report_high-interest_rate_shock.txt)
#
# • One-shot baseline run (no prompts, saves plots + report):
#     python -m agentomics.simulation
#   This prints a start/finish summary and saves figures to the project root.

# LLM / OLLAMA (OPTIONAL)
# • You do NOT need an Ollama server to run the simulation.
# • If an Ollama server is available (default http://127.0.0.1:11434)
#   and the `ollama` Python package is installed, some hiring decisions
#   will consult the LLM briefly; otherwise the code automatically falls
#   back to rule-based behavior.
# • Default model used when available: "qwen2.5:7b-instruct".
# • To point at a non-default host, set:
#     export OLLAMA_HOST="http://<host>:<port>"
# • If the server is unreachable, calls time out quickly and the code
#   proceeds with deterministic rules.

# WHAT WE EXPECT TO SEE
# • Saved to the project root after a successful run:
#   - report.txt                               → Baseline simulation summary.
#   - report_unemployment.png                  → Unemployment over time.
#   - report_avg_wage.png                      → Average wage over time.
#   - report_house_price.png                   → Average house price over time.
#   - report_gini.png                          → Inequality (Gini) over time.
#   - report_<scenario-name>.txt               → For interactive scenarios.
# • Console/log output includes:
#   - Start banner with config (households, firms, steps, LLM ON/OFF).
#   - Step progress and end-of-run summary lines.

# WHAT CONCLUSIONS WE CAN DRAW AND WHY
# • Household dynamics:
#   Rising interest rates or adverse shocks typically reduce hiring and
#   dampen consumption; stimulus payments tend to raise savings/consumption.
# • Firm behavior:
#   Under weak demand or tighter conditions, firms post fewer vacancies,
#   restrain wages, and adjust prices downward; in supportive conditions,
#   hiring/wages generally firm up.
# • Macro outcomes (read the figures together):
#   - Unemployment (report_unemployment.png): contractionary scenarios show
#     higher/lazier declines; expansionary scenarios trend lower.
#   - Average wage (report_avg_wage.png): proxy for labor-market tightness.
#   - House price (report_house_price.png): sensitive to rates/credit; often
#     softer under higher rates, firmer with stimulus/demand.
#   - Gini (report_gini.png): distributional effects; stress periods can widen
#     inequality if job/income losses are uneven.
# • Why these conclusions hold here:
#   Micro-to-macro aggregation: households and firms follow explicit rules
#   (and optionally LLM-guided heuristics) in job/housing/financial markets.
#   Their local interactions generate the observed macro time series, letting
#   you compare baseline vs. shocks to see consistent causal patterns.

# TROUBLESHOOTING
# • If imports fail: ensure `pip install -r requirements.txt` and install
#   `requests` if missing.
# • If no plot windows appear: figures are saved as PNGs in the project root.
# • If LLM calls seem slow: either stop the Ollama server (fallback engages)
#   or install/point OLLAMA_HOST correctly; timeouts are short by design.

# QUICK START CHECKLIST
# [ ] pip install -r requirements.txt
# [ ] (if needed) pip install requests
# [ ] python -m agentomics.simulation   # baseline run, saves PNGs + report.txt
# [ ] OR python scenario_runner.py      # choose a scenario and get report_<...>.txt
