from forth.core import *
from forth.util import *
import util
import unittest
import random


class TestStack(unittest.TestCase):

    def testBasicOps(self):
        stack = Stack()
        self.assertTrue(stack.isEmpty())

        stack.push(10)
        self.assertFalse(stack.isEmpty())

        top1 = stack.top()
        top2 = stack.pop()

        self.assertEquals(10, top1)
        self.assertEquals(10, top2)

        items = [10, '32', 'sujay', Stack()]
        for item in items:
            stack.push(item)

        # reverse order!!
        i = len(items)-1
        while (i >= 0):
            self.assertEquals(items[i], stack.pop())
            i -= 1


class TestQueue(unittest.TestCase):

    def testBasicOps(self):
        queue = Queue()
        self.assertTrue(queue.isEmpty())

        queue.push(10)
        self.assertFalse(queue.isEmpty())

        top1 = queue.top()
        top2 = queue.pop()

        self.assertEquals(10, top1)
        self.assertEquals(10, top2)

        items = [10, '32', 'sujay', Stack()]
        for item in items:
            queue.push(item)

        i = 0
        while (i < len(items)):
            self.assertEquals(items[i], queue.pop())
            i += 1


class TestMemoryHeap(unittest.TestCase):

    def testBasicAlloc(self):
        mh = MemoryHeap()
        addr = mh.currentAddress()
        addr2 = mh.currentAddress()
        # Shouldn't really change!
        self.assertEquals(addr, addr2)

        # Allocate 2 'bytes' to addr
        mh.allocate(2)
        addr2 = mh.currentAddress()
        self.assertEquals(addr+2, addr2)
        mh.store(addr, 13)
        mh.store(addr2, 6757)
        self.assertEquals(mh.fetch(addr), 13)
        self.assertEquals(mh.fetch(addr2), 6757)


class TestTokeniser(unittest.TestCase):

    def checkTokens(self, tokens, tokeniser):
        i = 0
        while tokeniser.hasMoreTokens():
            self.assertEquals(tokens[i], tokeniser.nextToken())
            i += 1

    def testTokensBasic(self):
        line = "Now there are wrinkles  round my      baby's eyes"
        tokeniser = Tokeniser(line)
        tokens = ["Now", "there", "are", "wrinkles", "round", "my", "baby's", "eyes"]
        self.checkTokens(tokens, tokeniser)

        line = "    And she cries herself to sleep at night."
        tokeniser = Tokeniser(line)
        tokens = ["And", "she", "cries", "herself", "to", "sleep", "at", "night."]
        self.checkTokens(tokens, tokeniser)

    def testReadUpto(self):
        line = 'When I come home the house is dark, she sobs "baby did you make it all right?"'
        tokeniser = Tokeniser(line)
        readTokens = []
        token = ''
        while tokeniser.hasMoreTokens() and token != 'sobs':
            token = tokeniser.nextToken()
            readTokens.append(token)

        tokeniser.returnUptoChar('"')
        readTokens.append(tokeniser.returnUptoChar('"'))

        self.assertEquals(readTokens, ['When', 'I', 'come', 'home', 'the', 'house', 'is', 'dark,', 'she', 'sobs', 'baby did you make it all right?'])

            
