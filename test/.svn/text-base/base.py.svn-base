
__author__="jeffrey"
__date__ ="$Mar 8, 2009 11:30:28 AM$"

import unittest

class BaseFileTest(unittest.TestCase):

    def setUp(self):
        infile = file(self.url+'.html', 'r')
        self.content = infile.read()
        infile.close()
