import stat
from tkinter import NO
import utilities
from pprint import pp, pprint
import pandas as pd
import math
import os
# Initialize variables
sample_event: list[list[str]] = utilities.init_graph("Sample/default.csv")
# Final_state and initial_state
sample_state: list[list[str]] = utilities.init_statestypes(
    "Sample/default.csv")

transition: list = utilities.transitions("Sample/default.csv")
# fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values


class automate:
    # initialize the basic automate
    def __init__(self, sample_event: list[list[str]], sample_state: list[list[str]], transition: list = transition) -> None:

        self.matrix: list = sample_event
        self.initial_states: list = sample_state[0]
        self.all_states: list = [state[0] for state in sample_event]
        self.final_states: list = sample_state[1]
        self.transitions: list = [transit for transit in transition]
        # self.label=[f"q{i}" for i in range(len(self.matrix)) if self.matrix != []]

    def create_state(self, name) -> None:
        self.matrix.append([])
        self.matrix[-1].append([name])
        self.initial_states.append(0)
        self.final_states.append(0)
        self.all_states.append(name)
        for i in range(1, len(self.matrix[0])):
            self.matrix[-1].append(['nan'])

    # display the necessary information about the states
    def display_states(self) -> None:
        output = f"""
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
                self.matrix[i][j] = str(self.matrix[i][j]).split(',')

    def is_complete(self) -> bool:
        complete = True
        i = 0
        len_matrix = len(self.matrix)
        while complete and i < len_matrix:
            if ['nan'] in self.matrix[i]:
                complete = False
            i += 1
        return complete

    def is_deterministic(self) -> bool:
        for line in self.matrix:
            for row in line:
                if len(row) > 1:
                    return False
        return True

    def display_transition(self):
        print(self.transitions)

    # ... (other methods)
    # ... (other methods)

    # ... (existing methods)

    # ... (other existing methods)

    def add_transition(self, initial_state, transition_symbol, final_state):
        # Find the index of the initial state and transition symbol
        index_state = self.all_states.index(initial_state)
        # +1 to account for the state name in self.matrix
        index_transition = self.transitions.index(transition_symbol) + 1

        # Get the current transition for the state and symbol
        current_transition = self.matrix[index_state][index_transition]

        # Handle the case of no existing transition (nan)
        if current_transition == 'nan':
            self.matrix[index_state][index_transition] = final_state
        else:
            # If there is an existing transition, update it
            # Check if the current transition is a single state or a list of states
            if ',' in current_transition:
                # Split the current transition into a list, add the new state if it's not already there, and join back
                current_transitions = current_transition.split(',')
                if final_state not in current_transitions:
                    current_transitions.append(final_state)
                self.matrix[index_state][index_transition] = ','.join(
                    current_transitions)
            else:
                # If the current transition is a single state, create a list with the new state
                if current_transition != final_state:
                    self.matrix[index_state][index_transition] = ','.join(
                        [current_transition, final_state])

    # ... (rest of the automate class)

    def display_matrix(self):
        pprint(self.matrix)

    def delete_state(self, state=""):  # Verifier que l'automate est coupé en 2
        if (state in self.all_states):
            index_state = self.all_states.index(state)
            self.all_states.remove(state)
            del self.matrix[index_state]
            del self.initial_states[index_state]
            del self.final_states[index_state]
            for i in range(len(self.matrix)-1):
                for transition_states in self.matrix[i]:
                    for test_state in transition_states:
                        if (test_state == state):
                            transition_states.remove(state)
                            if (transition_states == []):
                                transition_states.append("nan")
        else:
            print("L'état à supprimer n'existe pas")

    def delete_transition(self, transition):
        if (transition in self.transitions):
            self.transitions.remove(transition)
        else:
            print("La transition à supprimer n'existe pas")

    def complement(self):
        # Inverting final states: If a state is final (1), it becomes non-final (0) and vice versa.
        self.final_states = [1 if state ==
                             0 else 0 for state in self.final_states]

    def edit_csv(self, filename):
        # Create a DataFrame to hold the CSV data
        csv_data = {
            'etat': self.all_states,
            'EI': self.initial_states,
            'EF': self.final_states
        }

        # Process transitions for each symbol
        for symbol_index, symbol in enumerate(self.transitions):
            csv_data[symbol] = []
            for state_index in range(len(self.all_states)):
                # Extract the transition state for this symbol
                transition_state = self.matrix[state_index][symbol_index + 1]

                # If the transition state is NaN, convert it to the string 'nan'
                if pd.isna(transition_state):
                    transition_str = 'nan'
                else:
                    transition_str = transition_state

                csv_data[symbol].append(transition_str)

        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame(csv_data)

        # Reorder the DataFrame columns to match the desired format
        column_order = ['etat'] + self.transitions + ['EI', 'EF']
        df = df[column_order]

        # Write to CSV using pandas, with the header
        df.to_csv(f"Sample/{filename}.csv", index=False, header=True, sep=';')

    # ... (existing methods)

    def mirror(self):
        # Initialize a mirrored matrix
        mirrored_matrix = [[state] + ['nan' for _ in self.transitions]
                           for state in self.all_states]

        # Reverse the transitions
        for state_index, state in enumerate(self.all_states):
            for trans_index, transition in enumerate(self.transitions):
                transition_targets = self.matrix[state_index][trans_index + 1]
                if isinstance(transition_targets, float):
                    # Convert the float to a string before splitting
                    transition_targets = str(transition_targets)
                if transition_targets != 'nan':
                    for target_state in transition_targets.split(','):
                        if target_state:
                            # Add a reversed transition in the mirrored matrix
                            target_index = self.all_states.index(target_state)
                            mirrored_matrix[target_index][trans_index + 1] = state

        # Swap the initial and final states
        self.initial_states, self.final_states = self.final_states[:], self.initial_states[:]

        # Update the current object with the mirrored matrix and states
        self.matrix = mirrored_matrix


automate1 = automate(sample_event, sample_state)
automate1.display_matrix()

automate1.mirror()

automate1.display_matrix()
automate1.edit_csv("test")

# mirror_automaton = automate1.mirror()
# mirror_automaton.display_matrix()

# Now, you can edit and save the mirrored automaton if needed
# mirror_automaton.edit_csv("test")

"""
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
"""
