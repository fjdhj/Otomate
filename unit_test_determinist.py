import unittest
from automate import automate  # Import the automate class

class TestAutomateDeterminist(unittest.TestCase):
    """
    A test suite for testing the conversion of a non-deterministic automaton to a finite deterministic automaton.

    This class contains test cases to evaluate the AND_to_AFD method of the 'automate' class.
    """

    def setUp(self):
        """
        Setup method called before each test method.
        Prints a message indicating setup for a new test.
        """
        print("\nSetting up for a new test...")

    def tearDown(self):
        """
        Teardown method called after each test method.
        Prints a message indicating completion of a test.
        """
        print("Test completed.")


    def create_automaton_from_csv(self, file_name):
        """
        Helper method to create an automaton from a CSV file.

        Args:
        file_name (str): The file path of the CSV file.

        Returns:
        automate: An instance of the 'automate' class.
        """
        print(f"Creating automaton from {file_name}...")
        return automate(file_name)

    def test_deterministic(self):
        """
        Test case to check the proper conversion of a non-deterministic automaton to deterministic.

        Asserts that certain states ('q0', 'q1', 'q2') are removed and the number of states remains the same after conversion.
        """
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
        """
        Test case to verify if the output automaton is deterministic.

        The test passes if the automaton is deterministic after conversion.
        """
        print("Testing the determinism of the output...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_nondeterminist.csv")
        automaton.display_matrix()
        automaton.AND_to_AFD()
        automaton.display_matrix()
        print("\n")

        # Check if the automaton is deterministic
        if automaton.is_deterministic():
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
