import stat
from tkinter import NO
import utilities
from pprint import pp, pprint
import pandas as pd
import os
#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Sample/default2.csv")
#Final_state and initial_state
sample_state: list[list[str]]=utilities.init_statestypes("Sample/default2.csv")

transition: list=utilities.transitions("Sample/default2.csv")
#fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values



class expression:
    def __init__(self, isFactor:bool|None, isStar: bool|None, state: int|None, content) -> None:
        self.isFactor: bool|None=isFactor
        self.isStar: bool|None=isStar
        self.state: int|None=state #Indice de l'état
        self.content: list|int|expression=content


    def parentheses(self):
        i=0
        parenthesed = True
        while(i<len(self.expression) and parenthesed == True):
            if (isinstance(self.expression[i], expression) and self.expression[i].isFactor == "False"):
                parenthesed = False
        if(parenthesed==False):
            newExpr = expression(self.isFactor, "False", self.state, [self])
            self.isFactor = True
            self.state = None
        return newExpr
    
    def ardenne(self):
        if(self.content == None or self.state == None):
            return False
        if(self.content == None):
            return False
        if():
            ...




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
        complete=True
        i=0
        len_matrix=len(self.matrix)
        while complete and i<len_matrix:
            if ['nan'] in self.matrix[i]:
                complete=False
            i+=1
        return complete
    
    def is_deterministic(self)->bool:
        for line in self.matrix:
            for row in line:
                if len(row) > 1:
                    return False
        return True

    def display_transition(self):
        print(self.transitions)

    def create_transition(self, transition):
        self.transitions.append(transition)
        for line in self.matrix:
            line.append(["nan"])

        
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
            index_transition = self.transitions.index(transition)
            self.transitions.remove(transition)
            for line in self.matrix: #Delete column in the matrix
                del line[index_transition+1] 
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
        for i in range(len(self.transitions)): #J'ai changé transition pour self.transitions
            csv_file.update({self.transitions[i]:[state for state in csv_file_temp[i+1]]})
        csv_file.update({"EI":self.initial_states})
        csv_file.update({"EF":self.final_states})
        df = pd.DataFrame(csv_file)
        df.to_csv(f"Sample/{file}.csv", index=False, sep=';')
    
    def make_complete(self):
        modified = False
        for state in self.all_states:
            index_state = self.all_states.index(state)
            for transition in self.transitions:
                index_transition = self.transitions.index(transition)
                if(self.matrix[index_state][index_transition+1] == ["nan"]):
                    if (modified == False):
                        modified = True
                        if ("poubelle" not in self.all_states):
                            self.create_state("poubelle")
                            for bin_transition in self.transitions:
                                self.add_transition("poubelle", bin_transition, "poubelle")
                    self.add_transition(state, transition, "poubelle")
        return modified
    
    

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
automate1.display_states()
automate1.display_matrix()

#Test suppr TRANSITION
automate1.delete_transition("a")
automate1.display_states()
automate1.display_matrix()


automate1.make_complete()
print("Make Complete :")
automate1.display_states()
automate1.display_matrix()

automate1.create_transition("transtest")
print("Create Transition:")
automate1.display_transition()
automate1.display_matrix()

#automate1.edit_csv("test")