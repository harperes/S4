import unittest
import S4

class TestSetMethods(unittest.TestCase):

    def testSetNumG(self):
        S = S4.Simulation()
        S.CreateNew()
        S.SetNumG(81)
        x = S.GetNumG()
        self.assertEqual(x, 81)
