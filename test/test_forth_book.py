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

    def test02(self):
        self.interp.processString(': REVERSE.TOP.4 SWAP 2SWAP SWAP ;')
        self.interp.processString('10 20 30 40 REVERSE.TOP.4')
        self.assertEquals([40, 30, 20, 10], self.interp.stack.copyOfItems())
        self.interp.processString('2DROP 2DROP')

        self.interp.processString(': 3DUP DUP 2OVER ROT ;')
        self.interp.processString('10 20 30 3DUP')
        self.assertEquals([10, 20, 30, 10, 20, 30], self.interp.stack.copyOfItems())
        self.interp.processString('2DROP 2DROP 2DROP')

        # aa + ab + c  using  (a b c -- result)
        a = 2; b = 3; c = 4; res = (a*a) + (a*b) + c
        self.interp.processString(': QUADR SWAP ROT DUP DUP * ROT ROT * + + ;')
        self.interp.processString('%d %d %d QUADR . CR' % (a, b, c))
        self.assertEquals(str(res), self.interp.output.readline())

        self.interp.processString(': CONVICTED-OF 0 ;')
        self.interp.processString(': HOMICIDE   20 + ;')
        self.interp.processString(': ARSON      10 + ;')
        self.interp.processString(': BOOKMAKING  2 + ;')
        self.interp.processString(': TAX-EVASION 5 + ;')
        self.interp.processString(': WILL-SERVE . ." YEARS" ;')
        self.interp.processString('CONVICTED-OF ARSON HOMICIDE TAX-EVASION WILL-SERVE CR')
        self.assertEquals('35YEARS', self.interp.output.readline())

        self.interp.processString(': EGG.CARTONS 12 /MOD . ."  CARTONS AND " . ."  EGGS" ;')
        self.interp.processString('148 EGG.CARTONS CR')
        self.assertEquals('12 CARTONS AND 4 EGGS', self.interp.output.readline())
# end of Chapter02


class Chapter04(TestCaseWithInterp):

    def test01(self):
        for item in [(1, '1'), (0, '0'), (200, '1')]:
            num, expected = item
            self.interp.processString('%d 0= NOT . CR' % num)
            self.assertEquals(expected, self.interp.output.readline())

        # artichoke

        self.interp.processString(': CARD 18 < IF ." UNDER AGE" ELSE ." ALCOHOLIC BEVERAGES PERMITTED" THEN ;')
        for i in range(1, 100):
            age = random.randint(10, 80)
            self.interp.processString('%d CARD CR' % (age))
            expected = 'UNDER AGE' if age < 18 else 'ALCOHOLIC BEVERAGES PERMITTED'
            self.assertEquals(expected, self.interp.output.readline())

        self.interp.processString(': SIGN.TEST DUP 0 = IF DROP ." ZERO" ELSE 0 > IF ." POSITIVE" ELSE ." NEGATIVE" THEN THEN ;')
        for item in [(1, 'POSITIVE'), (0, 'ZERO'), (-44, 'NEGATIVE'), (12, 'POSITIVE'), (-1, 'NEGATIVE')]:
            num, expected = item
            self.interp.processString('%d SIGN.TEST CR' % num)
            self.assertEquals(expected, self.interp.output.readline())

        # TODO: STARS (I'll need to implement a loop first.)

        # WITHIN (n low-limit high-limit -- ) Puts a true flag if low-limit <= n < high-limit, but a false flag if not.
        self.interp.processString(': WITHIN ROT DUP ROT < IF SWAP < IF 0 ELSE 1 THEN ELSE DROP DROP 0 THEN ;')
        for item in [('6 4 8', '1'), ('3 4 8', '0'), ('9 4 8', '0')]:
            numbers, expected = item
            self.interp.processString('%s WITHIN . CR' % (numbers))
            self.assertEquals(expected, self.interp.output.readline())


class Chapter05(TestCaseWithInterp):

    def testReturnStackSimple(self):
        self.interp.processString(': QUADRATIC >R SWAP ROT I * + R> * + ;')
        self.interp.processString('2 7 9 3 QUADRATIC . CR')
        self.assertEquals('48', self.interp.output.readline())

                                                                                                                                                                                                                                                                                                                                                                
            

# end of Chapter04
