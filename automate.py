import stat
import utilities
from pprint import pp, pprint
import pandas as pd
import os
#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Sample/default.csv")
#Final_state and initial_state
sample_state: list[list[str]]=utilities.init_statestypes("Sample/default.csv")

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

    def display_transition(self):
        print(self.transitions)
        
    def add_transition(self,initial_state,transition="c",final_state="sale boulot"):
        if not (transition in self.transitions):
             raise ValueError("La transition entrée n'est pas dans la colonne veuillez saisir une autre")
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        if(self.matrix[index_state][index_transition][0] == "nan"):
            del self.matrix[index_state][index_transition][0]
        self.matrix[index_state][index_transition].append(final_state)
        
    def display_matrix(self):
        pprint(self.matrix)

    def delete_state(self, state=""):
        if(state in self.all_states):
            index_state = self.all_states.index(state)
            self.all_states.remove(state) 
            del self.matrix[index_state]
            del self.initial_states[index_state]
            del self.final_states[index_state]
            for i in range(len(self.matrix)-1):
                for transition_states in self.matrix[i]:
                    for test_state in transition_states:
                        if(test_state == state):
                            transition_states.remove(state)
                            if(transition_states == []):
                                transition_states.append("nan")
        else:
            print("L'état à supprimer n'existe pas")
    
    def delete_transition(self, transition):
        if(transition in self.transitions):
            self.transitions.remove(transition)
        else:
            print("La transition à supprimer n'existe pas")
    
    def edit_csv(self,file):
        csv_file={}
        csv_file_temp=[[] for i in range(len(self.matrix))]
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                csv_file_temp[i].append(",".join(self.matrix[j][i]))
        pprint(csv_file_temp)
        csv_file.update({"etat":csv_file_temp[0]})
        for i in range(len(transition)):
            csv_file.update({self.transitions[i]:[state for state in csv_file_temp[i+1]]})
        
        
        csv_file.update({"EI":[0 for i in range(5)]})
        csv_file.update({"EF":[0 for i in range(5)]})
        
        # pprint(csv_file)
        df = pd.DataFrame(csv_file)
        print(df)
        # df['']=self.all_states
        
        #df.to_csv(f"Sample/{file}.csv", sep=";")
        # Chargez le fichier CSV dans un DataFrame
        # df = pd.read_csv(f"Sample/{file}.csv", delimiter=';')
        # df = pd.DataFrame(csv_file)
        # # Mettez à jour les valeurs du DataFrame en utilisant le dictionnaire
        # for colonne, val in csv_file.items():
        #     df[colonne] = val
        # print(df)
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


#Test suppr
automate1.delete_state("q0")
# automate1.display_states()
# automate1.display_matrix()


automate1.edit_csv("test")