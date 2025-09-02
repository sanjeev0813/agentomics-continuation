import langroid as lr
import random

class RegulatorAgent (lr .Agent ):

    def __init__ (self ,config ,central_bank =None ):
        super ().__init__ (config )
        self .central_bank =central_bank

    def collect_data (self ):
        pass

    def set_policy (self ):
        pass

    @property
    def interest_rate (self ):
        return self .central_bank .interest_rate if self .central_bank else 0.02

    def interest_rate_shock (self ,new_rate ):
        if self .central_bank :
            self .central_bank .set_monetary_policy (new_rate ,self .central_bank .money_supply )

    def stimulus_payment (self ,households ,amount ):
        for household in households :
            household .savings +=amount

    def unemployment_shock (self ,households ,shock_rate ):
        for household in households :
            if household .employed and random .random ()<shock_rate :
                household .employed =False

    def productivity_shock (self ,firms ,shock_factor ):
        for firm in firms :
            firm .production_function =lambda l ,k :20 *shock_factor *l **0.5 *k **0.5

    def financial_crisis (self ,households ,financial_market ,social_network ):
        if financial_market .stocks :
            failed_firm =random .choice (financial_market .stocks ).firm
            failed_firm .stock .price =0.01
            for household in households :
                for stock in household .portfolio ['stocks']:
                    if stock ['stock'].firm ==failed_firm :
                        household .savings *=0.5
                        for neighbor in social_network .get_neighbors (household ):
                            neighbor .savings *=0.9

    def technological_disruption (self ,firms ,shock_factor ):
        if firms :
            disrupted_firm =random .choice (firms )
            disrupted_firm .production_function =lambda l ,k :20 *shock_factor *l **0.8 *k **0.2