class TestCaseWithInterp(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = util.LineReader()


class TestInterpAdding(TestCaseWithInterp):

    def testArithmetic(self):
        self.interp.handleToken('5')
        self.interp.handleToken('10')
        self.interp.handleToken('+')
        self.interp.handleToken('.')
        self.interp.handleToken('CR')

        res = self.interp.output.readline()
        self.assertEquals('15', res)

        self.interp.handleToken('15')
        self.interp.handleToken('12')
        self.interp.handleToken('*')
        # Should have 180
        self.interp.handleToken('10')
        self.interp.handleToken('/')
        self.interp.handleToken('.')
        self.interp.handleToken('CR')
        res = self.interp.output.readline()
        self.assertEquals('18', res)

    def testRandomArithmetic(self):
        for i in range(100):
            n1 = random.randint(0, 1000000)
            n2 = random.randint(1, 1000000)
            baseStr = '%d %d %s . CR'
            for (operator, expected) in [('+', n1+n2),('-', n1-n2),('*', n1*n2),('/', n1/n2)]:
                self.interp.processString(baseStr % (n1, n2, operator))
                res = self.interp.output.readline()
                self.assertEquals(str(expected), res)

    def testOneTwo(self):
        for i in range(100):
            r = random.randint(-1000, 1000)
            self.interp.processString('%d 1+ . CR' % (r))
            self.assertEquals(str(r+1), self.interp.output.readline())
            self.interp.processString('%d 1- . CR' % (r))
            self.assertEquals(str(r-1), self.interp.output.readline())
            self.interp.processString('%d 2+ . CR' % (r))
            self.assertEquals(str(r+2), self.interp.output.readline())
            self.interp.processString('%d 2- . CR' % (r))
            self.assertEquals(str(r-2), self.interp.output.readline())

            # If we're dividing, we don't want any zeros.
            while r == 0: r = random.randint(-1000, 1000)
            self.interp.processString('%d 2/ . CR' % (r))
            self.assertEquals(str(r/2), self.interp.output.readline())

    def testMoreArithmetic(self):
        self.interp.processString('-5 ABS . CR')
        self.assertEquals('5', self.interp.output.readline())
        self.interp.processString('8 ABS . CR')
        self.assertEquals('8', self.interp.output.readline())
        self.interp.processString('-5 NEGATE . CR')
        self.assertEquals('5', self.interp.output.readline())
        self.interp.processString('8 NEGATE . CR')
        self.assertEquals('-8', self.interp.output.readline())
        self.interp.processString('2 31 MIN . CR')
        self.assertEquals('2', self.interp.output.readline())
        self.interp.processString('12 -31 MAX . CR')
        self.assertEquals('12', self.interp.output.readline())

    def testArithmeticWithString(self):
        self.interp.processString('13 3 - 6 * . CR')
        res = self.interp.output.readline()
        self.assertEquals(res, '60')

    def testMods(self):
        self.interp.processString('22 4 /MOD . CR . CR')
        self.assertEquals('5', self.interp.output.readline())
        self.assertEquals('2', self.interp.output.readline())
        self.interp.processString('123 17 /MOD . CR . CR')
        self.assertEquals('7', self.interp.output.readline())
        self.assertEquals('4', self.interp.output.readline())

        self.interp.processString('1219 57 MOD . CR')
        self.assertEquals('22', self.interp.output.readline())


class TestStackStuff(TestCaseWithInterp):

    def testStackManipulate(self):
        self.interp.processString('1 5 10')

        self.interp.processString('SWAP')
        self.assertEquals([1, 10, 5], self.interp.stack.copyOfItems())
        self.interp.processString('SWAP')
        self.assertEquals([1, 5, 10], self.interp.stack.copyOfItems())

        self.interp.processString('DUP')
        self.assertEquals([1, 5, 10, 10], self.interp.stack.copyOfItems())
        self.interp.processString('DROP')
        self.assertEquals([1, 5, 10], self.interp.stack.copyOfItems())

        self.interp.processString('ROT')
        self.assertEquals([5, 10, 1], self.interp.stack.copyOfItems())

        self.interp.processString('OVER')
        self.assertEquals([5, 10, 1, 10], self.interp.stack.copyOfItems())


class TestFloatingPoint(TestCaseWithInterp):

    def testRandomArithmetic(self):
        for i in range(100):
            n1 = random.uniform(0, 100.0)
            n2 = random.uniform(0.1, 100.0)
            baseStr = '%.20e %.20e %s F. CR'
            for (operator, expected) in [('F+', n1+n2),('F-', n1-n2),('F*', n1*n2),('F/', n1/n2)]:
                self.interp.processString(baseStr % (n1, n2, operator))

                res = self.interp.output.readline()
                f1 = float(res)
                # Gah, floating point!!!
                diff = abs(f1-expected)
                self.assertTrue(diff < 1e-4)


class TestDouble(TestCaseWithInterp):

    def testParsing(self):
        testCases = []
        testCases.append(('12.', True,  (12, 0)))
        testCases.append(('12',  False, (12, 0)))
        testCases.append(('35.56', True,  (3556, 0)))
        testCases.append(('4294967298.', True,  (2, 1)))
        testCases.append(('3.00000001e1.', False,  (2, 1)))
        for (word, expectedBool, expectedNum) in testCases:
            isDouble = isDoubleInt(word)
            self.assertEquals(isDouble, expectedBool)
            if (isDouble):
                self.assertEquals(parseDoubleInt(word), expectedNum)

    def testSimple(self):
        self.interp.processString('5 2 D. CR')
        res = self.interp.output.readline()
        self.assertEquals(int(res), (2*MAX_UINT)+5)

    def testRandomArithmetic(self):
        for i in range(100):
            # Max uint is 4294967296
            n1 = random.randint(4000000000, 40000000000)
            n2 = random.randint(4000000000, 40000000000)
            baseStr = '%d. %d. %s'
            for (operator, expected) in [('D+', n1+n2),('D-', n1-n2),('D*', n1*n2),('D/', n1/n2)]:
                self.interp.processString(baseStr % (n1, n2, operator))
                self.interp.processString('D. CR')
                res = self.interp.output.readline()
                self.assertEquals(str(expected), res)

    def testStackManipulate(self):
        self.interp.processString('12 13 14 15')
        self.interp.processString('2SWAP')
        self.assertEquals(self.interp.stack.copyOfItems(), [14, 15, 12, 13])

        self.interp.processString('2DUP')
        self.assertEquals(self.interp.stack.copyOfItems(), [14, 15, 12, 13, 12, 13])

        self.interp.processString('2DROP')
        self.assertEquals(self.interp.stack.copyOfItems(), [14, 15, 12, 13])

        self.interp.processString('2OVER')
        self.assertEquals(self.interp.stack.copyOfItems(), [14, 15, 12, 13, 14, 15])




class TestConversion(TestCaseWithInterp):

    def testS_D(self):
        self.interp.processString('5 S>D')
        self.assertEquals([5, 0], self.interp.stack.copyOfItems())
        self.interp.processString('D>S')
        self.assertEquals([5], self.interp.stack.copyOfItems())

        self.interp.processString('S>D D>F')
        self.assertEquals([], self.interp.stack.copyOfItems())
        self.assertEquals([5.0], self.interp.fp_stack.copyOfItems())

        self.interp.processString('F>D')
        self.assertEquals([5, 0], self.interp.stack.copyOfItems())
        self.assertEquals([], self.interp.fp_stack.copyOfItems())

        self.interp.processString('D>S')
        self.assertEquals([5], self.interp.stack.copyOfItems())
        self.assertEquals([], self.interp.fp_stack.copyOfItems())



class TestInterpMemory(TestCaseWithInterp):

    def testMemory(self):
        self.interp.processString('HERE . CR')
        # I don't really know where it will start, but it should be a number.
        addr = int(self.interp.output.readline())

        self.interp.processString('CREATE X')
        self.interp.processString('X . CR')
        addrX = int(self.interp.output.readline())
        self.assertEquals(addr, addrX)

        self.interp.processString('CREATE Y')
        self.interp.processString('Y . CR')
        addrY = int(self.interp.output.readline())
        self.assertEquals(addrX, addrY)

        self.interp.processString('2 ALLOT')
        self.interp.processString('HERE . CR')
        addr = int(self.interp.output.readline())
        self.assertEquals(addrX+2, addr)

        self.interp.processString('137 X !')
        self.interp.processString('X @ . CR')
        self.assertEquals('137', self.interp.output.readline())


class TestEquality(TestCaseWithInterp):

    def checkStackFor(self, boolean):
        val = self.interp.output.readline()
        if boolean == True:
            self.assertNotEqual("0", val)
        else:
            self.assertEqual("0", val)

    def testSimpleEquality(self):
        self.interp.processString('132 131 = . CR')
        self.checkStackFor(False)
        self.interp.processString('131 131 = . CR')
        self.checkStackFor(True)

        self.interp.processString('132 131 > . CR')
        self.checkStackFor(True)
        self.interp.processString('14 20 > . CR')
        self.checkStackFor(False)
        self.interp.processString('131 131 > . CR')
        self.checkStackFor(False)

        self.interp.processString('132 131 < . CR')
        self.checkStackFor(False)
        self.interp.processString('14 20 < . CR')
        self.checkStackFor(True)

        self.interp.processString('131 131 < . CR')
        self.checkStackFor(False)

        self.interp.processString('132 131 < . CR')
        self.checkStackFor(False)
        self.interp.processString('14 20 < . CR')
        self.checkStackFor(True)
        self.interp.processString('131 131 < . CR')
        self.checkStackFor(False)


class TestDecision(TestCaseWithInterp):

    def testSimpleIf(self):
        self.interp.processString('1 IF 15 ELSE 20 THEN . CR')
        self.assertEquals('15', self.interp.output.readline())

    def testNestedIf(self):
        signage = '%d DUP 0 = IF DROP 0 ELSE 0 > IF 1 ELSE -1 THEN THEN . CR'

        self.interp.processString( signage % (0) )
        self.assertEquals("0", self.interp.output.readline())

        for num in [-1, -32, -242424, -9]:
            self.interp.processString( signage % (num,) )
            self.assertEquals("-1", self.interp.output.readline())

    def testZeros(self):
        data = [
            (0, '0=', 1), (133, '0=', 0), (-111, '0=', 0),
            (0, '0<', 0), (133, '0<', 0), (-111, '0<', 1),
            (0, '0>', 0), (133, '0>', 1), (-111, '0>', 0),
            ]
        for item in data:
            self.interp.processString('%d %s . CR' % (item[0], item[1]))
            self.assertEquals(str(item[2]), self.interp.output.readline())

    def testNaryOperators(self):
        data = [
            ('1 NOT', 0), ('2 NOT', 0), ('0 NOT', 1), ('-12 NOT', 0),
            ('0 0 OR', 0), ('1 0 OR', 1), ('0 1 OR', 1), ('1 1 OR', 1), ('1 -1 OR', 1), ('3332 0 OR', 1),
            ('0 0 AND', 0), ('1 0 AND', 0), ('0 1 AND', 0), ('1 1 AND', 1), ('1 -1 AND', 1), ('3332 0 AND', 0),
            ]
        for item in data:
            self.interp.processString('%s . CR' % (item[0]))
            self.assertEquals(str(item[1]), self.interp.output.readline())

        self.interp.processString('0 ?DUP')
        # Shouldn't have duplicated, so the only thing still on the stack should be the original 0.
        self.assertEquals(self.interp.stack.copyOfItems(), [0])

        self.interp.processString('DROP 1 ?DUP -1 ?DUP')
        self.assertEquals(self.interp.stack.copyOfItems(), [1, 1, -1, -1])




def main():
    unittest.main()


if __name__ == '__main__':
    main()
