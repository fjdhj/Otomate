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

    def complement(self):
        # Inverting final states: If a state is final (1), it becomes non-final (0) and vice versa.
        self.final_states = [1 if state ==
                             0 else 0 for state in self.final_states]

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

        if state in visited or (state in state_expressions and state_expressions[state]):
            return
        visited.add(state)

        expression_parts = []
        for trans_symbol, trans_state in zip(self.transitions, self.matrix[self.all_states.index(state)][1:]):
            if pd.isna(trans_state) or trans_state == 'nan':
                continue

            if trans_state == state:
                # Loop on the same state
                part = trans_symbol + '*'
            else:
                # Transition to a different state
                if trans_state not in state_expressions or not state_expressions[trans_state]:
                    self._resolve_state_expression(trans_state, state_expressions, visited.copy())

                next_state_expression = state_expressions[trans_state]
                part = trans_symbol + next_state_expression

            expression_parts.append(part)

        # Sequential concatenation for transitions
        state_expressions[state] = ''.join(expression_parts)

        # Additional handling to encapsulate the entire expression for states with multiple transitions
        if state in self.initial_states and len(expression_parts) > 1:
            state_expressions[state] = '(' + state_expressions[state] + ')*'

    def list_accessible_states(self):
        accessible_states = set()
        queue = []
        initial_state = self.initial_states.index(1)  # Assuming there's only one initial state
        accessible_states.add(initial_state)
        queue.append(initial_state)

        while queue:
            state = queue.pop(0)
            for trans_symbol, trans_state in zip(self.transitions, self.matrix[state][1:]):
                next_states = [i for i, st in enumerate(self.all_states) if trans_state == st]
                for next_state in next_states:
                    if next_state not in accessible_states:
                        accessible_states.add(next_state)
                        queue.append(next_state)

        return [self.all_states[state] for state in accessible_states]

    def list_coaccessible_states(self):
        co_accessible = set()
        queue = []

        for final_state in self.final_states:
            if final_state == 1:
                final_state_index = self.final_states.index(final_state)
                co_accessible.add(final_state_index)
                queue.append(final_state_index)

        while queue:
            current_state = queue.pop(0)
            for state in range(len(self.all_states)):
                if state not in co_accessible:
                    for trans_symbol, trans_state in zip(self.transitions, self.matrix[state][1:]):
                        if current_state in [i for i, st in enumerate(self.all_states) if trans_state == st]:
                            co_accessible.add(state)
                            queue.append(state)
                            break

        return [self.all_states[state] for state in co_accessible]

    def trim(self):
        acc = set(self.list_accessible_states())
        coacc = set(self.list_coaccessible_states())
        states_to_remove = []

        # Identify states that are neither accessible nor co-accessible
        for state in self.all_states:
            if state not in acc or state not in coacc:
                states_to_remove.append(state)

        # Remove identified states and their transitions
        for state in states_to_remove:
            if state in self.all_states:
                state_index = self.all_states.index(state)
                self.all_states.remove(state)
                del self.matrix[state_index]
                del self.initial_states[state_index]
                del self.final_states[state_index]

                # Remove transitions leading to the deleted state
                for row in self.matrix:
                    for i in range(1, len(row)):  # Start from 1 to skip the state name
                        transition_state = row[i]
                        if isinstance(transition_state, float):
                            transition_state = str(transition_state)
                        if transition_state == state:
                            row[i] = 'nan'

        # Additional step to handle transitions leading from the deleted state
        for i, row in enumerate(self.matrix):
            for j in range(1, len(row)):
                transition_state = row[j]
                if isinstance(transition_state, float):
                    transition_state = str(transition_state)
                if ',' in transition_state:
                    transitions = transition_state.split(',')
                    transitions = [t for t in transitions if t in self.all_states]
                    self.matrix[i][j] = ','.join(transitions) if transitions else 'nan'

         
        
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
