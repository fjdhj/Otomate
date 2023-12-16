import unittest
from automate import automate  # Import the automate class

class TestAutomateTrim(unittest.TestCase):

    def setUp(self):
        print("\nSetting up for a new test...")

    def tearDown(self):
        print("Test completed.")


    def create_automaton_from_csv(self, file_name):
        print(f"Creating automaton from {file_name}...")
        return automate(file_name)

    def test_trim_inaccessible_states(self):
        print("Testing trim method for inaccessible states...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_inaccessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertNotIn('q4', automaton.all_states, msg="'q4' should be removed as it is inaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")


    def test_trim_uncoaccessible_states(self):
        print("Testing trim method for uncoaccessible states...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_uncoaccessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertNotIn('q3', automaton.all_states, msg="'q3' should be removed as it is uncoaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")

    def test_trim_fully_accessible_coaccessible(self):
        print("Testing trim method for a fully accessible and coaccessible automaton...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_fully_accessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertEqual(len(automaton.all_states), 3, msg="No states should be removed as all are accessible and coaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")

    def test_trim_empty_automaton(self):
        print("Testing trim method for an empty automaton...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_empty.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertEqual(len(automaton.all_states), 0, msg="No states should be present as the automaton is empty")
        print("\n")
        automaton.display_matrix()
        print("\n")
        
# Run the tests
if __name__ == '__main__':
    unittest.main()
