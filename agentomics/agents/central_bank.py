import langroid as lr

class CentralBankAgent (lr .Agent ):

    def __init__ (self ,config ,interest_rate =0.02 ,money_supply =1000000 ):
        super ().__init__ (config )
        self .interest_rate =interest_rate
        self .money_supply =money_supply

    def set_monetary_policy (self ,interest_rate ,money_supply ):
        self .interest_rate =interest_rate
        self .money_supply =money_supply