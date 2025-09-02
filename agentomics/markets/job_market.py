from typing import Callable, List, Tuple, Dict
from ..llm.ollama_client import llm_should_hire

class JobMarket:
    def __init__(self, get_household: Callable, get_firm: Callable):
        self.get_household = get_household
        self.get_firm = get_firm
        self.seekers: List[Tuple[int, float]] = []
        self.firm_slots: Dict[int, int] = {}
        self.firm_wages: Dict[int, float] = {}
        self.last_avg_wage: float = 20.0
        self.last_unemp: float | None = None
        self.max_slots_per_firm: int = 3
        self.max_llm_calls_per_step: int = 40
        self._llm_calls_left: int = 0
        self._llm_cache: Dict[Tuple, bool | None] = {}

    def collect_vacancies(self, firm_ids: List[int]) -> float:
        self.firm_slots.clear()
        self.firm_wages.clear()
        self._llm_calls_left = self.max_llm_calls_per_step
        self._llm_cache.clear()
        wages = []
        for fid in firm_ids:
            f = self.get_firm(fid)
            if f is None:
                continue
            w = getattr(f, "wage_offer", self.last_avg_wage)
            try:
                w = float(w)
            except Exception:
                w = self.last_avg_wage
            cash = getattr(f, "cash", 0.0)
            try:
                cash = float(cash)
            except Exception:
                cash = 0.0
            slots_attr = getattr(f, "vacancies", None)
            try:
                slots_attr = int(slots_attr) if slots_attr is not None else None
            except Exception:
                slots_attr = None
            slots = 0
            if slots_attr is not None and slots_attr > 0:
                slots = slots_attr
            else:
                if w > 0.0 and cash >= w:
                    afford = int(cash // w)
                    if afford <= 0:
                        afford = 1
                    slots = min(afford, self.max_slots_per_firm)
            if slots > 0:
                self.firm_slots[fid] = int(slots)
                self.firm_wages[fid] = float(w)
                wages.append(w)
        if wages:
            self.last_avg_wage = sum(wages) / len(wages)
        return self.last_avg_wage

    def avg_posted_wage(self) -> float:
        return self.last_avg_wage

    def register_seeker(self, household_id: int, skill: float):
        t = (household_id, float(skill))
        if t not in self.seekers:
            self.seekers.append(t)

    def set_last_unemp(self, unemp: float):
        self.last_unemp = float(unemp)

    def _llm_decide(self, fid: int, w: float, vac: int, cash: float, skill: float, model: str) -> bool:
        key = (fid, round(w, 2), min(vac, 3), round(cash, -2) if cash > 0 else 0.0, round(skill, 1), round(self.last_unemp, 1) if self.last_unemp is not None else None, model)
        if key in self._llm_cache:
            res = self._llm_cache[key]
            if res is None:
                return cash >= w and vac > 0
            return bool(res)
        if self._llm_calls_left <= 0:
            self._llm_cache[key] = None
            return cash >= w and vac > 0
        self._llm_calls_left -= 1
        res = llm_should_hire(model=model, firm_cash=cash, wage_offer=w, seeker_skill=skill, vacancies=vac, unemp=self.last_unemp)
        self._llm_cache[key] = res
        if res is None:
            return cash >= w and vac > 0
        return bool(res)

    def match(self) -> int:
        if not self.seekers or not self.firm_slots:
            self.seekers.clear()
            return 0
        self.seekers.sort(key=lambda x: x[1], reverse=True)
        hires = 0
        while self.seekers and self.firm_slots:
            hid, skill = self.seekers.pop(0)
            ordered = sorted(self.firm_slots.keys(), key=lambda fid: self.firm_wages.get(fid, self.last_avg_wage), reverse=True)
            hired_flag = False
            for fid in ordered:
                if fid not in self.firm_slots or self.firm_slots[fid] <= 0:
                    continue
                f = self.get_firm(fid)
                if f is None:
                    continue
                w = float(self.firm_wages.get(fid, self.last_avg_wage))
                vac = int(self.firm_slots.get(fid, 0))
                cash = float(getattr(f, "cash", 0.0) or 0.0)
                model = getattr(f, "llm_model", "qwen2.5:7b-instruct")
                approve = self._llm_decide(fid=fid, w=w, vac=vac, cash=cash, skill=float(skill), model=model)
                if not approve:
                    continue
                hired = False
                hire_fn = getattr(f, "hire", None)
                if callable(hire_fn):
                    try:
                        hired = bool(hire_fn(hid, skill, self))
                    except Exception:
                        hired = False
                if not hired and cash >= w and vac > 0:
                    try:
                        f.cash = float(cash) - w
                    except Exception:
                        pass
                    try:
                        if hasattr(f, "vacancies"):
                            f.vacancies = int(getattr(f, "vacancies", 0)) - 1
                    except Exception:
                        pass
                    firm_id = getattr(f, "id", getattr(f, "fid", fid))
                    self.notify_hire(hid, firm_id, w)
                    hired = True
                if hired:
                    hires += 1
                    self.firm_slots[fid] -= 1
                    if self.firm_slots[fid] <= 0:
                        del self.firm_slots[fid]
                    hired_flag = True
                    break
            if not hired_flag:
                pass
        self.seekers.clear()
        return hires

    def notify_hire(self, seeker_id: int, firm_id: int, wage: float):
        hh = self.get_household(seeker_id)
        if hh is not None:
            try:
                hh.accept_offer(firm_id, float(wage))
            except Exception:
                pass
