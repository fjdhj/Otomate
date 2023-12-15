import stat
from tkinter import NO
import utilities
from pprint import pprint
import pandas as pd
import os
import math
from itertools import combinations
import numpy as np
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
    def __init__(self, file_name: str) -> None:
        if not (os.path.isfile(file_name)):
            with open(file_name, "w") as csv_file:
                csv_file.writelines("etat;EI;EF")
        transition: list=utilities.transitions(file_name)
        #Initialize variables
        sample_event: list[list[str]]=utilities.init_graph(file_name)
        #Final_state and initial_state
        sample_state: list[list[str]]=utilities.init_statestypes(file_name)
        self.matrix: list[list[str]]=sample_event
        self.initial_states: list=sample_state[0]
        self.all_states: list=[state[0] for state in sample_event]
        self.final_states: list=sample_state[1]
        self.transitions: list=[transit for transit in transition]
        self.name: str=file_name
        # self.label=[f"q{i}" for i in range(len(self.matrix)) if self.matrix != []]
    
    
    def create_state(self,name)->None:
        while(name in self.all_states):
            name = str(input("Entrez le nom du nouvel état"))
        self.matrix.append([])
        self.matrix[-1].append(name)
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

    def is__deterministic(self) -> bool:
        """
        Check if the automaton is deterministic based on the transition matrix.

        Returns:
            bool: True if the automaton is deterministic, False otherwise.
        """
        for line in self.matrix:
            for row in line:
                if ',' in row:
                    return False  # Non-deterministic, as a comma indicates multiple transitions
        return True

    def display_transition(self):
        print(self.transitions)

    def create_transition(self, transition):
        self.transitions.append(transition)
        for line in self.matrix:
            line.append("nan")

        
    def add_transition(self,initial_state,transition="c",final_state="sale boulot"):
        if not (transition in self.transitions):
             raise ValueError("La transition entrée n'est pas dans la colonne veuillez saisir une autre")
        index_state=self.all_states.index(initial_state)
        index_transition=self.transitions.index(transition)
        if(self.matrix[index_state][index_transition+1][0] == "nan"):
            del self.matrix[index_state][index_transition+1][0]
        self.matrix[index_state][index_transition+1] = final_state
        

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
            
    #TODO Créer la suppression d'une liaison (pas supprimer l'intégralité de la transition)
            
    # FIXME add programm for transition
    def edit_csv(self, file_name: str,AFD: list, final_state:list):
        csv_file={}
        rows, cols= len(AFD), len(AFD[0])
        csv_file_temp=[["" for _ in range(rows)] for i in range(cols)]
        for i in range(rows):
            for j in range(cols):
                csv_file_temp[j][i]=AFD[i][j] if i<len(AFD) and j < len(AFD[i]) else None
        pprint(csv_file_temp)
        csv_file.update({"etat":csv_file_temp[0]})
        for i in range(len(self.transitions)): #J'ai changé transition pour self.transitions
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


            

    # TODO: finish AFD and begin AND
    #FIXME Prendre en compte le fait qu'un caractère n'existe pas dans l'automate
    def recognize_wordAFD(self, word: str) -> bool:
        matrix = [elem[1:] for elem in self.matrix]
        i_current_state = self.initial_states.index(1)
        current_state = self.all_states[i_current_state]
        i_final_state = self.final_states.index(1)
        print(f"The final state is {self.all_states[i_final_state]}")
        for c in word:
            current_state = self.all_states[i_current_state]
            print(f"\nWe analyze this symbol: {c}")
            if i_current_state == i_final_state:
                return True  # If the current state is already a final state, the word is recognized
                
            Possible_Transition = self.possible_transition(current_state, matrix, c)
            print(f"Possible state : {Possible_Transition} for this state: {current_state}")
            if Possible_Transition:
                print("The transition is possible\n")
                if i_current_state >= len(matrix[0])-1:
                    i_current_state=0
                # if we can go directly to the final state without going to another state
                if self.all_states[i_final_state] in Possible_Transition.split(","):
                    to_final=Possible_Transition.split(",").index(self.all_states[i_final_state])
                    
                    print(f"The index of the current state is {i_current_state}")
                    print(self.all_states.index(Possible_Transition.split(",")[to_final])-self.all_states.index(current_state))
                    i_current_state+=self.all_states.index(Possible_Transition.split(",")[to_final])
                    print("ff<ff<",i_current_state)
                    current_state = self.all_states[i_current_state]
                    
                    print(f"The current state: {Possible_Transition.split(',')[-1]} \n")  # Update the current state
                else:
                    i_current_state+=self.all_states.index(Possible_Transition.split(",")[-1])
                    
                    print(f"The index of the current state is {i_current_state}")
                    current_state = self.all_states[i_current_state]
                    print(f"The current state: {Possible_Transition[-1]} \n")  # Update the current state
                    
        print("End of process...")   
        return i_current_state == i_final_state  # Check if the final state is reached after processing the word



    
    # TODO: begin transform AND in AEF
    
    # TODO: 3) Program the algorithm to set transitions between the new states
    
    def combination_of_states(self,states: list)->list:
        """
        Return combinations of all states possible for new automaton
        """
        combin=[comb for size_combination in range(1,len(states)+1)
                      for comb in combinations(states, size_combination)]
        return combin
        
    def enumerate_new_states(self, states: list) -> dict:
        """
        Enumarate all new states that are possible to create for new AFD
        """
        len_states=int(math.pow(2,len(states))) # Number of new states = 2**number of state AND
        new_states={}
        # print(str(chr(97)).capitalize())
        all_combinations=self.combination_of_states(self.all_states)
        for i in range(len_states-1):
            new_name_for_new_states=str(chr(97+i)).capitalize()
            new_states.update({new_name_for_new_states : all_combinations[i]})
        return new_states
    
    # TODO: 2) Create function that allow us to determinate new initial_state and new_final state
    def define_new_state_and_final_states(self,transitions):   
        ...
        
    def create_state_for_AFD(self,symbols:str,i_for_check:int,new_states_to_check:list[dict],name_of_new_state:str,matrix:list)->list:
        states:list=str(new_states_to_check[i_for_check][name_of_new_state]).split(",")
        Possible_transitions:list=[]
        for state in states:
            Possible_transition: list=self.possible_transition(state,matrix,symbols)
            print(f"Possible transition: {Possible_transition}")
            Possible_transitions.append(Possible_transition)
            
        final=list(set(Possible_transitions))
        
        # delete duplicate
        final_temp=list(set(''.join(final).replace(",","").split("q")))

        finals=[]
        final_temp=final_temp[1:]
        for end in final_temp:
            finals.append(f"q{end}")
        return {f"S{i_for_check+1}":",".join(sorted(list(finals)))}

    def AND_to_AFD(self)->tuple:
        """_summary_
        The function is separate in two part,
        1) Enumerate all new state
        2) place in the new tab
        Returns:
            tuple: tuple[0] -> new_atomaton / tuple[1] -> new_final_state
        """
        matrix = [elem[1:] for elem in self.matrix]
        pprint(matrix)
        # for i in range(len(matrix)):
        #     for j in range(len(matrix[i])):
        #         print(matrix[i][j])
        #         if matrix[i][j]=="nan":
        #             matrix[i][j]='poubelle'
        symbols=self.transitions
        new_states_to_check:list[dict]=[]
        i_for_check=0
        #We add the new state firstly S0->q0
        new_states_to_check.append({f"S0": self.all_states[i_for_check]})
        # phase 1
        end=False
        len_states=len(new_states_to_check)
        # We loop 10 times in order to be sure that we go through every states
        for i in range(len(self.all_states)**2-len(new_states_to_check)):
            state_to_check=list(new_states_to_check[-1].keys())[0]
            print("State to visit", state_to_check,"\n")
            for iter_state in range(len(new_states_to_check)):
                name_of_new_state=list(new_states_to_check[iter_state].keys())[0]
                if name_of_new_state==state_to_check:
                    
                    for symb in symbols:
                        states: list=new_states_to_check[iter_state][name_of_new_state].split(",")
                       
                        # loop states ex: S1->{q0,q1}
                        Possible_transitions=[]
                        for state in states:
                            # if there is a nan we do nothing
                            try:
                                Possible_transition=self.possible_transition(state,matrix,symb)
                            except ValueError as e:
                                pass
                            print(f"{name_of_new_state} | Possible transition for {symb} -> {Possible_transition}")
                        
                            Possible_transitions.append(Possible_transition)
                        
                        # We eliminate duplicate elements
                        unique_elements = set()
                        for element in Possible_transitions:
                            unique_elements.update(str(element).split(','))
                        Possible_transitions=",".join(list(sorted(unique_elements)))
                        
                        not_in_states=False
                        for j in range(len(new_states_to_check)):
                            key_name=list(new_states_to_check[j].keys())[0]
                            if Possible_transitions==new_states_to_check[j][key_name]:
                                break
                            elif j==len(new_states_to_check)-1:
                                not_in_states=True
                                if not_in_states:
                                    new_states_to_check.append({f"S{j+1}":Possible_transitions})
                    print(new_states_to_check,"\n")
            
        
        i_for_check+=len(new_states_to_check)-1
                
        # Phase 2
        result:list[list][list]=[[[] for i in range(len(self.transitions))] for i in range(len(new_states_to_check))]
        new_st=[list(state.keys())[0] for state in new_states_to_check]
        #Put states at the right place
        for new_state in new_states_to_check:
            key_name=list(new_state.keys())[0]
            state_possible_transition=new_state[key_name].split(",")
            
            for symb in symbols:
                no_doublon_state:list=[[] for _ in range(len(self.transitions))]
                no_doublon_states=[]
                for state in state_possible_transition:
                    try:
                        state_to_check_transition:str=self.possible_transition(state,matrix,symb)
                    except:
                        pass
                    split_state_to_check_transition=state_to_check_transition.split(",")
                    no_doublon_state[self.transitions.index(symb)].append(split_state_to_check_transition)

                    print(f"{key_name} | {state} : {state_to_check_transition} -> {symb}")
                    for i in range(len(new_states_to_check)):
                        states_to_check=new_states_to_check[i][list(new_states_to_check[i].keys())[0]]
                        if state_to_check_transition == states_to_check:
                            print(f"{state_to_check_transition} : {states_to_check} -> {i}")

                final_states = self.eliminate_duplicate(no_doublon_state, no_doublon_states)
                print(symb,"Final->",final_states)
                self.put_on_new_matrix(symbols, new_states_to_check, symb, result, new_st, key_name, final_states)
            print()
        self.join_list(result)
        i_final_state: int=self.final_states.index(1)
        i_initial_state: int=self.initial_states.index(1)
        final_state: str=self.all_states[i_final_state]
        initial_state: str=self.all_states[i_initial_state]
        all_final_state=[0 for i in range(len(new_states_to_check))]
        all_initial_state=[1 if new_states_to_check[i][new_st[i]]==new_states_to_check[0]["S0"] else 0 for i in range(len(new_states_to_check)) ]
        self.all_states=new_st
        # Create new and new final
        self.init_new_final_state(new_states_to_check, final_state, all_final_state)
        for k in range(len(new_st)):
           new_st[k]:list=new_st[k].split(",")
           new_st[k].extend(result[k])
        self.matrix,self.final_states=new_st, all_final_state
        self.initial_states=all_initial_state
        self.all_states=[]
        for i in range(len(new_st)):
            self.all_states.append(new_st[i][0])

    
        
    def init_new_final_state(self, new_states_to_check, final_state, all_final_state):
        for i in range(len(new_states_to_check)):
            key_name=list(new_states_to_check[i].keys())[0]
            if final_state in new_states_to_check[i][key_name].split(","):
                all_final_state[i]=1

    def join_list(self, result):
        for row in result:
            for i in range(len(row)):
                row[i] = "".join(row[i])
    # intermediate method for the method AND-AFD
    def put_on_new_matrix(self, symbols, new_states_to_check, symb, result, new_st, key_name, final_states):
        for paf in range(len(new_states_to_check)):
            key_name_final=list(new_states_to_check[paf].keys())[0]
            if final_states==new_states_to_check[paf][key_name_final]:
                print(f"{key_name_final}->{new_st.index(key_name)}")
                result[new_st.index(key_name)][symbols.index(symb)].append(key_name_final)
    # intermediate method for the method AND-AFD
    def eliminate_duplicate(self, no_doublon_state, no_doublon_states):
        for k in range(len(no_doublon_state)):
            final_states=[]
            no_doublon_states.extend(no_doublon_state[k])
            for _ in range(len(no_doublon_states)):
                final_states.extend(no_doublon_states[_])
            final_states=",".join(sorted(list(set(final_states))))
        return final_states

    def complement(self):
        # Inverting final states: If a state is final (1), it becomes non-final (0) and vice versa.
        self.final_states = [1 if state == 0 else 0 for state in self.final_states]

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
        #CHANGE product_automaton = automate([], [[], []], combined_transitions)
        product_automaton = automate(f"product{self.name}{other_automaton.name}.csv")

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
        if 1 not in self.initial_states:
            # Handle the scenario when there is no initial state
            return []

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
        
    #FIXME NATHAN MARCHE PAS
    def make_complete(self):
        modified = False
        for state in self.all_states:
            index_state = self.all_states.index(state)
            for transition in self.transitions:
                index_transition = self.transitions.index(transition)
                if(self.matrix[index_state][index_transition+1]) == "nan":
                    if (modified == False):
                        modified = True
                        if ("poubelle" not in self.all_states):
                            self.create_state("poubelle")
                            for bin_transition in self.transitions:
                                self.add_transition("poubelle", bin_transition, "poubelle")
                    self.add_transition(state, transition, "poubelle")
        return modified
        
