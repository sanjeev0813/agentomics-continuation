import numpy as np

def generate_report (households ,firms ,regulator ,housing_market ,financial_market ,total_bankruptcies ,total_new_firms ,report_filename ='report.txt'):
    with open (report_filename ,'w')as f :
        f .write ('Simulation Report\n')
        f .write ('=================\n\n')
        f .write (f'Number of households: {len (households )}\n')
        f .write (f'Initial number of firms: 10\n')
        f .write (f'Final number of firms: {len (firms )}\n')
        f .write (f'Final interest rate: {regulator .interest_rate }\n\n')
        unemployed_count =sum ((1 for household in households if not household .employed ))
        unemployment_rate =unemployed_count /len (households )if households else 0
        f .write (f'Final unemployment rate: {unemployment_rate :.2%}\n')
        total_savings =sum ((household .savings for household in households ))
        f .write (f'Total household savings: {total_savings :,.2f}\n\n')
        f .write ('Firm Stats\n')
        f .write ('----------\n')
        f .write (f'Total bankruptcies: {total_bankruptcies }\n')
        f .write (f'Total new firms created: {total_new_firms }\n')
        if firms :
            total_capital =sum ((f .capital for f in firms ))
            avg_capital =np .mean ([f .capital for f in firms ])
            f .write (f'Total capital stock: {total_capital :,.2f}\n')
            f .write (f'Average capital stock: {avg_capital :,.2f}\n\n')
        else :
            f .write ('No firms remaining.\n\n')
        f .write ('Financial Market Stats\n')
        f .write ('----------------------\n')
        if financial_market .stocks :
            total_market_cap =sum ((s .price *s .quantity for s in financial_market .stocks ))
            stock_market_index =np .mean ([s .price for s in financial_market .stocks ])
            f .write (f'Total market capitalization: {total_market_cap :,.2f}\n')
            f .write (f'Stock market index: {stock_market_index :,.2f}\n\n')
        else :
            f .write ('No stocks in the market.\n\n')
        f .write ('Housing Market Stats\n')
        f .write ('--------------------\n')
        homeowner_count =sum ((1 for h in households if h .housing_status =='owning'))
        homeownership_rate =homeowner_count /len (households )if households else 0
        f .write (f'Homeownership rate: {homeownership_rate :.2%}\n')
        if housing_market .houses :
            avg_house_price =np .mean ([h ['price']for h in housing_market .houses ])
            f .write (f'Average house price: {avg_house_price :,.2f}\n')
            avg_rent =housing_market .get_average_rent ()
            f .write (f'Average rent (for available houses): {avg_rent :,.2f}\n')
        else :
            f .write ('No houses in the market.\n')