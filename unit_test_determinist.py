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

    def test_deterministic(self):
        print("Testing Automaton Non-Deterministic to Finite Deterministic (AND to AFD)...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_nondeterminist.csv")
        automaton.display_matrix()
        automaton.AND_to_AFD()
        self.assertNotIn('q0', automaton.all_states, msg="'q0' should be removed")
        self.assertNotIn('q1', automaton.all_states, msg="'q1' should be removed")
        self.assertNotIn('q2', automaton.all_states, msg="'q2' should be removed")
        self.assertEqual(len(automaton.all_states), 3, msg="Same number of states")
        print("\n")
        automaton.display_matrix()
        print("\n")

    def test_deterministic2(self):
        print("Testing the determinism of the output...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_nondeterminist.csv")
        automaton.display_matrix()
        automaton.AND_to_AFD()
        automaton.display_matrix()
        print("\n")

        # Check if the automaton is deterministic
        if automaton.is__deterministic():
            print("Automation is deterministic.")
            self.assertTrue(True)  # The test passes if it's deterministic
        else:
            print("Automation is not deterministic.")
            self.assertTrue(False, "Automation is not deterministic.")  # The test fails with a message
        automaton.display_matrix()
        print("\n")

# Run the tests
if __name__ == '__main__':
    unittest.main()
