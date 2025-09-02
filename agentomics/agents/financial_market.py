import random

class FinancialMarket :

    def __init__ (self ):
        self .stocks =[]
        self .bonds =[]
        self .options =[]
        self .futures =[]
        self .order_book ={}

    def add_stock (self ,stock ):
        self .stocks .append (stock )
        self .order_book [stock ]={'buys':[],'sells':[]}

    def add_bond (self ,bond ):
        self .bonds .append (bond )

    def add_option (self ,option ):
        self .options .append (option )

    def add_future (self ,future ):
        self .futures .append (future )

    def place_buy_order (self ,household ,stock ,quantity ):
        if stock in self .order_book :
            self .order_book [stock ]['buys'].append ({'household':household ,'quantity':quantity })

    def place_sell_order (self ,household ,stock ,quantity ):
        if stock in self .order_book :
            self .order_book [stock ]['sells'].append ({'household':household ,'quantity':quantity })

    def process_orders (self ):
        for stock ,orders in self .order_book .items ():
            buys =orders ['buys']
            sells =orders ['sells']
            total_buy_quantity =sum ((b ['quantity']for b in buys ))
            total_sell_quantity =sum ((s ['quantity']for s in sells ))
            random .shuffle (buys )
            random .shuffle (sells )
            buy_idx =0
            sell_idx =0
            while buy_idx <len (buys )and sell_idx <len (sells ):
                buyer_order =buys [buy_idx ]
                seller_order =sells [sell_idx ]
                trade_quantity =min (buyer_order ['quantity'],seller_order ['quantity'])
                trade_price =stock .price
                buyer_order ['household'].stock_purchase_successful (stock ,trade_quantity ,trade_price )
                seller_order ['household'].stock_sale_successful (stock ,trade_quantity ,trade_price )
                buyer_order ['quantity']-=trade_quantity
                seller_order ['quantity']-=trade_quantity
                if buyer_order ['quantity']==0 :
                    buy_idx +=1
                if seller_order ['quantity']==0 :
                    sell_idx +=1
            excess_demand =total_buy_quantity -total_sell_quantity
            total_volume =total_buy_quantity +total_sell_quantity
            if total_volume >0 :
                price_adjustment_factor =1 +excess_demand /total_volume *0.1
                stock .price *=price_adjustment_factor
                if stock .price <1 :
                    stock .price =1

    def clear_order_book (self ):
        for stock in self .order_book :
            self .order_book [stock ]['buys']=[]
            self .order_book [stock ]['sells']=[]

class Stock :

    def __init__ (self ,firm ,price ,quantity ):
        self .firm =firm
        self .price =price
        self .quantity =quantity

class Bond :

    def __init__ (self ,firm ,price ,quantity ,interest_rate ,maturity ):
        self .firm =firm
        self .price =price
        self .quantity =quantity
        self .interest_rate =interest_rate
        self .maturity =maturity

class Option :

    def __init__ (self ,underlying ,strike_price ,expiration_date ,option_type ):
        self .underlying =underlying
        self .strike_price =strike_price
        self .expiration_date =expiration_date
        self .option_type =option_type

class Future :

    def __init__ (self ,underlying ,price ,expiration_date ):
        self .underlying =underlying
        self .price =price
        self .expiration_date =expiration_date