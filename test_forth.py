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


class TestInterpAdding(unittest.TestCase):

    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = LineReader()

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


class TestFloatingPoint(unittest.TestCase):

    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = LineReader()

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
            



def main():
    unittest.main()


if __name__ == '__main__':
    main()
