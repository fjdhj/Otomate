import unittest
from automate import automate  # Import the automate class

class TestAutomateTrim(unittest.TestCase):

    def create_automaton_from_csv(self, file_name):
        return automate(file_name)

    def test_trim_inaccessible_states(self):
        automaton = self.create_automaton_from_csv("UNITTEST/automaton_inaccessible.csv")
        automaton.trim()
        self.assertNotIn('q4', automaton.all_states)  # Expecting 'q4' to be removed
    
    def test_trim_uncoaccessible_states(self):
        automaton = self.create_automaton_from_csv("UNITTEST/automaton_uncoaccessible.csv")
        automaton.trim()
        self.assertNotIn('q3', automaton.all_states)  # Expecting 'q3' to be removed

    def test_trim_fully_accessible_coaccessible(self):
        automaton = self.create_automaton_from_csv("UNITTEST/automaton_fully_accessible.csv")
        automaton.trim()
        self.assertEqual(len(automaton.all_states), 3)  # Expecting no states to be removed
        pass

    def test_trim_empty_automaton(self):
        automaton = self.create_automaton_from_csv("UNITTEST/automaton_empty.csv")
        automaton.trim()
        self.assertEqual(len(automaton.all_states), 0)  # Expecting no states as the automaton is empty

# Run the tests
if __name__ == '__main__':
    unittest.main()
