import utilities
from pprint import pprint
#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Otomate/Sample/default2.csv")
sample_state: list[list[str]]=utilities.init_statestypes("Otomate/Sample/default2.csv")

class automate:
    # initialize the basic automate
    def __init__(self, sample_event:list[list[str]], sample_state:list[list[str]]) -> None:
        
        self.matrix: list=sample_event
        self.initial_states: list=sample_state[0]
        self.all_states: list=sample_state
        self.final_states: list=sample_state[1]
        self.transitions: list=[transition for transition in self.matrix]
    
    # display the necessary information about the states 
    def display_states(self) -> None:
        output=f"""
Initial_states: {self.initial_states}
Current_States: {self.all_states}
Final_states: {self.final_states} 
        """
        print(output)
        
    def split_transition(self) -> None:
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
    
    def display_matrix(self):
        pprint(self.matrix)
    
automate1=automate(sample_event, sample_state)
automate1.split_transition()

automate1.display_states()
print(automate1.is_complete())
automate1.display_matrix()
print(automate1.is_deterministic())