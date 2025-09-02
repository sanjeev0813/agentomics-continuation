import os, requests
_s = requests.Session()

def llm_should_hire(model: str, firm_cash: float, wage_offer: float, seeker_skill: float, vacancies: int, unemp: float | None = None):
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1")
    sys = "Answer YES or NO only."
    usr = (
        f"Firm cash: {firm_cash}\n"
        f"Wage offer: {wage_offer}\n"
        f"Vacancies: {vacancies}\n"
        f"Candidate skill: {seeker_skill}\n"
        f"Unemployment rate: {'' if unemp is None else unemp}\n"
        f"Decision: Hire this candidate now? YES or NO"
    )
    data = {"model": model, "messages": [{"role": "system", "content": sys}, {"role": "user", "content": usr}], "stream": False, "options": {"temperature": 0}}
    try:
        r = _s.post(host + "/api/chat", json=data, timeout=(0.25, 0.75))
        r.raise_for_status()
        j = r.json()
        txt = (j.get("message", {}).get("content") or j.get("response") or "").strip().upper()
        if txt.startswith("Y"):
            return True
        if txt.startswith("N"):
            return False
        return None
    except Exception:
        return None
