from typing import List ,Dict ,Tuple
import math

def _align_by_index (sim :List [float ],real :List [float ])->Tuple [List [float ],List [float ]]:
    n =min (len (sim ),len (real ))
    return (sim [:n ],real [:n ])

def rmse (sim :List [float ],real :List [float ])->float :
    s ,r =_align_by_index (sim ,real )
    if not s :
        return float ('nan')
    return (sum (((si -ri )**2 for si ,ri in zip (s ,r )))/len (s ))**0.5

def corr (sim :List [float ],real :List [float ])->float :
    s ,r =_align_by_index (sim ,real )
    n =len (s )
    if n <2 :
        return float ('nan')
    ms ,mr =(sum (s )/n ,sum (r )/n )
    num =sum (((si -ms )*(ri -mr )for si ,ri in zip (s ,r )))
    den =(sum (((si -ms )**2 for si in s ))*sum (((ri -mr )**2 for ri in r )))**0.5
    return num /den if den else float ('nan')

def validate_unemployment (sim_history :List [float ],real_series :List [Dict [str ,float ]])->Dict [str ,float ]:
    real_vals =[row ['value']for row in real_series ]
    return {'unemp_rmse':rmse (sim_history ,real_vals ),'unemp_corr':corr (sim_history ,real_vals )}

def validate_cpi (sim_history :List [float ],real_series :List [Dict [str ,float ]])->Dict [str ,float ]:
    real_vals =[row ['value']for row in real_series ]
    return {'cpi_rmse':rmse (sim_history ,real_vals ),'cpi_corr':corr (sim_history ,real_vals )}