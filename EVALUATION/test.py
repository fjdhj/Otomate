import stat
from tkinter import NO
import utilities
from expression import expression
from pile import pile
from pprint import pprint
import pandas as pd
import os
import math
from itertools import combinations
import numpy as np

class automate:
    """
    A class representing a finite automaton, capable of various operations such as complementing the automaton.

    Attributes:
    matrix (list of list of str): Represents the transition table of the automaton.
    initial_states (list): List of initial states in the automaton.
    all_states (list): List of all states in the automaton.
    final_states (list): List of final states in the automaton.
    transitions (list): List of transitions in the automaton.
    name (str): The name of the automaton, derived from the file name.
    """

    def __init__(self, file_name: str) -> None:
        """
        Initializes an instance of the automate class.

        This constructor initializes an automaton from a given file. The file should contain 
        the necessary details about the states, transitions, and Initial state(s) and Final one(s) of the automaton.

        Args:
            file_name (str): The name of the file from which to load the automaton data.

        Returns:
            None
        """
        if not (os.path.isfile(file_name)):
            print("Création du fichier : ", file_name)
            with open(file_name, "w") as csv_file:
                csv_file.writelines("etat;EI;EF")

        # Extract transition details from the file
        transition: list = utilities.transitions(file_name)
        
        # Initialize the graph and state types from the file
        sample_event: list[list[str]] = utilities.init_graph(file_name)
        sample_state: list[list[str]] = utilities.init_statestypes(file_name)

        # Initialize attributes of the automaton
        self.matrix: list[list[str]] = sample_event
        self.initial_states: list = sample_state[0]
        self.all_states: list = [state[0] for state in sample_event]
        self.final_states: list = sample_state[1]
        self.transitions: list = [transit for transit in transition]
        self.name: str = os.path.splitext(file_name)[0].replace("/", "")

        # self.label=[f"q{i}" for i in range(len(self.matrix)) if self.matrix != []]
    
    
    def create_state(self,name)->None:
        """
        Creates and adds a new state to the automaton.

        This method introduces a new state to the automaton.
        It's a key function for building and modifying the state machine.

        Args:
            name (str): name of the new state

        Returns:
            None
        """
        while(name in self.all_states):
            name = str(input("Entrez le nom du nouvel état"))
        self.matrix.append([])
        self.matrix[-1].append(name)
        self.initial_states.append(0)
        self.final_states.append(0)
        self.all_states.append(name)
        for i in range(1,len(self.transitions)+1):
            self.matrix[-1].append("nan")

    def make_initial(self, state):
        """
        Marks a specified state as an initial state in the automaton.

        This method updates the status of a given state to be an initial state.

        Args:
            state (str): The state to be marked as initial. 

        Returns:
            None
        """
        index_state = self.all_states.index(state)
        self.initial_states[index_state]=1

    def make_final(self, state):
        """
        Marks a specified state as a final state in the automaton.

        This method updates the status of a given state to be a final state.

        Args:
            state (str): The state to be marked as final.

        Returns:
            None
        """
        index_state = self.all_states.index(state)
        self.final_states[index_state]=1

    def demake_initial(self, state):
        """
        Unmarks a specified state as an initial state in the automaton.

        This method reverses the status of a given state from being an initial state.

        Args:
            state (str): The state to be unmarked as initial.

        Returns:
            None
        """
        index_state = self.all_states.index(state)
        self.initial_states[index_state]=0

    def demake_final(self, state):
        """
        Unmarks a specified state as a final state in the automaton.

        This method reverses the status of a given state from being a final state.

        Args:
            state(str): The state to be unmarked as final.

        Returns:
            None
        """
        index_state = self.all_states.index(state)
        self.final_states[index_state]=0

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



    def display_transition(self):
        print(self.transitions)

    def create_transition(self, transition):
        """
        Adds a new transition symbol to the automaton.

        This method introduces a new transition symbol to the automaton and updates the transition matrix
        accordingly. Each state is updated to include this new transition with a default value of 'nan'.

        Args:
            transition (str): The transition symbol to be added.

        Returns:
            None
        """
        self.transitions.append(transition)
        for line in self.matrix:
            line.append(["nan"])

        
    def add_transition(self,initial_state,transition,final_state):
        """
        Adds a transition to the automaton.

        This method introduces a new transition between states in the automaton. If the transition symbol is 
        not already in the automaton, it raises an error.

        Args:
            initial_state (str): The state from which the transition originates.
            transition (str): The symbol representing the transition.
            final_state (str): The state to which the transition leads.

        Raises:
            ValueError: If the transition symbol is not present in the automaton's transitions.

        Returns:
            None
        """
        if not (transition in self.transitions):
             raise ValueError("La transition entrée n'est pas dans la colonne veuillez saisir une autre")
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        if(self.matrix[index_state][index_transition+1] == "nan"):
            self.matrix[index_state][index_transition+1] = final_state
        else:
            self.matrix[index_state][index_transition+1]="{0},{1}".format(str(self.matrix[index_state][index_transition+1]), final_state)

    def remove_transition(self, initial_state, transition, final_state):
        """
        Removes a transition from the automaton.

        This method deletes an existing transition between states. If the transition symbol is not in the 
        automaton, it raises an error.

        Args:
            initial_state (str): The state from which the transition originates.
            transition (str): The symbol representing the transition.
            final_state (str): The state to which the transition leads.

        Raises:
            ValueError: If the transition symbol is not present in the automaton's transitions.

        Returns:
            None
        """
        if not (transition in self.transitions):
             raise ValueError("La transition entrée n'est pas dans la colonne veuillez saisir une autre")
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        if(self.matrix[index_state][index_transition+1] == final_state):
            self.matrix[index_state][index_transition+1] = "nan"
        elif(final_state+"," in self.matrix[index_state][index_transition+1]):
            self.matrix[index_state][index_transition+1] = self.matrix[index_state][index_transition+1].replace(final_state+",", "")
        elif(","+final_state in self.matrix[index_state][index_transition+1]):
            self.matrix[index_state][index_transition+1] = self.matrix[index_state][index_transition+1].replace(","+final_state, "")

    def display_matrix(self):
        """
        Displays the transition matrix of the automaton.

        This method prints the transition matrix, which shows the transitions between the states for each 
        transition symbol.

        Returns:
            None
        """
        pprint(self.matrix)

    def delete_state(self, state=""): # Verifier que l'automate est coupé en 2
        """
        Deletes a state from the automaton.

        This method removes a specified state from the automaton, along with its associated transitions. 
        If the state does not exist, a message is printed.

        Args:
            state (str): The state to be deleted. Default is an empty string.

        Returns:
            None
        """
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
        """
        Deletes a specified transition from the automaton.

        This method removes a transition symbol from the automaton's list of transitions. It also updates the 
        transition matrix by removing the corresponding column. If the transition does not exist, a message 
        is printed.

        Args:
            transition (str): The transition symbol to be removed.

        Returns:
            None
        """
        if(transition in self.transitions):
            index_transition = self.transitions.index(transition)
            self.transitions.remove(transition)
            for line in self.matrix: #Delete column in the matrix
                del line[index_transition+1]
        else:
            print("La transition à supprimer n'existe pas")
            
    def get_neighbour(self, state:int) -> dict:
        """
        This function return the list of neighboors for state
        
        state : the state to check
        
        Return a dictionary of str:list(str) with the name of the transition link to neighbour
        Example : {a:[q0], b:[q0 q1]}
        """
        neighbour:list = {}
        for i in range(1, len(self.matrix[state])):
            if not "nan" in self.matrix[state][i]:
                if isinstance(self.matrix[state][i], str):
                    neighbour[self.transitions[i-1]] = [self.matrix[state][i]]
                else:
                    neighbour[self.transitions[i-1]] = self.matrix[state][i]

        #This is use to remove duplicate entry
        return neighbour
        
    def edit_csv(self, file_name: str,AFD: list, final_state:list):
        if len(AFD)==0:
            print("Rien à exporter.")
            return None
        csv_file={}
        rows, cols= len(AFD), len(AFD[0])
        csv_file_temp=[["" for _ in range(rows)] for i in range(cols)]
        for i in range(rows):
            for j in range(cols):
                csv_file_temp[j][i]=AFD[i][j] if i<len(AFD) and j < len(AFD[i]) else None
        pprint(csv_file_temp)
        csv_file.update({"etat":csv_file_temp[0]})
        for i in range(len(self.transitions)):
            csv_file.update({self.transitions[i]:[state for state in csv_file_temp[i+1]]})
        
        pprint(csv_file)
        csv_file.update({"EI":self.initial_states})
        csv_file.update({"EF":final_state})
        df = pd.DataFrame(csv_file)
        df.to_csv(f"Sample/{file_name}.csv", index=False, sep=';')
        
        df2=pd.read_csv(f"Sample/{file_name}.csv",sep=";")
        df2.replace('nan',np.nan, inplace=True)
        df2.to_csv(f"Sample/{file_name}.csv", index=False, sep=';')
    
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
        transition=self.transitions
        transitions_for_symbol = transitions_for_state[transition.index(symbols)]      
        return transitions_for_symbol
