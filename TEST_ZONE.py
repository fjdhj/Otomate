from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
import itertools


# Helper function to convert NFA to DFA
def convert_to_dfa(nfa):
    return DFA.from_nfa(nfa)

# Define the NFA for the first regular expression
nfa1 = NFA(
    states={'q0', 'q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': {'q0'}, 'b': {'q3'}},
        'q3': {'a': {'q0'}}
    },
    initial_state='q0',
    final_states={'q3'}
)

# Define the NFA for the second regular expression
nfa2 = NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': {'q1'}, 'b': {'q3'}},
        'q1': {'a': {'q2'}, 'b': {'q3'}},
        'q2': {'a': {'q0'}, 'b': {'q3'}},
        'q3': {'a': {'q0'}}
    },
    initial_state='q0',
    final_states={'q3'}
)

# Convert both NFAs to DFAs
dfa1 = convert_to_dfa(nfa1)
dfa2 = convert_to_dfa(nfa2)


# Helper function to check if two DFAs are equivalent
def are_dfa_equivalent(dfa1, dfa2):
    # Check if both DFAs accept the same input symbols
    if dfa1.input_symbols != dfa2.input_symbols:
        return False

    # Generate test strings (you might need to customize this part)
    test_strings = [''.join(x) for x in itertools.product(dfa1.input_symbols, repeat=3)]

    # Check each string to see if both DFAs accept it
    for string in test_strings:
        accepts_dfa1 = dfa1.accepts_input(string)
        accepts_dfa2 = dfa2.accepts_input(string)
        if accepts_dfa1 != accepts_dfa2:
            return False

    return True

# Check if the DFAs are equivalent
are_equivalent = are_dfa_equivalent(dfa1, dfa2)

# Print the result
print(f"The two automata are {'equivalent' if are_equivalent else 'not equivalent'}.")