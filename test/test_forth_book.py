# The idea here is to simply take the book "Starting Forth" by Leo Brodie
# (highly recommended btw) and go through the chapters and make sure that
# all the exercises are supported by my forth intepreter!
#

from forth.core import Interpreter
import util
import unittest
import random


class TestCaseWithInterp(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = util.LineReader()
# end of TestCaseWithInterp


class TestChapter01(TestCaseWithInterp):

    def test01(self):
        self.interp.processString(': GIFT ." BOOKENDS" ;')
        self.interp.processString(': GIVER ." STEPHANIE" ;')
        self.interp.processString(': THANKS ." DEAR " GIVER ." , THANKS FOR THE " GIFT ." ." ;')

        self.interp.processString('THANKS CR')
        line = self.interp.output.readline()
        self.assertEquals(line, "DEAR STEPHANIE, THANKS FOR THE BOOKENDS.")


    def test02(self):
        self.interp.processString(': TEN.LESS -10 + ;')
        self.interp.processString('10 TEN.LESS . CR')
        self.assertEquals(self.interp.output.readline(), '0')

