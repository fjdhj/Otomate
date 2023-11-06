import utilities
from pprint import pprint
#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Sample/default2.csv")
#Final_state and initial_state
sample_state: list[list[str]]=utilities.init_statestypes("Sample/default2.csv")

transition: list=utilities.transitions("Sample/default2.csv")
#fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values
class automate:
    # initialize the basic automate
    def __init__(self, sample_event:list[list[str]], sample_state:list[list[str]],transition:list=transition) -> None:
        
        self.matrix: list=sample_event
        self.initial_states: list=sample_state[0]
        self.all_states: list=[state[0] for state in sample_event]
        self.final_states: list=sample_state[1]
        self.transitions: list=[transit for transit in transition]
        # self.label=[f"q{i}" for i in range(len(self.matrix)) if self.matrix != []]
    
    # display the necessary information about the states 
    def display_states(self) -> None:
        output=f"""
Initial_states: {self.initial_states}
Current_States: {self.all_states}
Final_states: {self.final_states} 
        """
        print(output)
        
    def split_states(self) -> None:
        """example:
        This function allow us to manipulate more easily the transitions
        'q1,q2' -> [q1,q2]
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j]=str(self.matrix[i][j]).split(',')
    
    
    def is_complete(self) -> bool:
        complete=True
        i=0
        len_matrix=len(self.matrix)
        while complete and i<len_matrix:
            if ['nan'] in self.matrix[i]:
                complete=False
            i+=1
        return complete
    
    def is_deterministic(self)->bool:
        deterministic=True
        for line in self.matrix:
            for row in line:
                if len(row) > 1:
                    deterministic=False
                    break
        return deterministic
    
    def create_state(self,name)->None:
        self.matrix.append([])
        self.matrix[-1].append([name])
        self.all_states.append(name)
        for i in range(1,len(self.matrix[0])):
            self.matrix[-1].append(['nan'])
    
    def add_transition(self,initial_state,transition="c",final_state="boulot"):
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        self.matrix[index_state][index_transition].append(final_state)
        
        
    def display_matrix(self):
        pprint(self.matrix)
    
    
automate1=automate(sample_event, sample_state)
automate1.split_states()
automate1.create_state("bidule")
automate1.display_states()

print(automate1.is_complete())
automate1.display_matrix()
print(automate1.is_deterministic())

automate1.create_state("sale boulot")
automate1.display_states()
#automate1.display_matrix()
automate1.add_transition("bidule")
automate1.display_matrix()