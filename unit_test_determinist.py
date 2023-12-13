import unittest
from automate import automate  # Import the automate class

class TestAutomateDeterminist(unittest.TestCase):

    def setUp(self):
        print("\nSetting up for a new test...")

    def tearDown(self):
        print("Test completed.")


    def create_automaton_from_csv(self, file_name):
        print(f"Creating automaton from {file_name}...")
        return automate(file_name)

    def test_deter(self):
        print("Testing Automaton Non-Deterministic to Finite Deterministic (AND to AFD)...")
        automaton = self.create_automaton_from_csv("otomate5.csv")
        #automaton = self.create_automaton_from_csv("UNITTESTS/automaton_nondeterminist.csv")
        automaton.display_matrix()
        automaton.AND_to_AFD()
        self.assertNotIn('q2', automaton.all_states, msg="'q2' should be removed")
        self.assertEqual(len(automaton.all_states), 3, msg="No states should be removed as all are accessible and coaccessible")

        print("\n")
        automaton.display_matrix()
        print("\n")
        
# Run the tests
if __name__ == '__main__':
    unittest.main()
