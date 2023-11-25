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
sample_state: list[list[str]] = utilities.init_statestypes("Sample/default.csv")
transition: list = utilities.transitions("Sample/default.csv")
# fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values

sample_event2: list[list[str]] = utilities.init_graph("Sample/default2.csv")
# Final_state and initial_state
sample_state2: list[list[str]] = utilities.init_statestypes("Sample/default2.csv")
transition2: list = utilities.transitions("Sample/default2.csv")



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

    def display_matrix(self):
        pprint(self.matrix)

    def display_states(self):
        """Display the initial states, final states, and all states of the automaton."""
        print("Initial States:", self.initial_states)
        print("Final States:", self.final_states)
        print("All States:", self.all_states)

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
        df.to_csv(f"{filename}.csv", index=False, header=True, sep=';')

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

    def product(self, other_automaton):
        combined_transitions = list(set(self.transitions + other_automaton.transitions))
        product_automaton = automate([], [[], []], combined_transitions)

        for state1 in self.all_states:
            for state2 in other_automaton.all_states:
                combined_state = f"{state1}_{state2}"
                product_automaton.all_states.append(combined_state)

                # Initial state logic: True if both states are initial
                is_initial = (self.initial_states[self.all_states.index(state1)] == 1 and
                            other_automaton.initial_states[other_automaton.all_states.index(state2)] == 1)
                product_automaton.initial_states.append(1 if is_initial else 0)

                # Final state logic: True if both states are final
                is_final = (self.final_states[self.all_states.index(state1)] == 1 and
                            other_automaton.final_states[other_automaton.all_states.index(state2)] == 1)
                product_automaton.final_states.append(1 if is_final else 0)

        # Initialize the transition matrix with proper length
        for _ in product_automaton.all_states:
            product_automaton.matrix.append(['nan'] * (len(combined_transitions) + 1))  # +1 for state itself

        for i, combined_state in enumerate(product_automaton.all_states):
            state1, state2 = combined_state.split('_')
            idx1 = self.all_states.index(state1)
            idx2 = other_automaton.all_states.index(state2)

            for trans_symbol in combined_transitions:
                trans_idx = combined_transitions.index(trans_symbol)
                trans_state1 = str(self.matrix[idx1][self.transitions.index(trans_symbol) + 1]) if trans_symbol in self.transitions else 'nan'
                trans_state2 = str(other_automaton.matrix[idx2][other_automaton.transitions.index(trans_symbol) + 1]) if trans_symbol in other_automaton.transitions else 'nan'

                if trans_state1 != 'nan' and trans_state2 != 'nan':
                    # Handling non-deterministic transitions
                    combined_transitions_list = []
                    for t1 in trans_state1.split(','):
                        for t2 in trans_state2.split(','):
                            combined_transitions_list.append(f"{t1}_{t2}")
                    combined_transition = ','.join(combined_transitions_list)
                else:
                    combined_transition = 'nan'

                product_automaton.matrix[i][trans_idx + 1] = combined_transition

        return product_automaton



    def concatenate(self, other_automaton):
        combined_transitions = list(set(self.transitions + other_automaton.transitions))
        concatenated_automaton = automate([], [[], []], combined_transitions)

        prefix_A = "A_"
        prefix_B = "B_"

        # Concatenate states and transitions from the first automaton
        for state in self.all_states:
            new_state = prefix_A + state
            concatenated_automaton.all_states.append(new_state)
            concatenated_automaton.initial_states.append(self.initial_states[self.all_states.index(state)])
            concatenated_automaton.final_states.append(0)  # Final states are only from the second automaton

            new_transitions = [new_state] + ['nan' for _ in combined_transitions]
            for i, trans_symbol in enumerate(self.transitions):
                trans_state = self.matrix[self.all_states.index(state)][i + 1]
                if pd.isna(trans_state):
                    new_transitions[combined_transitions.index(trans_symbol) + 1] = 'nan'
                else:
                    new_transitions[combined_transitions.index(trans_symbol) + 1] = prefix_A + trans_state
            concatenated_automaton.matrix.append(new_transitions)

        # Concatenate states and transitions from the second automaton
        for state in other_automaton.all_states:
            new_state = prefix_B + state
            concatenated_automaton.all_states.append(new_state)
            concatenated_automaton.initial_states.append(0)  # Initial state is only from the first automaton
            concatenated_automaton.final_states.append(other_automaton.final_states[other_automaton.all_states.index(state)])

            new_transitions = [new_state] + ['nan' for _ in combined_transitions]
            for i, trans_symbol in enumerate(other_automaton.transitions):
                trans_state = other_automaton.matrix[other_automaton.all_states.index(state)][i + 1]
                if pd.isna(trans_state):
                    new_transitions[combined_transitions.index(trans_symbol) + 1] = 'nan'
                else:
                    new_transitions[combined_transitions.index(trans_symbol) + 1] = prefix_B + trans_state
            concatenated_automaton.matrix.append(new_transitions)

        # Link final states of the first automaton to initial state of the second automaton
        for i, is_final in enumerate(self.final_states):
            if is_final == 1:
                initial_state_of_B = other_automaton.all_states[other_automaton.initial_states.index(1)]
                for trans_symbol in combined_transitions:
                    if trans_symbol in other_automaton.transitions:
                        concatenated_automaton.matrix[i][combined_transitions.index(trans_symbol) + 1] = prefix_B + initial_state_of_B
                        break

        return concatenated_automaton

    # ... (existing methods and constructor)
    # ... (existing methods and constructor)

    # ... (existing methods and constructor)
    # ... (existing methods and constructor)
    # ... (existing methods and constructor)
    # ... (existing methods and constructor)
    # ... (existing methods and constructor)
    # ... (existing methods and constructor)

    def to_regular_expression(self):
        # Initialize regular expressions for each state
        state_expressions = {state: '' for state in self.all_states}

        # Resolve the regular expression for each state
        for state in self.all_states:
            self._resolve_state_expression(state, state_expressions)

        # The regular expression for the entire automaton starts at the initial state
        initial_state = self.all_states[self.initial_states.index(1)]
        return state_expressions[initial_state]

    def _resolve_state_expression(self, state, state_expressions, visited=None):
        if visited is None:
            visited = set()

        # Check if the state's expression has been resolved or if we're in a loop
        if state in visited or state_expressions[state]:
            return
        visited.add(state)

        expression_parts = []
        for trans_symbol, trans_state in zip(self.transitions, self.matrix[self.all_states.index(state)][1:]):
            if trans_state != 'nan':  # Skip 'nan' values
                part = trans_symbol
                if trans_state == state:  # Self-loop
                    part += '*'  # Apply Kleene star for self-loops
                else:
                    # Resolve expressions for non-self transitions
                    self._resolve_state_expression(trans_state, state_expressions, visited.copy())
                    part += state_expressions[trans_state]
                expression_parts.append(part)

        # Combine expressions for the current state
        state_expressions[state] = '|'.join(expression_parts)

# Example Usage
"""
automate1 = automate(sample_event, sample_state, transition)
regex = automate1.to_regular_expression()
print("Regular Expression:", regex)
"""


automate1 = automate(sample_event, sample_state, transition)
automate2 = automate(sample_event2, sample_state2, transition2)

automate3 = automate1.product(automate2)
automate3.display_matrix()

#automate3.edit_csv("Sample/test")


#automate3 = automate1.product(automate2)

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
