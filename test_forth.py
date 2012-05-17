from forth import *
import unittest
import random

class LineReader(object):

    def __init__(self):
        self.lines = []
        self.buffer = ''

    def write(self, s):
        for c in s:
            if (c == '\n'):
                self.lines.append(self.buffer)
                self.buffer = ''
            else:
                self.buffer = self.buffer + c

    def readline(self):
        line = self.lines[0]
        self.lines = self.lines[1:]
        return line


class TestStack(unittest.TestCase):

    def testBasicOps(self):
        stack = Stack()
        stack.push(10)
        top = stack.pop()
        self.assertEquals(10, top)

        items = [10, '32', 'sujay', Stack()]
        for item in items:
            stack.push(item)

        # reverse order!!
        i = len(items)-1
        while (i >= 0):
            self.assertEquals(items[i], stack.pop())
            i -= 1

class TestCaseWithInterp(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = LineReader()
    


class TestInterpAdding(TestCaseWithInterp):

    def testArithmetic(self):
        self.interp.handleWord('5')
        self.interp.handleWord('10')
        self.interp.handleWord('+')
        self.interp.handleWord('.')

        res = self.interp.output.readline()
        self.assertEquals('15', res)

        self.interp.handleWord('15')
        self.interp.handleWord('12')
        self.interp.handleWord('*')
        # Should have 180
        self.interp.handleWord('10')
        self.interp.handleWord('/')
        self.interp.handleWord('.')
        res = self.interp.output.readline()
        self.assertEquals('18', res)

    def testRandomArithmetic(self):
        for i in range(100):
            n1 = random.randint(0, 1000000)
            n2 = random.randint(1, 1000000)
            baseStr = '%d %d %s .'
            for (operator, expected) in [('+', n1+n2),('-', n1-n2),('*', n1*n2),('/', n1/n2)]:
                self.interp.processString(baseStr % (n1, n2, operator))
                res = self.interp.output.readline()
                self.assertEquals(str(expected), res)

    def testArithmeticWithString(self):
        self.interp.processString('13 3 - 6 * .')
        res = self.interp.output.readline()
        self.assertEquals(res, '60')


class TestFloatingPoint(TestCaseWithInterp):

    def testRandomArithmetic(self):
        for i in range(100):
            n1 = random.uniform(0, 100.0)
            n2 = random.uniform(0.1, 100.0)
            baseStr = '%.20e %.20e %s F.'
            for (operator, expected) in [('F+', n1+n2),('F-', n1-n2),('F*', n1*n2),('F/', n1/n2)]:
                self.interp.processString(baseStr % (n1, n2, operator))

                res = self.interp.output.readline()
                f1 = float(res)
                # Gah, floating point!!!
                diff = abs(f1-expected)
                self.assertTrue(diff < 1e-4)


class TestDoubleInts(TestCaseWithInterp):

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




def main():
    unittest.main()


if __name__ == '__main__':
    main()
