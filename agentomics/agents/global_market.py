class GlobalMarket :

    def __init__ (self ,exchange_rate =1.0 ):
        self .exchange_rate =exchange_rate

    def export_goods (self ,firm ,quantity ):
        firm .cash_reserves +=quantity *firm .price *self .exchange_rate

    def import_goods (self ,firm ,quantity ):
        firm .cash_reserves -=quantity *firm .price /self .exchange_rate