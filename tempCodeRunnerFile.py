import stat
from tkinter import NO
import utilities
from pprint import pp, pprint
import pandas as pd
import os

#Initialize variables
sample_event: list[list[str]]=utilities.init_graph("Sample/default.csv")
#Final_state and initial_state
sample_state: list[list[str]]=utilities.init_statestypes("Sample/default.csv")

transition: list=utilities.transitions("Sample/default.csv")
#fonction nouvel etat/ modifier les transitions / supprimer un etat/ecrire dans un fichier csv les values

class automate:
    def __init__(self, transitions, state_names, initial_final_states, alphabet):
        self.all_states = state_names
        self.transitions = alphabet
        self.initial_states = initial_final_states[0]
        self.final_states = initial_final_states[1]

        # Adjusting the matrix to handle list-based transitions
        self.matrix = []
        for i, state in enumerate(state_names):
            state_transitions = []
            for trans in transitions[i]:
                state_transitions.append(trans if trans != '-' else ['-'])
            self.matrix.append([state] + state_transitions + [initial_final_states[0][i], initial_final_states[1][i]])
    
    def display_matrix(self):
        for row in self.matrix:
            print(row)

    def create_state(self, name, is_initial=False, is_final=False):
        self.matrix.append([name] + [['-'] for _ in self.transitions] + [int(is_initial), int(is_final)])
        self.all_states.append(name)
        self.initial_states.append(int(is_initial))
        self.final_states.append(int(is_final))

    def add_transition(self, initial_state, symbol, final_state):
        if symbol not in self.transitions:
            raise ValueError("The symbol is not in the automaton's alphabet.")
        
        state_index = self.all_states.index(initial_state)
        symbol_index = self.transitions.index(symbol) + 1

        # Adjusting for list-based transitions
        if final_state not in self.matrix[state_index][symbol_index]:
            self.matrix[state_index][symbol_index].append(final_state)
            if '-' in self.matrix[state_index][symbol_index]:
                self.matrix[state_index][symbol_index].remove('-')

    def delete_state(self, state):
        if state in self.all_states:
            index_state = self.all_states.index(state)
            del self.matrix[index_state]
            del self.all_states[index_state]
            del self.initial_states[index_state]
            del self.final_states[index_state]
        else:
            print("The state to be deleted does not exist.")


    def recognize_word(self, word):
        actual_initial_states = [self.all_states[i] for i, is_initial in enumerate(self.initial_states) if is_initial == 1]
        current_states = set(actual_initial_states)

        for char in word:
            next_states = set()
            for state in current_states:
                state_index = self.all_states.index(state)
                if char in self.transitions:
                    transition_index = self.transitions.index(char) + 1
                    transition_states = self.matrix[state_index][transition_index]
                    for next_state in transition_states:
                        if next_state != '-':
                            next_states.add(next_state)
            current_states = next_states

        return any(self.final_states[self.all_states.index(state)] == 1 for state in current_states)

    def is_automaton_complete(self):
        for row in self.matrix:
            state = row[0]
            transitions = row[1:-2]
            for symbol, transition in zip(self.transitions, transitions):
                if transition == ['-']:
                    print(f"No transition found for state {state} and symbol {symbol}. Automaton is not complete.")
                    return False

        print("All states have transitions for each symbol. Automaton is complete.")
        return True
    
    def make_automaton_complete(self):
        # Adding the 'phi' state if it does not exist
        phi_state = 'phi'
        if phi_state not in self.all_states:
            self.create_state(phi_state)

        # Ensuring that 'phi' state has looping transitions for each symbol
        phi_index = self.all_states.index(phi_state)
        for i, symbol in enumerate(self.transitions, start=1):
            self.matrix[phi_index][i] = [phi_state] if self.matrix[phi_index][i] == ['-'] else self.matrix[phi_index][i]

        # Checking and updating each state's transitions
        for i, row in enumerate(self.matrix):
            for j, trans in enumerate(row[1:-2], start=1):
                if trans == ['-']:
                    self.matrix[i][j] = [phi_state]


    def is_deterministic(self):
        for row in self.matrix:
            # Check each transition for each symbol
            for trans in row[1:-2]:  # Skip state name, EI, and EF
                # Check if transition is a list with more than one state
                if isinstance(trans, list) and len(trans) > 1:
                    return False
        return True



    def edit_csv(self, file):
        # Prepare the header for the CSV file
        header = ['etat'] + self.transitions + ['EI', 'EF']

        # Convert the matrix to a format suitable for CSV writing
        csv_data = []
        for row in self.matrix:
            csv_row = []
            for element in row:
                # If the element is a list, join it into a string; otherwise, keep it as it is
                if isinstance(element, list):
                    joined_element = ','.join(element)
                    csv_row.append(joined_element)
                else:
                    csv_row.append(element)
            csv_data.append(csv_row)

        # Write to CSV
        df = pd.DataFrame(csv_data, columns=header)
        df.to_csv(f"Sample/{file}.csv", index=False, sep=';')



sample_event, state_names = utilities.init_graph("Sample/default.csv")
sample_state = utilities.init_statestypes("Sample/default.csv")
transition = utilities.transitions("Sample/default.csv")




automate1 = automate(sample_event, state_names, sample_state, transition)
automate1.display_matrix()
print("All States: ", automate1.all_states)

print(automate1.is_deterministic())


"""

complete = automate1.is_automaton_complete()
print(complete)
automate1.delete_state("q0")
automate1.display_matrix()
print("All States: ", automate1.all_states)
automate1.edit_csv("testv")
automate1.add_transition("q1","a","q1")
automate1.display_matrix()
print("All States: ", automate1.all_states)
automate1.add_state(q4, is_initial=False, is_final=True)



automate1.edit_csv("testv")



automate1=automate(sample_event, sample_state)
automate1.display_states()
complete=automate1.is_automaton_complete()
print (complete)


word="aaaaaaaaaaaaaaaab"
is_accepted = automate1.recognize_word(word)
print(f"The word '{word}' is {'accepted' if is_accepted else 'not accepted'} by the automaton.")
"""


"""        

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