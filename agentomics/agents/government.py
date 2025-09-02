import langroid as lr

class GovernmentAgent (lr .Agent ):

    def __init__ (self ,config ,tax_rate :float =0.2 ,spending :float =10000.0 ):
        super ().__init__ (config )
        self .tax_rate =float (tax_rate )
        self .spending =float (spending )
        self .treasury =0.0

    def collect_taxes (self ,households ,firms )->None :
        for h in households :
            tax =float (h .income )*self .tax_rate
            h .savings -=tax
            self .treasury +=tax
        for f in firms :
            profit =0.0
            try :
                profit =float (getattr (f ,'_last_profit',0.0 ))
            except Exception :
                profit =0.0
            self .treasury +=max (0.0 ,profit )*self .tax_rate

    def set_fiscal_policy (self ,tax_rate :float ,spending :float )->None :
        self .tax_rate =float (tax_rate )
        self .spending =float (spending )

    def distribute_stimulus (self ,households ,amount_per_household :float )->None :
        amt =float (amount_per_household or 0.0 )
        if amt <=0 :
            return
        for h in households :
            h .savings +=amt