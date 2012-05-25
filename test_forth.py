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


class TestCaseWithInterp(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()
        self.interp.output = LineReader()


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

    def testArithmeticWithString(self):
        self.interp.processString('13 3 - 6 * . CR')
        res = self.interp.output.readline()
        self.assertEquals(res, '60')


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

    def testSimpleEquality(self):
        self.interp.processString('132 131 = . CR')
        self.assertNotEqual("0", self.interp.output.readline())
        self.interp.processString('131 131 = . CR')
        self.assertEquals("0", self.interp.output.readline())

        self.interp.processString('132 131 > . CR')
        self.assertEquals("0", self.interp.output.readline())
        self.interp.processString('14 20 > . CR')
        self.assertNotEquals("0", self.interp.output.readline())
        self.interp.processString('131 131 > . CR')
        self.assertNotEqual("0", self.interp.output.readline())

        self.interp.processString('132 131 < . CR')
        self.assertNotEquals("0", self.interp.output.readline())
        self.interp.processString('14 20 < . CR')
        self.assertEquals("0", self.interp.output.readline())
        self.interp.processString('131 131 < . CR')
        self.assertNotEqual("0", self.interp.output.readline())

        self.interp.processString('132 131 < . CR')
        self.assertNotEquals("0", self.interp.output.readline())
        self.interp.processString('14 20 < . CR')
        self.assertEquals("0", self.interp.output.readline())
        self.interp.processString('131 131 < . CR')
        self.assertNotEqual("0", self.interp.output.readline())




def main():
    unittest.main()


if __name__ == '__main__':
    main()
