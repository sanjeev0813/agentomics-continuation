class JobMarket :

    def __init__ (self ):
        self .vacancies =[]
        self .applicants =[]

    def add_vacancy (self ,firm ):
        self .vacancies .append (firm )

    def add_applicant (self ,household ):
        self .applicants .append (household )

    def match (self ):
        for firm in self .vacancies :
            for household in list (self .applicants ):
                if not household .employed :
                    firm .hire (household )
                    self .applicants .remove (household )
                    break
        self .vacancies =[]