#automate1=automate("Sample/default3det.csv")
#automate1.display_matrix()
# automate1.display_states()
# automate1.make_complete()
# automate1.display_matrix()
# automate1.display_states()
# automate1.split_states()
# #automate1.create_state("bidule")
# automate1.display_states()

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
#print(automate1.recognize_wordAFD("ab"))

# automate1.make_complete()
# print(automate1.is_complete())
# print(automate1.display_matrix())
# if not automate1.is_deterministic():
#     automate1.AND_to_AFD()
# automate1.display_states()
# automate1.edit_csv("testyy",automate1.matrix,automate1.final_states)
# pprint(automate1.AND_to_AFD())
# AFD=automate1.AND_to_AFD()
# print(AFD[0])
# automate1.edit_csv_deterministic("deterministic",AFD[0],AFD[1])


#automate1.edit_csv("test")


# automate1 = automate("default3.csv")
# automate1.display_matrix()
# automate1.display_states()
# print(automate1.make_complete())
# automate1.display_matrix()
# automate1.display_states()
# list=['jj','cc']
# list_=",".join(list)
# print(list,list_)

"""POUR IMAHD
Comment edit un csv deterministe:
1) Tu initialises une variable:
auto=automate1.AND_to_AFD()
auto.edit_csv("a", auto[0], auto[1])
et après tu vas dans sample et le nom de fichier a.csv
"""