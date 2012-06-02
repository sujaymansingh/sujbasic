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


class Chapter01(TestCaseWithInterp):

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
# end of Chapter01


class Chapter02(TestCaseWithInterp):

    def test01(self):
        self.interp.processString('1 5 10')
        self.interp.processString('SWAP ROT')
        self.assertEquals([10, 5, 1], self.interp.stack.copyOfItems())
        self.interp.processString('DROP DROP DROP')

        self.interp.processString('1 5 10')
        self.interp.processString('SWAP DUP ROT SWAP')
        self.assertEquals([1, 5, 10, 5], self.interp.stack.copyOfItems())
        self.interp.processString('DROP DROP DROP DROP')

        self.interp.processString(': <ROT ROT ROT ;')
        self.interp.processString('1 5 10')
        self.interp.processString('<ROT')
        self.assertEquals([10, 1, 5], self.interp.stack.copyOfItems())
        self.interp.processString('DROP DROP DROP')

        # (n+1) / n  using  (n -- result)
        self.interp.processString(': 2C4 DUP 1 + SWAP / ;')
        n = 29; res = (n+1)/n
        self.interp.processString('%d 2C4 . CR' % (n))
        self.assertEquals(str(res), self.interp.output.readline())

        # x(7x + 5)  using  (x -- result)
        self.interp.processString(': 2C5 DUP 7 * 5 + * ;')
        x = 56; res = x * ((x*7) + 5)
        self.interp.processString('%d 2C5 . CR' % (x))
        self.assertEquals(str(res), self.interp.output.readline())
        
        # 9a^2 - ba  using  (a b -- result)
        a = 102; b = 71; res = (9*a*a) - (b*a)
        self.interp.processString(': 2C6 SWAP DUP DUP * 9 * ROT ROT * - ;')
        # Book used : 2C6 OVER 9 * SWAP - * ;
        self.interp.processString('%d %d 2C6 . CR' % (a,b))
        self.assertEquals(str(res), self.interp.output.readline())
