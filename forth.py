import sys
import re
import traceback

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

    def isEmpty(self):
        return len(self.items) == 0

    def top(self):
        return self.items[len(self.items)-1]
# end Stack


# This is also fairly simple :)
#
class Queue(object):

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        head = self.items[0]
        self.items = self.items[1:]
        return head

    def copyOfItems(self):
        result = []
        for item in self.items:
            result.append(item)
        return result

    def isEmpty(self):
        return len(self.items) == 0

    def top(self):
        return self.items[0]
# end Queue


# Less simple.
#
class MemoryHeap(object):

    def __init__(self):
        self.current = 0
        self.data = {}

    def currentAddress(self):
        return self.current

    def allocate(self, size):
        self.current += size

    def store(self, address, value):
        self.data[address] = value

    def fetch(self, address):
        return self.data[address]
# end MemoryHeap


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

        # We can't use the stack for everything.
        self.memoryHeap = MemoryHeap()

        # A dictionary of known words.
        self.dictionary = {}

        for (symbol, word) in registeredWords:
            self.dictionary[symbol] = word

        self.wordHandlers = Stack()

        # Is there anything waiting on the next token?
        self.waitingForToken = None
        self.tokenQueue = Queue()

        # defaults?
        self.output = sys.stdout
        self.input  = sys.stdin

    def handleToken(self, token, fromInternal=False):
        
        if (self.waitingForToken != None):
            if fromInternal == True:
                self.tokenQueue.push(token)
                return
            else:
                waitingWord = self.waitingForToken
                self.waitingForToken = None
                waitingWord.handleToken(token, self)
                self.processTokenQueue()
                return

        if (token in self.dictionary):
            word = self.dictionary[token]
            word.execute(self)
        elif isDoubleInt(token):
            for i in parseDoubleInt(token):
                self.stack.push(i)
        else:
            
            try:
                i = int(token)
                self.stack.push(i)
            except ValueError:
                # Actually, we might have a float...
                f = float(token)
                self.fp_stack.push(f)

    def readyToExecute(self):
        return self.waitingForToken == None

    def processTokenQueue(self):
        while not self.tokenQueue.isEmpty():
            token = self.tokenQueue.pop()
            self.handleToken(token, True)

            # This token may have put us in a state where we can't continue. How rude.
            if not self.readyToExecute():
                break

    def waitForToken(self, word):
        self.waitingForToken = word

    def addWord(self, symbol, word):
        self.dictionary[symbol] = word

    def processString(self, line):
        for token in line.split():
            self.handleToken(token)
# end Interpreter


# Abstract class
#
class Word(object):
    def execute(self, interp):
        pass
    def handleToken(self, token, interp):
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
registerWord('.', Dot())

class DotS(Word):
    def execute(self, interp):
        for item in interp.stack.copyOfItems():
            interp.output.write(str(item))
registerWord('.S', DotS())

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


# Some simple conversion stuff.
class StoD(Word):
    def execute(self, interp):
        interp.stack.push(0)
registerWord('S>D', StoD())
class DtoS(Word):
    def execute(self, interp):
        interp.stack.pop()
registerWord('D>S', DtoS())
class DtoF(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        f1 = d1+0.0
        interp.fp_stack.push(f1)
registerWord('D>F', DtoF())
class FtoD(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        d1 = int(f1)
        for i in singleInts(d1):
            interp.stack.push(i)
registerWord('F>D', FtoD())
    
# end of Some simple conversion stuff.



# How to define extra words.
#
class DefinedWord(Word):
    def __init__(self, wordsBuffer):
        self.wordsBuffer = wordsBuffer
    def execute(self, interp):
        for token in self.wordsBuffer:
            interp.handleToken(token, True)

class Colon(Word):
    def execute(self, interp):
        # This means that we can't handle nested definitions, but I think that's valid.
        self.tokenBuffer = []
        interp.waitForToken(self)
    def handleToken(self, token, interp):
        if token == ';':
            name = self.tokenBuffer[0]
            newWord = DefinedWord(self.tokenBuffer[1:])
            interp.addWord(name, newWord)
        else:
            self.tokenBuffer.append(token)
            interp.waitForToken(self)
registerWord(':', Colon())
# end of How to define extra words.


# Memory stuff
#
class AllocatedAddress(Word):
    def __init__(self, address):
        self.address = address
    def execute(self, interp):
        interp.stack.push(self.address)

class CreateWord(Word):
    def execute(self, interp):
        interp.waitForToken(self)
    def handleToken(self, token, interp):
        currentAddress = interp.memoryHeap.currentAddress()
        allocated = AllocatedAddress(currentAddress)
        interp.dictionary[token] = allocated
registerWord('CREATE', CreateWord())

class Here(Word):
    def execute(self, interp):
        interp.stack.push(interp.memoryHeap.currentAddress())
registerWord('HERE', Here())

class Alloc(Word):
    def execute(self, interp):
        n = interp.stack.pop()
        interp.memoryHeap.allocate(n)
registerWord('ALLOT', Alloc())

class Store(Word):
    def execute(self, interp):
        addr = interp.stack.pop()
        n = interp.stack.pop()
        interp.memoryHeap.store(addr, n)
registerWord('!', Store())

class Fetch(Word):
    def execute(self, interp):
        addr = interp.stack.pop()
        v = interp.memoryHeap.fetch(addr)
        interp.stack.push(v)
registerWord('@', Fetch())        
# end of Memory stuff


if __name__ == '__main__':

    interp = Interpreter()

    keepGoing = True

    while keepGoing:
        try:
            line = raw_input('forth> ')
            try:
                interp.processString(line)
                interp.output.write(" ok\n")
            except Exception as e:
                print 'Encountered erroe ',e
                traceback.print_exc(file=sys.stdout)
        except EOFError:
            keepGoing = False
