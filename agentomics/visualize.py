import matplotlib .pyplot as plt
import numpy as np
from typing import Sequence
try :
    import matplotlib
    if not matplotlib .get_backend ().lower ().startswith ('qt'):
        matplotlib .use ('Agg')
except Exception :
    pass

def calculate_gini (savings :np .ndarray |Sequence [float ])->float :
    arr =np .asarray (savings ,dtype =float )
    if arr .size ==0 :
        return 0.0
    arr =np .clip (arr ,0.0 ,None )
    total =arr .sum ()
    if total <=0.0 :
        return 0.0
    sorted_vals =np .sort (arr )
    n =sorted_vals .size
    diff_sum =np .sum (np .abs (sorted_vals [:,None ]-sorted_vals [None ,:]))
    return float (diff_sum /(2.0 *n *total ))

def plot_unemployment (unemployment_rate ,save_path :str |None =None ):
    plt .figure ()
    plt .plot (unemployment_rate )
    plt .title ('Unemployment Rate')
    plt .xlabel ('Step')
    plt .ylabel ('Rate')
    if save_path :
        plt .savefig (save_path ,bbox_inches ='tight',dpi =150 )
        plt .close ()
    else :
        plt .show ()

def plot_gini (gini_coefficient ,save_path :str |None =None ):
    plt .figure ()
    plt .plot (gini_coefficient )
    plt .title ('Gini Coefficient')
    plt .xlabel ('Step')
    plt .ylabel ('Gini')
    if save_path :
        plt .savefig (save_path ,bbox_inches ='tight',dpi =150 )
        plt .close ()
    else :
        plt .show ()