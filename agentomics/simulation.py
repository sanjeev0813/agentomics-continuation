from __future__ import annotations

import sys
import random
from dataclasses import dataclass
from typing import Dict, List

SEP_RATE = 0.02

try:
    import ollama
    HAVE_OLLAMA = True
except Exception:
    ollama = None
    HAVE_OLLAMA = False

from agentomics.agents.household import HouseholdAgent
from agentomics.agents.firm import FirmAgent
from agentomics.markets.job_market import JobMarket
from agentomics.markets.housing_market import HousingMarket
from agentomics.data_loader import get_real_data
from agentomics.validation import validate_unemployment, validate_cpi


@dataclass
class SimConfig:
    num_households: int = 300
    num_firms: int = 20
    num_steps: int = 120
    seed: int = 42
    use_llm: bool = True
    llm_model: str = "qwen2.5:7b-instruct"
    llm_temperature: float = 0.2
    decision_interval: int = 3
    max_llm_households_per_step: int = 20
    max_llm_firms_per_step: int = 5
    verbose: bool = True
    log_every: int = 1


def _log(msg: str):
    print(msg)
    sys.stdout.flush()


def build_households(n: int) -> Dict[int, HouseholdAgent]:
    import random as _r
    _r.seed(123)
    hh = {}
    for i in range(n):
        skill = 0.7 + 0.6 * _r.random()
        savings = 2000 + 10000 * _r.random()
        hh[i] = HouseholdAgent(id=i, skill=skill, savings=savings)
    return hh


def build_firms(n: int) -> Dict[int, FirmAgent]:
    import random as _r
    _r.seed(456)
    fm = {}
    for j in range(n):
        price = 0.8 + 0.8 * _r.random()
        wage = 16.0 + 10.0 * _r.random()
        cash = 8000 + 20000 * _r.random()
        fm[j] = FirmAgent(id=j, price=price, wage_offer=wage, cash=cash)
    return fm


