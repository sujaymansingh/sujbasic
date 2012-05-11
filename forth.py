import sys
import re

MAX_UINT = 4294967296

# This is fairly simple :)
#
class Stack(object):

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def copyOfItems(self):
        result = []
        for item in self.items:
            result.append(item)
        return result
# end Stack



doubleRe = re.compile(r"^\d+\.\d*$")

registeredWords = []
def registerWord(symbol, word):
    registeredWords.append((symbol, word))
# Oh my. Now what?
#
class Interpreter(object):

    def __init__(self):
        # The basic stack...
        self.stack = Stack()

        # We have a separate one for FPs.
        self.fp_stack = Stack()

        # A dictionary of known words.
        self.dictionary = {}

        for (symbol, word) in registeredWords:
            self.dictionary[symbol] = word

        # defaults?
        self.output = sys.stdout
        self.input  = sys.stdin


    def handleWord(self, wordStr):

        if (wordStr in self.dictionary):
            word = self.dictionary[wordStr]
            word.execute(self)
        elif isDoubleInt(wordStr):
            for i in parseDoubleInt(wordStr):
                self.stack.push(i)
        else:
            
            try:
                i = int(wordStr)
                self.stack.push(i)
            except ValueError:
                # Actually, we might have a float...
                f = float(wordStr)
                self.fp_stack.push(f)

    def processString(self, line):

        for word in line.split():
            self.handleWord(word)


# Abstract class
#
class Word(object):
    def execute(self, interp):
        pass
# end Word

# Some simple arithmetic words.
class Plus(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 + n1)
registerWord('+', Plus())

class Minus(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 - n1)
registerWord('-', Minus())

class Multiply(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 * n1)
registerWord('*', Multiply())

class Divide(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 / n1)
registerWord('/', Divide())

# end simple arithmetic words.

class Dot(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.output.write(str(v))
        interp.output.write('\n')
registerWord('.', Dot())

class Dup(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.stack.push(v)
        interp.stack.push(v)
registerWord('DUP', Dup())

class Swap(Word):
    def execute(self, interp):
        n1 = self.interp.stack.pop()
        n2 = self.interp.stack.pop()
        self.interp.stack.push(n1)
        self.interp.stack.push(n2)
registerWord('SWAP', Swap())

class Drop(Word):
    def execute(self, interp):
        self.interp.stack.pop()
registerWord('DROP', Drop())

class CR(Word):
    def execute(self, interp):
        interp.output.write("\n")
registerWord('CR', CR())


# Floating point stuff.
#
class F_Fetch(Word):
    def execute(self, interp):
        # TODO!
        pass
registerWord('F@', F_Fetch())

class F_Store(Word):
    def execute(self, interp):
        # TODO!
        pass
registerWord('F!', F_Store())

class F_Plus(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2+f1)
registerWord('F+', F_Plus())

class F_Minus(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2-f1)
registerWord('F-', F_Minus())

class F_Multiply(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2*f1)
registerWord('F*', F_Multiply())

class F_Divide(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2/f1)
registerWord('F/', F_Divide())

class F_Dot(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        interp.output.write(str(f1))
        interp.output.write("\n")
registerWord('F.', F_Dot())
# end of Floating point stuff.


# DoubleInt stuff
#
def doubleInt(big, small):
    return (big * MAX_UINT) + small

def singleInts(doubleInt):
    big = doubleInt / MAX_UINT
    small = doubleInt - (big*MAX_UINT)
    return (small, big)

def isDoubleInt(wordStr):
    return (doubleRe.match(wordStr) != None)

def parseDoubleInt(wordStr):
    res = ''
    for c in wordStr:
        if c != '.':
            res += c
    return singleInts(int(res))

class D_Fetch(Word):
    def execute(self, interp):
        # TODO!
        pass
registerWord('D@', D_Fetch())

class D_Store(Word):
    def execute(self, interp):
        # TODO!
        pass
registerWord('D!', D_Store())

class D_Plus(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d1 + d2
        for i in singleInts(res):
            interp.stack.push(i)
registerWord('D+', D_Plus())

class D_Minus(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d2 - d1
        for i in singleInts(res):
            interp.stack.push(i)
registerWord('D-', D_Minus())

class D_Multiply(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d1 * d2
        for i in singleInts(res):
            interp.stack.push(i)
registerWord('D*', D_Multiply())

class D_Divide(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d2 / d1
        for i in singleInts(res):
            interp.stack.push(i)
registerWord('D/', D_Divide())

class D_Dot(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        interp.output.write(str(d1))
registerWord('D.', D_Dot())
# end of DoubleInt stuff.
