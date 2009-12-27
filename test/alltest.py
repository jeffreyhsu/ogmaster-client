# -*- coding:utf-8 -*-
import unittest

from TestParser import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestParseGalaxy))
    return suite

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(suite())
    unittest.TextTestRunner(verbosity=2).run(suite)