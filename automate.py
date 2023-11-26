import stat
from tkinter import NO
import utilities
from pprint import pprint
import pandas as pd
import os
#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("default.csv")
#Final_state and initial_state
sample_state: list[list[str]]=utilities.init_statestypes("default.csv")

transition: list=utilities.transitions("Sample/default2.csv")
#fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values
class automate:
    # initialize the basic automate
    def __init__(self, sample_event:list[list[str]], sample_state:list[list[str]], transition:list=transition) -> None:
        
        self.matrix: list=sample_event
        self.initial_states: list=sample_state[0]
        self.all_states: list=[state[0] for state in sample_event]
        self.final_states: list=sample_state[1]
        self.transitions: list=[transit for transit in transition]
        # self.label=[f"q{i}" for i in range(len(self.matrix)) if self.matrix != []]
    
    
    def create_state(self,name)->None:
        self.matrix.append([])
        self.matrix[-1].append([name])
        self.initial_states.append(0)
        self.final_states.append(0)
        self.all_states.append(name)
        for i in range(1,len(self.matrix[0])):
            self.matrix[-1].append(['nan'])

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
        return ["nan"] in self.matrix[:][:]
    
    def is_deterministic(self)->bool:
        for line in self.matrix:
            for row in line:
                if len(row) > 1:
                    return False
        return True

    def display_transition(self):
        print(self.transitions)
        
    def add_transition(self,initial_state,transition="c",final_state="sale boulot"):
        if not (transition in self.transitions):
             raise ValueError("La transition entrée n'est pas dans la colonne veuillez saisir une autre")
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        if(self.matrix[index_state][index_transition+1][0] == "nan"):
            del self.matrix[index_state][index_transition+1][0]
        self.matrix[index_state][index_transition+1].append(final_state)
        
        
    def display_matrix(self):
        pprint(self.matrix)

    def delete_state(self, state=""): # Verifier que l'automate est coupé en 2
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
        rows, cols= len(self.matrix), len(self.matrix[0])
        csv_file_temp=[["" for _ in range(rows)] for i in range(cols)]
        for i in range(rows):
            for j in range(cols): 
                csv_file_temp[j][i]=",".join(self.matrix[i][j]) if i<len(self.matrix) and j < len(self.matrix[i]) else None
        csv_file.update({"etat":csv_file_temp[0]})
        for i in range(len(transition)):
            csv_file.update({self.transitions[i]:[state for state in csv_file_temp[i+1]]})
            
        csv_file.update({"EI":self.initial_states})
        csv_file.update({"EF":self.final_states})
        df = pd.DataFrame(csv_file)
        df.to_csv(f"Sample/{file}.csv", index=False, sep=';')
    


    
    def possible_transition(self, current_state: str, matrix: list, symbols: list) -> list:
        """Récupère les transitions possibles pour passer d'un état à un autre en fonction du symbole fourni.

        Args:
            current_state (str): État actuel
            matrix (list): Matrice des transitions
            symbols (list): Liste des symboles pour les transitions ('a', 'b', 'c', ...)

        Returns:
            list: Liste des transitions possibles pour passer de l'état actuel à un autre état
        """
        transitions_for_state = matrix[self.all_states.index(current_state)]
        
        transitions_for_symbol = transitions_for_state[symbols.index(symbols)]
        
        return transitions_for_symbol


            

    # TODO: finish AFD and begin AND
    def recognize_wordAFD(self, word: str) -> bool:
        matrix = [elem[1:] for elem in self.matrix]
        
        transition_dict = {}
        for i_transition, transition in enumerate(self.transitions):
            transition_dict.update({transition: i_transition})
        
        i_current_state = self.initial_states.index(1)
        current_state = self.all_states[i_current_state]
        i_final_state = self.final_states.index(1)
        
        for c in word:
            if i_current_state == i_final_state:
                return True  # If the current state is already a final state, the word is recognized
                
            Possible_Transition = self.possible_transition(current_state, matrix, c)
            
            if Possible_Transition:
                i_current_state += 1
                next_state = matrix[i_current_state][transition_dict[c]]
                current_state = self.all_states[i_current_state]
                print(current_state)  # Update the current state
            
        return i_current_state == i_final_state  # Check if the final state is reached after processing the word

    # TODO: begin transform AND in AEF

         
        
automate1=automate(sample_event, sample_state)
automate1.split_states()
#automate1.create_state("bidule")
automate1.display_states()

# print(automate1.is_complete())
# automate1.display_matrix()
# print(automate1.is_deterministic())

# automate1.create_state("sale boulot")
# automate1.display_states()
# #automate1.display_matrix()
#automate1.add_transition("bidule")
# automate1.display_matrix()


#Test suppr
# automate1.delete_state("q0")
# automate1.display_states()
# automate1.display_matrix()
print(automate1.recognize_wordAFD("aada"))

#automate1.edit_csv("test")