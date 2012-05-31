import core
from core import Word, Batch
from util import *

# Some simple arithmetic words.
class Plus(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 + n1)
core.registerWord('+', Plus())

class Minus(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 - n1)
core.registerWord('-', Minus())

class Multiply(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 * n1)
core.registerWord('*', Multiply())

class Divide(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 / n1)
core.registerWord('/', Divide())

# end simple arithmetic words.

class Dot(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.output.write(str(v))
core.registerWord('.', Dot())

class DotS(Word):
    def execute(self, interp):
        for item in interp.stack.copyOfItems():
            interp.output.write(str(item))
core.registerWord('.S', DotS())

class Dup(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.stack.push(v)
        interp.stack.push(v)
core.registerWord('DUP', Dup())

class Swap(Word):
    def execute(self, interp):
        n1 = self.interp.stack.pop()
        n2 = self.interp.stack.pop()
        self.interp.stack.push(n1)
        self.interp.stack.push(n2)
core.registerWord('SWAP', Swap())

class Drop(Word):
    def execute(self, interp):
        interp.stack.pop()
core.registerWord('DROP', Drop())

class CR(Word):
    def execute(self, interp):
        interp.output.write("\n")
core.registerWord('CR', CR())


# Floating point stuff.
#
class F_Fetch(Word):
    def execute(self, interp):
        # TODO!
        pass
core.registerWord('F@', F_Fetch())

class F_Store(Word):
    def execute(self, interp):
        # TODO!
        pass
core.registerWord('F!', F_Store())

class F_Plus(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2+f1)
core.registerWord('F+', F_Plus())

class F_Minus(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2-f1)
core.registerWord('F-', F_Minus())

class F_Multiply(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2*f1)
core.registerWord('F*', F_Multiply())

class F_Divide(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        f2 = interp.fp_stack.pop()
        interp.fp_stack.push(f2/f1)
core.registerWord('F/', F_Divide())

class F_Dot(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        interp.output.write(str(f1))
core.registerWord('F.', F_Dot())
# end of Floating point stuff.


# DoubleInt stuff
#
class D_Fetch(Word):
    def execute(self, interp):
        # TODO!
        pass
core.registerWord('D@', D_Fetch())

class D_Store(Word):
    def execute(self, interp):
        # TODO!
        pass
core.registerWord('D!', D_Store())

class D_Plus(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d1 + d2
        for i in singleInts(res):
            interp.stack.push(i)
core.registerWord('D+', D_Plus())

class D_Minus(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d2 - d1
        for i in singleInts(res):
            interp.stack.push(i)
core.registerWord('D-', D_Minus())

class D_Multiply(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d1 * d2
        for i in singleInts(res):
            interp.stack.push(i)
core.registerWord('D*', D_Multiply())

class D_Divide(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        d2 = doubleInt(interp.stack.pop(), interp.stack.pop())
        res = d2 / d1
        for i in singleInts(res):
            interp.stack.push(i)
core.registerWord('D/', D_Divide())

class D_Dot(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        interp.output.write(str(d1))
core.registerWord('D.', D_Dot())
# end of DoubleInt stuff.


# Some simple conversion stuff.
class StoD(Word):
    def execute(self, interp):
        interp.stack.push(0)
core.registerWord('S>D', StoD())
class DtoS(Word):
    def execute(self, interp):
        interp.stack.pop()
core.registerWord('D>S', DtoS())
class DtoF(Word):
    def execute(self, interp):
        d1 = doubleInt(interp.stack.pop(), interp.stack.pop())
        f1 = d1+0.0
        interp.fp_stack.push(f1)
core.registerWord('D>F', DtoF())
class FtoD(Word):
    def execute(self, interp):
        f1 = interp.fp_stack.pop()
        d1 = int(f1)
        for i in singleInts(d1):
            interp.stack.push(i)
core.registerWord('F>D', FtoD())
    
# end of Some simple conversion stuff.



# How to define extra words.
#
class DefinedWord(Word):
    def __init__(self, tokensBuffer):
        self.tokensBuffer = tokensBuffer
    def execute(self, interp):
        batch = Batch()
        batch.start(self.tokensBuffer, interp)

class Colon(Word):
    def execute(self, interp):
        # This means that we can't handle nested definitions, but I think that's valid.
        self.tokenBuffer = []
        interp.giveNextTokenTo(self)
    def handleToken(self, token, interp):
        if token == ';':
            name = self.tokenBuffer[0]
            newWord = DefinedWord(self.tokenBuffer[1:])
            interp.addWord(name, newWord)
        else:
            self.tokenBuffer.append(token)
            interp.giveNextTokenTo(self)
core.registerWord(':', Colon())
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
        interp.waitForStdinToken(self)
    def handleToken(self, token, interp):
        currentAddress = interp.memoryHeap.currentAddress()
        allocated = AllocatedAddress(currentAddress)
        interp.dictionary[token] = allocated
core.registerWord('CREATE', CreateWord())

class Here(Word):
    def execute(self, interp):
        interp.stack.push(interp.memoryHeap.currentAddress())
core.registerWord('HERE', Here())

class Alloc(Word):
    def execute(self, interp):
        n = interp.stack.pop()
        interp.memoryHeap.allocate(n)
core.registerWord('ALLOT', Alloc())

class Store(Word):
    def execute(self, interp):
        addr = interp.stack.pop()
        n = interp.stack.pop()
        interp.memoryHeap.store(addr, n)
core.registerWord('!', Store())

class Fetch(Word):
    def execute(self, interp):
        addr = interp.stack.pop()
        v = interp.memoryHeap.fetch(addr)
        interp.stack.push(v)
core.registerWord('@', Fetch())        
# end of Memory stuff


# Comparison
#
class Equals(Word):
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        if (n2 == n1):
            interp.stack.push(-1)
        else:
            interp.stack.push(0)
core.registerWord('=', Equals())
class MoreThan(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        if (n2 > n1):
            interp.stack.push(-1)
        else:
            interp.stack.push(0)
core.registerWord('>', MoreThan())
class LessThan(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        if (n2 < n1):
            interp.stack.push(-1)
        else:
            interp.stack.push(0)
core.registerWord('<', LessThan())
# end of Comparison


# Conditional Stuff
#
class AnonymousIf(Word):
    def __init__(self):
        self.trueItems = []
        self.falseItems = []
        self.inTrueBranch = True
    def execute(self, interp):
        n = interp.stack.pop()
        if n != 0:
            Batch().start(self.trueItems, interp)
        else:
            Batch().start(self.falseItems, interp)
    def handleElse(self):
        self.inTrueBranch = False

    def addToken(self, item):
        if self.inTrueBranch:
            self.trueItems.append(item)
        else:
            self.falseItems.append(item)
    def handleItems(self, items, interp):
        for item in items:
            interp.handleItem(item)

class If(Word):
    def execute(self, interp):
        self.anonymousIf = AnonymousIf()
        self.count = 1
        interp.giveNextTokenTo(self)

    def handleToken(self, token, interp):
        appendToken = True
        claimNextToken = True

        if token == 'THEN':
            self.count -= 1
            if self.count == 0:
                appendToken = False
                # We're done!
                claimNextToken = False
                # Time to execute!
                self.anonymousIf.execute(interp)
        elif token == 'IF':
            self.count += 1
        elif token == 'ELSE':
            if self.count == 1:
                self.anonymousIf.handleElse()
                appendToken = False
        
        if appendToken == True:
            self.anonymousIf.addToken(token)
        if claimNextToken == True:
            interp.giveNextTokenTo(self)
            

    def pop(self, interp):
        obj = self.objects.pop()
        if not self.objects.isEmpty():
            self.objects.top().addItem(obj)
            interp.giveNextTokenTo(self)
        else:
            obj.execute(interp)
    def push(self, obj, interp):
        self.objects.push(obj)
        interp.giveNextTokenTo(self)
    def addToken(self, token, interp):
        self.objects.top().addItem(token)
        interp.giveNextTokenTo(self)


core.registerWord('IF', If())
# end of Conditional