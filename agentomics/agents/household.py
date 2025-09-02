from __future__ import annotations
from dataclasses import dataclass ,field
from typing import Optional
import re
from concurrent .futures import ThreadPoolExecutor ,TimeoutError
try :
    import ollama
    HAVE_OLLAMA =True
except Exception :
    ollama =None
    HAVE_OLLAMA =False
from agentomics .behavior import BehavioralParams ,cpt_value ,softmax_choice

def _llm_choose (context :str ,options :list [str ],model :str ,temperature :float ,timeout :float =1.8 )->int :
    if not HAVE_OLLAMA :
        return 0
    prompt =f'You are a rational-but-noisy economic agent. Read the context and pick exactly ONE option index.\n\nContext:\n{context }\n\nOptions (reply ONLY the number):\n'+'\n'.join ((f'- {i }: {opt }'for i ,opt in enumerate (options )))+'\n\nAnswer format: just the NUMBER (e.g., 0)'

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
class HouseholdAgent :
    id :int
    savings :float =5000.0
    income :float =0.0
    employed :bool =False
    employer_id :Optional [int ]=None
    wage :float =0.0
    skill :float =1.0
    house_owned :bool =False
    paying_rent :bool =False
    monthly_rent :float =0.0
    mortgage_payment :float =0.0
    behavioral :BehavioralParams =field (default_factory =BehavioralParams )

    def decide_housing (self ,housing_market ,use_llm :bool ,step :int ,decision_interval :int ,llm_model :str ,llm_temperature :float )->None :
        if self .house_owned :
            return
        price ,rent =housing_market .get_quotes ()
        down =0.2 *price
        can_buy =self .savings >=down
        current_cost =self .monthly_rent if self .paying_rent else 0.0
        base_util =cpt_value (self ._step_income_minus (current_cost ),bp =self .behavioral )
        rent_util =cpt_value (self ._step_income_minus (rent ),bp =self .behavioral )
        opts =[('stay',base_util ),('rent',rent_util )]
        if can_buy :
            mort =housing_market .estimate_mortgage (price ,down_payment =down )
            buy_util =cpt_value (self ._step_income_minus (mort ),bp =self .behavioral )
            opts .append (('buy',buy_util ))
        labels =[o [0 ]for o in opts ]
        if use_llm and step %decision_interval ==0 :
            ctx =f'Household #{self .id } deciding housing.\nsavings={self .savings :.2f}, income={self .income :.2f}, rent_current={self .monthly_rent :.2f}, mortgage_current={self .mortgage_payment :.2f}\nmarket_price={price :.2f}, market_rent={rent :.2f}, can_buy={can_buy }'
            idx =_llm_choose (ctx ,labels ,llm_model ,llm_temperature )
        else :
            idx =softmax_choice ([u for _ ,u in opts ])
        choice =labels [idx ]
        if choice =='rent':
            if not self .paying_rent or rent <0.95 *self .monthly_rent :
                if housing_market .rent_house (self .id ,rent ):
                    self .paying_rent =True
                    self .house_owned =False
                    self .monthly_rent =rent
                    self .mortgage_payment =0.0
        elif choice =='buy'and can_buy :
            if housing_market .buy_house (self .id ,price ,down_payment =down ):
                self .house_owned =True
                self .paying_rent =False
                self .savings -=down
                self .mortgage_payment =housing_market .estimate_mortgage (price ,down_payment =down )
                self .monthly_rent =0.0

    def decide_labor (self ,job_market ,use_llm :bool ,step :int ,decision_interval :int ,llm_model :str ,llm_temperature :float )->None :
        if self .employed :
            bench =job_market .avg_posted_wage ()
            if bench and self .wage <0.8 *bench :
                if use_llm and step %decision_interval ==0 :
                    ctx =f'Household #{self .id } employed at wage={self .wage :.2f}, market_wage={bench :.2f}. Consider quitting?'
                    idx =_llm_choose (ctx ,['stay','quit'],llm_model ,llm_temperature )
                    if idx ==1 :
                        self ._resign ()
                else :
                    self ._resign ()
        if not self .employed :
            job_market .register_seeker (self .id ,self .skill )

    def accept_offer (self ,firm_id :int ,wage :float ):
        self .employed =True
        self .employer_id =firm_id
        self .wage =wage

    def _resign (self ):
        self .employed =False
        self .employer_id =None
        self .wage =0.0

    def realize_income (self )->float :
        gross =self .wage if self .employed else 0.0
        cost =0.0
        if self .paying_rent :
            cost +=self .monthly_rent
        if self .house_owned :
            cost +=self .mortgage_payment
        disposable =max (0.0 ,gross -cost )
        consume =disposable *(0.75 +0.1 *(1 -self .behavioral .present_bias ))
        consume =max (0.0 ,min (consume ,disposable ))
        self .income =gross
        self .savings +=disposable -consume
        return consume

    def _step_income_minus (self ,expense :float )->float :
        gross =self .wage if self .employed else 0.0
        return gross -expense