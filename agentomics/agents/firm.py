from __future__ import annotations
from dataclasses import dataclass
import math
import re
from concurrent .futures import ThreadPoolExecutor ,TimeoutError
try :
    import ollama
    HAVE_OLLAMA =True
except Exception :
    ollama =None
    HAVE_OLLAMA =False

def _llm_choose (context :str ,options :list [str ],model :str ,temperature :float ,timeout :float =1.8 )->int :
    if not HAVE_OLLAMA :
        return 0
    prompt =f'You are a firm manager. Read the context and pick ONE option index.\n\nContext:\n{context }\n\nOptions (reply ONLY the number):\n'+'\n'.join ((f'- {i }: {opt }'for i ,opt in enumerate (options )))+'\n\nAnswer format: just the NUMBER (e.g., 0)'

    def _call ():
        return ollama .chat (model =model ,messages =[{'role':'user','content':prompt }],options ={'temperature':temperature })
    try :
        with ThreadPoolExecutor (max_workers =1 )as ex :
            resp =ex .submit (_call ).result (timeout =timeout )
        text =(resp .get ('message',{})or {}).get ('content','')if isinstance (resp ,dict )else ''
        m =re .search ('\\b(\\d+)\\b',text )
        if not m :
            return 0
        idx =int (m .group (1 ))
        return idx if 0 <=idx <len (options )else 0
    except TimeoutError :
        return 0
    except Exception :
        return 0

@dataclass
class FirmAgent :
    id :int
    price :float =1.0
    wage_offer :float =20.0
    desired_margin :float =0.15
    labor :int =0
    capacity :int =0
    inventory :float =0.0
    cash :float =10000.0
    vacancies :int =0
    demand_ema :float =10.0

    def forecast_and_set_vacancies (self ,recent_demand :float ,use_llm :bool ,step :int ,decision_interval :int ,llm_model :str ,llm_temperature :float )->None :
        self .demand_ema =0.8 *self .demand_ema +0.2 *max (0.0 ,recent_demand )
        if use_llm and step %decision_interval ==0 :
            ctx =f'Firm #{self .id }: demand_ema={self .demand_ema :.2f}, labor={self .labor }, vacancies={self .vacancies }, cash={self .cash :.2f}'
            opts =['hire_more','hold','reduce_headcount']
            idx =_llm_choose (ctx ,opts ,llm_model ,llm_temperature )
            if opts [idx ]=='hire_more':
                target_labor =max (self .labor ,math .ceil (self .demand_ema /5.0 ))
                self .vacancies =max (0 ,target_labor -self .labor )
            elif opts [idx ]=='reduce_headcount':
                self .vacancies =max (0 ,self .vacancies -1 )
                self .fire (1 if self .labor >0 else 0 )
            else :
                self .vacancies =max (0 ,self .vacancies )
        else :
            target_labor =max (0 ,math .ceil (self .demand_ema /5.0 ))
            self .vacancies =max (0 ,target_labor -self .labor )

    def set_wage_and_price (self ,market_wage :float ,input_cost_index :float ,use_llm :bool ,step :int ,decision_interval :int ,llm_model :str ,llm_temperature :float )->None :
        if use_llm and step %decision_interval ==0 :
            ctx =f'Firm #{self .id } set wage & price.\nmarket_wage={market_wage :.2f}, current_wage_offer={self .wage_offer :.2f}, desired_margin={self .desired_margin :.2f}, inventory={self .inventory :.2f}'
            wi =_llm_choose (ctx +'\nChoose wage policy.',['below_market','at_market','premium_5pct'],llm_model ,llm_temperature )
            if wi ==0 :
                self .wage_offer =max (12.0 ,0.95 *market_wage if market_wage else self .wage_offer )
            elif wi ==2 :
                self .wage_offer =max (12.0 ,1.05 *market_wage if market_wage else self .wage_offer )
            else :
                self .wage_offer =max (12.0 ,market_wage if market_wage else self .wage_offer )
            pi =_llm_choose (ctx +'\nChoose price adjustment.',['cut_2pct','hold','raise_1pct'],llm_model ,llm_temperature )
            if pi ==0 :
                self .price =max (0.5 ,self .price *0.98 )
            elif pi ==2 :
                self .price =max (0.5 ,self .price *1.01 )
            else :
                self .price =max (0.5 ,self .price )
        else :
            premium =1.05 if self .vacancies >0 else 1.0
            self .wage_offer =max (12.0 ,premium *(market_wage if market_wage else self .wage_offer ))
            effective_scale =max (1.0 ,float (self .labor ))
            unit_cost =self .wage_offer /effective_scale +0.5 *input_cost_index
            self .price =max (0.5 ,(1.0 +self .desired_margin )*unit_cost )

    def can_hire (self )->bool :
        return self .vacancies >0 and self .cash >self .wage_offer *2.0

    def hire (self ,seeker_id :int ,seeker_skill :float ,job_market )->bool :
        if not self .can_hire ():
            return False
        self .labor +=1
        self .vacancies -=1
        job_market .notify_hire (seeker_id ,self .id ,self .wage_offer )
        return True

    def fire (self ,n :int =1 )->int :
        k =min (n ,self .labor )
        self .labor -=k
        return k

    def produce_and_sell (self ,demand_signal :float ):
        produced =self .labor *5.0
        self .inventory +=produced
        sell_qty =min (self .inventory ,max (0.0 ,demand_signal ))
        self .inventory -=sell_qty
        revenue =sell_qty *self .price
        wage_bill =self .labor *self .wage_offer
        self .cash +=revenue -wage_bill
        if self .inventory >2.0 *self .demand_ema :
            self .price *=0.98
        elif sell_qty >0.9 *max (1.0 ,produced ):
            self .price *=1.01
        self .price =max (0.5 ,self .price )
        return (sell_qty ,produced ,revenue )