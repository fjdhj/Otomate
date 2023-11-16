    def product(self, other_automaton):
        combined_transitions = list(set(self.transitions + other_automaton.transitions))
        product_automaton = automate([], [[], []], combined_transitions)

        for state1 in self.all_states:
            for state2 in other_automaton.all_states:
                combined_state = f"{state1},{state2}"
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
            state1, state2 = combined_state.split(',')
            idx1 = self.all_states.index(state1)
            idx2 = other_automaton.all_states.index(state2)

            for trans_symbol in combined_transitions:
                trans_idx = combined_transitions.index(trans_symbol)
                trans_state1 = self.matrix[idx1][self.transitions.index(trans_symbol) + 1] if trans_symbol in self.transitions else 'nan'
                trans_state2 = other_automaton.matrix[idx2][other_automaton.transitions.index(trans_symbol) + 1] if trans_symbol in other_automaton.transitions else 'nan'

                combined_transition = 'nan'
                if trans_state1 != 'nan' or trans_state2 != 'nan':
                    combined_transition = f"{trans_state1 if trans_state1 != 'nan' else state1},{trans_state2 if trans_state2 != 'nan' else state2}"
                product_automaton.matrix[i][trans_idx + 1] = combined_transition  # +1 for the state itself

        return product_automaton
