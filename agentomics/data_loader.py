from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict ,List ,Optional

def _first_existing (paths :List [str ])->Optional [Path ]:
    for p in paths :
        pp =Path (p )
        if pp .exists ():
            return pp
    return None

def load_fred_series (path :str ,value_col :str ,date_col :str ='observation_date')->List [Dict [str ,float ]]:
    p =Path (path )
    if not p .exists ():
        return []
    out :List [Dict [str ,float ]]=[]
    with p .open (newline ='')as f :
        reader =csv .DictReader (f )
        for row in reader :
            try :
                date =row [date_col ]
                val_raw =row [value_col ]
                if val_raw is None or val_raw =='':
                    continue
                val =float (val_raw )
                out .append ({'date':date ,'value':val })
            except (KeyError ,ValueError ):
                continue
    return out

def get_real_data ()->Dict [str ,List [Dict [str ,float ]]]:
    unrate_path =_first_existing (['data/UNRATE.csv','UNRATE.csv','/mnt/data/UNRATE.csv'])
    cpi_path =_first_existing (['data/CPIAUCSL.csv','CPIAUCSL.csv','/mnt/data/CPIAUCSL.csv'])
    unemployment =load_fred_series (str (unrate_path ),value_col ='UNRATE')if unrate_path else []
    cpi =load_fred_series (str (cpi_path ),value_col ='CPIAUCSL')if cpi_path else []
    return {'unemployment':unemployment ,'cpi':cpi }