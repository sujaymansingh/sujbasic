# Simple stuff.
#
import core
from core import Word, Batch
from util import *


class CR(Word):
    """( -- ) Simply print out a carriage return."""
    def execute(self, interp):
        interp.output.write('\n')
core.registerWord('CR', CR())


class Spaces(Word):
    """(n -- ) Print out n spaces."""
    def execute(self, interp):
        n = interp.stack.pop()
        for i in range(n):
            interp.output.write(' ')
core.registerWord('SPACES', Spaces())


class Space(Word):
    """( -- ) Print out just one space."""
    def execute(self, interp):
        interp.output.write(' ')
core.registerWord('SPACE', Space())


class Emit(Word):
    """(c -- ) Emit the character from the stack."""
    def execute(self, interp):
        n = interp.stack.pop()
        interp.output.write(chr(n))
core.registerWord('EMIT', Emit())


class Swap(Word):
    """(n1 n2 -- n2 n1) Swap the top pair of the stack."""
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n1)
        interp.stack.push(n2)
core.registerWord('SWAP', Swap())


class Dup(Word):
    """(n -- n n) Duplicate the top of the stack."""
    def execute(self, interp):
        v = interp.stack.pop()
        interp.stack.push(v)
        interp.stack.push(v)
core.registerWord('DUP', Dup())


class Over(Word):
    """(n1 n2 -- n1 n2 n1) Duplicate the 2nd top item and then on the top."""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        for n in [n1, n2, n1]:
            interp.stack.push(n)
core.registerWord('OVER', Over())


class Rot(Word):
    """(n1 n2 n3 -- n2 n3 n1) Rotate the top 3 items."""
    def execute(self, interp):
        n3 = interp.stack.pop()
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        for n in [n2, n3, n1]:
            interp.stack.push(n)
core.registerWord('ROT', Rot())


class Drop(Word):
    """(n -- ) Discard the top of the stack."""
    def execute(self, interp):
        interp.stack.pop()
core.registerWord('DROP', Drop())


class Dot(Word):
    """(n -- ) Prints the top item of the stack."""
    def execute(self, interp):
        v = interp.stack.pop()
        interp.output.write(str(v))
core.registerWord('.', Dot())


class DotS(Word):
    """( -- ) Prints all items on the stack."""
    def execute(self, interp):
        for item in interp.stack.copyOfItems():
            interp.output.write(str(item))
core.registerWord('.S', DotS())


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
        interp.addWord(token, allocated)
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


class Abort(Word):
    """(f -- ) If the flag is true, print out the last word executed and then clear the stack."""
    def execute(self, interp):
        # TODO
        pass
core.registerWord('ABORT"', Abort())


class CheckStackUnderflow(Word):
    """( -- f) Returns true if a stack underflow condition has occurred."""
    def execute(self, interp):
        # TODO
        pass
core.registerWord('?STACK', CheckStackUnderflow())


class Bye(Word):
    """( -- ) Simply stop the interpreter."""
    def execute(self, interp):
        interp.exitFlag = True
core.registerWord('BYE', Bye())
