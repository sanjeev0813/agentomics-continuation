import sys
from agentomics .simulation import run_simulation
from agentomics .quiz import get_quiz ,run_quiz

def get_custom_params ():
    try :
        num_households =int (input ('Enter number of households (e.g., 10): '))
        num_firms =int (input ('Enter number of firms (e.g., 5): '))
        num_steps =int (input ('Enter number of simulation steps (e.g., 50): '))
        return {'num_households':num_households ,'num_firms':num_firms ,'num_steps':num_steps ,'shocks':[]}
    except ValueError :
        print ('Invalid input. Please enter integers.')
        return None

def main ():
    scenarios ={'1':{'name':'Baseline','quiz_id':None ,'params':{'shocks':[{'step':5 ,'type':'monetary','interest_rate':0.03 ,'money_supply':1100000 },{'step':10 ,'type':'fiscal','tax_rate':0.3 ,'stimulus':12000 }]}},'2':{'name':'High-Interest Rate Shock','quiz_id':'monetary_policy','params':{'shocks':[{'step':5 ,'type':'monetary','interest_rate':0.1 ,'money_supply':1100000 }]}},'3':{'name':'Major Unemployment Shock','quiz_id':'unemployment','params':{'num_steps':20 ,'shocks':[{'step':5 ,'type':'unemployment','rate':0.5 }]}},'4':{'name':'Custom Scenario','quiz_id':None }}
    print ('Available Scenarios:')
    for key ,scenario in scenarios .items ():
        print (f"  {key }: {scenario ['name']}")
    choice =input ('Choose a scenario to run (1-4): ')
    if choice =='4':
        params =get_custom_params ()
        if params :
            print ('\nRunning custom scenario...')
            params ['report_filename']='report_custom.txt'
            run_simulation (**params )
            print ('\nScenario run complete.')
    elif choice in scenarios :
        selected_scenario =scenarios [choice ]
        print (f"\nRunning scenario: {selected_scenario ['name']}...")
        report_filename =f"report_{selected_scenario ['name'].lower ().replace (' ','_')}.txt"
        params =selected_scenario ['params']
        params ['report_filename']=report_filename
        run_simulation (**params )
        print ('\nScenario run complete.')
        if selected_scenario .get ('quiz_id'):
            quiz_data =get_quiz (selected_scenario ['quiz_id'])
            if quiz_data :
                run_quiz (quiz_data ['name'],quiz_data ['questions'])
    else :
        print ('Invalid choice.')
if __name__ =='__main__':
    main ()