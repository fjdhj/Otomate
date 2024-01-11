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
#fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values

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
        the necessary details about the states, transitions, and other properties of the automaton.

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

        # The following line is commented out and seems to be for future use or deprecated
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