def run_simulation(cfg: SimConfig):
    households = build_households(cfg.num_households)
    firms = build_firms(cfg.num_firms)
    firm_ids = list(firms.keys())
    housing = HousingMarket()
    job_market = JobMarket(get_household=lambda hid: households.get(hid), get_firm=lambda fid: firms.get(fid))
    rng = random.Random(cfg.seed)

    llm_on = bool(cfg.use_llm and HAVE_OLLAMA)
    if llm_on:
        _log(f"LLM mode: ON; model={cfg.llm_model}")
        try:
            models = ollama.list().get("models", [])
            names = {m.get("model") or m.get("name") for m in models}
            if cfg.llm_model not in names:
                _log(f"[warn] Model '{cfg.llm_model}' not found locally. Run:  ollama pull {cfg.llm_model}")
        except Exception:
            pass
    else:
        _log("LLM mode: OFF")

    stats_unemp: List[float] = []
    stats_price: List[float] = []
    stats_avg_wage: List[float] = []
    real = get_real_data()

    for t in range(cfg.num_steps):
        if cfg.verbose and t % cfg.log_every == 0:
            _log(f"[tick {t+1}/{cfg.num_steps}] starting...")

        if llm_on:
            hh_ids = list(households.keys())
            fm_ids = list(firms.keys())
            llm_hh_step = set(rng.sample(hh_ids, min(cfg.max_llm_households_per_step, len(hh_ids))))
            llm_fm_step = set(rng.sample(fm_ids, min(cfg.max_llm_firms_per_step, len(fm_ids))))
        else:
            llm_hh_step = set()
            llm_fm_step = set()

        try:
            for h in households.values():
                if getattr(h, "employed", False) and rng.random() < SEP_RATE:
                    if hasattr(h, "lose_job"):
                        h.lose_job()
                    elif hasattr(h, "layoff"):
                        h.layoff()
                    elif hasattr(h, "become_unemployed"):
                        h.become_unemployed()
                    else:
                        if hasattr(h, "employer_id"):
                            h.employer_id = None
                        h.employed = False

            recent_demand_proxy = max(1.0, sum((max(0.0, f.inventory) for f in firms.values())) * 0.1)

            for fid, f in firms.items():
                f.forecast_and_set_vacancies(
                    recent_demand_proxy,
                    llm_on and fid in llm_fm_step,
                    t,
                    cfg.decision_interval,
                    cfg.llm_model,
                    cfg.llm_temperature,
                )

            job_market.collect_vacancies(firm_ids)
            market_wage = job_market.avg_posted_wage()

            for fid, f in firms.items():
                f.set_wage_and_price(
                    market_wage,
                    input_cost_index=1.0,
                    use_llm=llm_on and fid in llm_fm_step,
                    step=t,
                    decision_interval=cfg.decision_interval,
                    llm_model=cfg.llm_model,
                    llm_temperature=cfg.llm_temperature,
                )

            for hid, h in households.items():
                h.decide_labor(
                    job_market,
                    use_llm=llm_on and hid in llm_hh_step,
                    step=t,
                    decision_interval=cfg.decision_interval,
                    llm_model=cfg.llm_model,
                    llm_temperature=cfg.llm_temperature,
                )

            seekers_before = len(getattr(job_market, "seekers", []))
            employed_before = sum((1 for h in households.values() if h.employed))
            unemp_before = 1.0 - employed_before / max(1, len(households))
            if hasattr(job_market, "set_last_unemp"):
                job_market.set_last_unemp(unemp_before * 100.0)

            job_market.match()

            employed_after = sum((1 for h in households.values() if h.employed))
            hires = max(0, employed_after - employed_before)

            for hid, h in households.items():
                h.decide_housing(
                    housing,
                    use_llm=llm_on and hid in llm_hh_step,
                    step=t,
                    decision_interval=cfg.decision_interval,
                    llm_model=cfg.llm_model,
                    llm_temperature=cfg.llm_temperature,
                )

            total_consumption_demand = 0.0
            for h in households.values():
                total_consumption_demand += h.realize_income()

            demand_per_firm = max(1.0, total_consumption_demand / max(1, len(firms)))
            for f in firms.values():
                f.produce_and_sell(demand_per_firm)

            housing.adjust_prices()
            housing.replenish_stock()

            employed_count = employed_after
            unemp_rate = 1.0 - employed_count / max(1, len(households))
            stats_unemp.append(unemp_rate * 100.0)
            stats_price.append(housing.avg_price)
            stats_avg_wage.append(market_wage)

            if cfg.verbose and t % cfg.log_every == 0:
                _log(
                    f"Step {t+1:>3}/{cfg.num_steps}: seekers={seekers_before:>3} hires={hires:>3} "
                    f"unemp={stats_unemp[-1]:5.1f}% avg_wage={market_wage:6.2f} house_price={housing.avg_price:,.0f}"
                )
        except Exception as e:
            _log(f"[ERROR] at step {t}: {e}")
            raise

    if real["unemployment"]:
        metrics_u = validate_unemployment(stats_unemp, real["unemployment"])
        _log(f"Validation — Unemployment: {metrics_u}")
    if real["cpi"]:
        metrics_c = validate_cpi(stats_price, real["cpi"])
        _log(f"Validation — CPI proxy vs price level: {metrics_c}")

    return {
        "unemployment": stats_unemp,
        "house_price": stats_price,
        "avg_wage": stats_avg_wage,
        "llm_on": llm_on,
    }


def _make_plots(results):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4.5))
    plt.plot(results["unemployment"])
    plt.title("Unemployment Rate (%)")
    plt.xlabel("Step")
    plt.ylabel("Unemployment (%)")
    plt.tight_layout()
    plt.savefig("report_unemployment.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.plot(results["house_price"])
    plt.title("Average House Price (proxy)")
    plt.xlabel("Step")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig("report_house_price.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.plot(results["avg_wage"])
    plt.title("Market Wage (avg posted)")
    plt.xlabel("Step")
    plt.ylabel("Wage")
    plt.tight_layout()
    plt.savefig("report_avg_wage.png", dpi=150)
    plt.close()


def main():
    cfg = SimConfig(
        use_llm=True,
        llm_model="qwen2.5:7b-instruct",
        llm_temperature=0.2,
        decision_interval=3,
        max_llm_households_per_step=20,
        max_llm_firms_per_step=5,
        verbose=True,
        log_every=1,
    )
    _log(
        f"Starting simulation: H={cfg.num_households} F={cfg.num_firms} steps={cfg.num_steps} | "
        f"LLM={('ON' if cfg.use_llm and HAVE_OLLAMA else 'OFF')} (interval={cfg.decision_interval})"
    )
    results = run_simulation(cfg)
    _make_plots(results)
    _log(
        f"Done. Final unemployment: {results['unemployment'][-1]:.2f}% | "
        f"Final avg house price: {results['house_price'][-1]:,.0f} | "
        f"Saved plots: report_unemployment.png, report_house_price.png, report_avg_wage.png"
    )


if __name__ == "__main__":
    main()