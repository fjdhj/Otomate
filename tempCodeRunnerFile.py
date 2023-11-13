    def mirror(self):
        # Create a new mirrored automaton with reversed transitions
        mirrored_matrix = [list(row) for row in self.matrix]

        # Reverse the transitions in the mirrored matrix
        for state_index, state in enumerate(self.all_states):
            for trans_index, transition in enumerate(self.transitions):
                transition_targets = self.matrix[state_index][trans_index + 1]
                if isinstance(transition_targets, float):
                    # Convert the float to a string before splitting
                    transition_targets = str(transition_targets)
                if transition_targets != 'nan':
                    for target_state in transition_targets.split(','):
                        if target_state:
                            # Update the mirrored matrix with reversed transitions
                            target_index = self.all_states.index(target_state)
                            mirrored_matrix[state_index][trans_index +
                                                         1] = target_state

        # Reverse the initial and final states in the mirrored automaton
        mirrored_initial_states = [1 if state ==
                                   0 else 0 for state in self.final_states]
        mirrored_final_states = [1 if state ==
                                 0 else 0 for state in self.initial_states]

        # Create a new mirrored automaton with the mirrored matrix and states
        mirrored_automaton = automate(mirrored_matrix, [
            mirrored_initial_states, mirrored_final_states], self.transitions)

        return mirrored_automaton
