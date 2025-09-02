from dataclasses import dataclass
import math
import random

@dataclass
class BehavioralParams :
    loss_aversion :float =2.0
    risk_aversion_gain :float =0.88
    risk_aversion_loss :float =0.88
    present_bias :float =0.15

def cpt_value (x :float ,p :float =1.0 ,bp :BehavioralParams =BehavioralParams ())->float :
    if x >=0 :
        return x **bp .risk_aversion_gain *p
    else :
        return -bp .loss_aversion *(-x )**bp .risk_aversion_loss *p

def discount_future (x :float ,t :int ,bp :BehavioralParams =BehavioralParams ())->float :
    delta =0.97
    beta =1 -bp .present_bias
    return (beta if t >0 else 1.0 )*delta **t *x

def softmax_choice (scores ,temperature =0.5 ):
    mx =max (scores )
    exps =[math .exp ((s -mx )/max (1e-06 ,temperature ))for s in scores ]
    tot =sum (exps )
    r =random .random ()*tot
    run =0
    for i ,e in enumerate (exps ):
        run +=e
        if run >=r :
            return i
    return len (scores )-1