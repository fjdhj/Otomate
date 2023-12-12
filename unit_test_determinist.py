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

    def test_trim_inaccessible_states(self):
        print("Testing trim method for inaccessible states...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_nondeterminist.csv")
        automaton.display_matrix()
        #automaton.AND_to_AFD()
        self.assertIn('q1', automaton.all_states, msg="'q4' should be removed as it is inaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")
        
# Run the tests
if __name__ == '__main__':
    unittest.main()
