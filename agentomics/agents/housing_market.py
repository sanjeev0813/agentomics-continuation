import numpy as np

class HousingMarket :

    def __init__ (self ,num_houses =100 ,initial_price =200000 ):
        self .houses =[]
        for i in range (num_houses ):
            price =initial_price *(1 +np .random .normal (0 ,0.1 ))
            rent =price *0.05
            self .houses .append ({'id':i ,'price':price ,'rent':rent ,'owner':None })
        self .buyers_this_step =[]

    def get_average_house_price (self ):
        prices =[h ['price']for h in self .houses if h ['owner']is None ]
        return np .mean (prices )if prices else 200000

    def get_average_rent (self ):
        rents =[h ['rent']for h in self .houses if h ['owner']is None ]
        return np .mean (rents )if rents else 200000 *0.05

    def buy_house (self ,household ):
        self .buyers_this_step .append (household )

    def match_buyers_and_sellers (self ):
        for_sale =[h for h in self .houses if h ['owner']is None ]
        np .random .shuffle (self .buyers_this_step )
        for buyer in self .buyers_this_step :
            if for_sale :
                house =for_sale .pop (0 )
                house ['owner']=buyer
                buyer .purchase_successful (house ['price'])
        self .buyers_this_step =[]

    def update_prices (self ):
        num_buyers =len (self .buyers_this_step )
        num_houses_for_sale =len ([h for h in self .houses if h ['owner']is None ])
        if num_houses_for_sale >0 :
            demand_pressure =(num_buyers -num_houses_for_sale )/num_houses_for_sale
        else :
            demand_pressure =num_buyers
        price_adjustment_factor =1 +demand_pressure *0.05
        for h in self .houses :
            if h ['owner']is None :
                h ['price']*=price_adjustment_factor
                h ['rent']*=price_adjustment_factor