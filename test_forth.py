from forth import *
import unittest

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

    def testArithmeticWithString(self):
        self.interp.processString('13 3 - 6 * .')
        res = self.interp.output.readline()
        self.assertEquals(res, '60')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
