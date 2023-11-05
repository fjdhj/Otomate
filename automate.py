import pandas as pd
import utilities
import numpy as np

#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Otomate/Sample/default.csv")
sample_state: list[list[str]]=utilities.init_statestypes("Otomate/Sample/default.csv")

class automate:
    # initialize the basic automate
    def __init__(self, sample_event:list[list[str]], sample_state:list[list[str]]) -> None:
        
        self.matrix: list[list[str]]=sample_event
        self.initial_states: list[str]=sample_state[0]
        self.all_states: list[str]=sample_state
        self.final_states: list[str]=sample_state[1]
        self.transitions: list[str]=[]
     
    def display_states(self) -> None:
        """display all information needed about the states
        """
        print(f"""
        Initial_states: {self.initial_states}
        Current_States: {self.all_states}
        Final_states: {self.final_states} 
        """
        )
        

    def __str__(self) -> str:
        output_matrix=str(np.array(self.matrix))
        return (f"Current Matrix: \n {output_matrix}\n")

    
automate1=automate(sample_event, sample_state)
print(automate1)
automate1.display_states()
    