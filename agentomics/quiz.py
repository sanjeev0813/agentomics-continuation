def run_quiz (quiz_name ,questions ):
    print (f'\n--- Starting Quiz: {quiz_name } ---')
    score =0
    for i ,q in enumerate (questions ):
        print (f"\nQ{i +1 }: {q ['question']}")
        for j ,option in enumerate (q ['options']):
            print (f'  {j +1 }. {option }')
        while True :
            try :
                answer =int (input ('Your answer (1, 2, 3, ...): '))
                if 1 <=answer <=len (q ['options']):
                    break
                else :
                    print ('Invalid option. Please try again.')
            except ValueError :
                print ('Invalid input. Please enter a number.')
        if answer ==q ['correct_answer']:
            print ('Correct!')
            score +=1
        else :
            print (f"Incorrect. The correct answer was {q ['correct_answer']}.")
    print (f'\n--- Quiz Complete ---')
    print (f'Your score: {score }/{len (questions )}')
    return score
quizzes ={'monetary_policy':{'name':'Monetary Policy','questions':[{'question':'What is the most likely effect of a central bank raising interest rates?','options':['Increased borrowing and spending','Decreased borrowing and spending','No effect on the economy'],'correct_answer':2 },{'question':'What is the primary goal of expansionary monetary policy (like lowering interest rates)?','options':['To control inflation','To stimulate economic growth','To increase taxes'],'correct_answer':2 }]},'unemployment':{'name':'Unemployment','questions':[{'question':"An 'unemployment shock' in the simulation represents:",'options':['A sudden increase in job vacancies','A sudden loss of jobs for many households','A gradual decrease in wages'],'correct_answer':2 }]}}

def get_quiz (quiz_id ):
    return quizzes .get (quiz_id )