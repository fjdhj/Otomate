import unittest
from automate import automate  # Import the automate class

class TestAutomateTrim(unittest.TestCase):
    """
    A test suite for testing the 'trim' method in the 'automate' class.

    This class contains several test cases to evaluate the functionality of
    trimming inaccessible and uncoaccessible states from an automaton.
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

    def test_trim_inaccessible_states(self):
        """
        Test case for trimming inaccessible states from an automaton.

        Asserts that an inaccessible state ('q4') is removed after trimming.
        """
        print("Testing trim method for inaccessible states...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_inaccessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertNotIn('q4', automaton.all_states, msg="'q4' should be removed as it is inaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")


    def test_trim_uncoaccessible_states(self):
        """
        Test case for trimming uncoaccessible states from an automaton.

        Asserts that an uncoaccessible state ('q3') is removed after trimming.
        """
        print("Testing trim method for uncoaccessible states...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_uncoaccessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertNotIn('q3', automaton.all_states, msg="'q3' should be removed as it is uncoaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")

    def test_trim_fully_accessible_coaccessible(self):
        """
        Test case for verifying that no states are trimmed when all states are accessible and coaccessible.

        Asserts that no states are removed in this scenario.
        """
        print("Testing trim method for a fully accessible and coaccessible automaton...")
        automaton = self.create_automaton_from_csv("UNITTESTS/automaton_fully_accessible.csv")
        automaton.display_matrix()
        automaton.trim()
        self.assertEqual(len(automaton.all_states), 3, msg="No states should be removed as all are accessible and coaccessible")
        print("\n")
        automaton.display_matrix()
        print("\n")

    def test_trim_empty_automaton(self):
        """
        Test case for trimming an empty automaton.

        Asserts that the automaton remains empty after trimming.
        """
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
