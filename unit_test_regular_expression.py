import unittest
from automate import automate  # Import the automate class
from expression import expression

class TestAutomateRegularExpression(unittest.TestCase):

    expressionList = [
        #e1 : (a + b)c * q0 + bc * q0
        (expression(None, False, None, [ expression(True, False, None, [0, expression(False, False, None, [1])]), expression(True, False, 0, [2]), expression(False, False, 0, [1, 2]) ]), 1, "_[ *[ 0 +[ 1 ] ] *q0[ 2 ] ]"),
        
        #e2 : abc * q0
        (expression(None, False, 0, [0,1,2]), 1, "_q0[ 0 1 2 ]"),
        
        #e3 : ab * q0 + c * q0
        (expression(None, False, 0, [0,1, expression(False, False, 0, [2])]), 1, "_[ *q0[ 0 1 +[ 2 ] ] ]"),
        
        #e4 : ab * q0 + c * q1
        (expression(None, False, 0, [0,1, expression(False, False, 1, [2])]), 2, "_q0[ 0 1 +q1[ 2 ] ]"),
        
        #e5 : (a + b)^ * q0 + c * q0 -> ( (a + b)^ + c )q0
        (expression(None, False, None, [expression(True, True, 0, [0, expression(False, False, None, [1]) ]), expression(False, False, 0, [2]) ]), 1, "_[ *q0[ *^[ 0 +[ 1 ] ] +[ 2 ] ] ]"),
        
        #e6 : (a + b) * q0 + c * q0 -> ( (a + b + c )q0
        (expression(None, False, None, [expression(True, False, 0, [0, expression(False, False, None, [1]) ]), expression(False, False, 0, [2]) ]), 1, "_[ *q0[ 0 +[ 1 ] +[ 2 ] ] ]"),
        
        #e7 : abc * q0 + ab * q0
        (expression(None, False, 0, [0,1,2, expression(False, False, 0, [0, 1])]), 1, "_[ 0 1 *q0[ 2 +[ -1 ] ] ]"),
        
        #e8 : abc * q0 + abd * q0
        (expression(None, False, 0, [0,1,2, expression(False, False, 0, [0, 1, 3])]), 1, "_[ 0 1 *q0[ 2 +[ 3 ] ] ]")
    ]

    automateFiles = [
        ("Sample/Final_tests/sample8_2.csv", "_[ *^[ 0 *^[ 1 ] *[ 0 ] ] *[ 0 *^[ 1 ] ] ]"),
        ("Sample/Final_tests/sample8_1.csv", "_[ *^[ 0 1 2 +[ 3 *[ 4 1 2 +[ 5 ] ] ] ] *[ 0 +[ 3 4 ] ] *[ 2 ] ]"),
        ("Sample/Final_tests/evenNb0.csv", "_[ *^[ 0 *^[ 1 ] *[ 0 ] +[ 1 ] ] ]"),
        ("Sample/Final_tests/oddNb0.csv", "_[ *^[ 0 *^[ 1 ] *[ 0 ] +[ 1 ] ] *[ 0 *^[ 1 ] ] ]"),
        ("Sample/Final_tests/tourniquet.csv", "_[ *^[ *[ 0 *^[ 0 ] +[ -1 ] ] *[ 1 ] ] ]"),
        ("Sample/Final_tests/tourniquetInverse.csv", "_[ *^[ *[ 0 *^[ 0 ] +[ -1 ] ] *[ 1 ] ] *[ 0 *^[ 0 ] ] ]")
    ]

    def setUp(self):
        print("\nSetting up for a new test...")

    def tearDown(self):
        print("Test completed.")

    def test_factoryze(self):
        print("Testing Expression Factoryze ...")
        for test in self.expressionList:
            print("Testing expression", test[0])
            test[0].factorize(test[1])
            print("Result :", test[0])
            self.assertEqual(repr(test[0]), test[2], "The result is "+repr(test[0])+"\n   but shold be  "+test[2])

    def test_get_regular_expression(self):
        print("Testing Expression Factoryze ...")
        for test in self.automateFiles:
            print("Testing file", test[0])
            res = automate(test[0]).get_regular_expression()
            print("Result :", res)
            self.assertEqual(repr(res), test[1], "The result is "+repr(res)+"\n   but shold be  "+test[1])


# Run the tests
if __name__ == '__main__':
    unittest.main()
