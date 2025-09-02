class HousingMarket :

    def __init__ (self ,initial_price :float =250000.0 ,initial_rent :float =1500.0 ):
        self .avg_price =initial_price
        self .avg_rent =initial_rent
        self .for_sale =50
        self .for_rent =200
        self .price_momentum =0.0
        self .rent_momentum =0.0

    def get_quotes (self ):
        return (self .avg_price ,self .avg_rent )

    def estimate_mortgage (self ,price :float ,down_payment :float ,rate :float =0.06 ,years :int =30 )->float :
        loan =price -down_payment
        m =rate /12
        n =years *12
        return loan *(m *(1 +m )**n )/((1 +m )**n -1 )

    def buy_house (self ,household_id :int ,price :float ,down_payment :float )->bool :
        if self .for_sale <=0 :
            return False
        self .for_sale -=1
        self .price_momentum +=0.02
        return True

    def rent_house (self ,household_id :int ,rent :float )->bool :
        if self .for_rent <=0 :
            return False
        self .for_rent -=1
        self .rent_momentum +=0.01
        return True

    def replenish_stock (self ):
        self .for_sale =max (self .for_sale ,10 )
        self .for_rent =max (self .for_rent ,50 )

    def adjust_prices (self ):
        self .avg_price *=1 +self .price_momentum
        self .avg_rent *=1 +self .rent_momentum
        self .price_momentum *=0.5
        self .rent_momentum *=0.5
        self .avg_price =max (50000 ,self .avg_price )
        self .avg_rent =max (500 ,self .avg_rent )