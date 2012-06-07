# Words for conditional code.
#
import core



# If
#
class If(core.Word):
    """(f -- ) If f is non-zero, run the first branch of code, else run the other."""
    def execute(self, interp):
        self.anonymousIf = AnonymousIf()
        self.count = 1
        interp.giveNextTokenTo(self)

    def handleToken(self, token, interp):
        appendToken    = True
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
            # Must be a nested if statement. Read in as if it was any other
            # token, but we'll have to not process the next else/then.
            self.count += 1
        elif token == 'ELSE':
            if self.count == 1:
                self.anonymousIf.handleElse()
                appendToken = False
        
        if appendToken == True:
            self.anonymousIf.addToken(token)
        if claimNextToken == True:
            interp.giveNextTokenTo(self)
core.registerWord('IF', If())

class AnonymousIf(core.Word):
    def __init__(self):
        self.trueItems = []
        self.falseItems = []
        self.inTrueBranch = True
    def execute(self, interp):
        n = interp.stack.pop()
        if n != 0:
            core.Batch().start(self.trueItems, interp)
        else:
            core.Batch().start(self.falseItems, interp)
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
# end of If


class Equals(core.Word):
    """(n1 n2 -- f) Puts 0 on the stack if n1 and n2 are not equal, puts 1 otherwise"""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        if (n2 == n1):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('=', Equals())


class MoreThan(core.Word):
    """(n1 n2 -- f) Puts 0 on the stack if n1 is more than n2, puts 1 otherwise"""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        if (n1 > n2):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('>', MoreThan())


class LessThan(core.Word):
    """(n1 n2 -- f) Puts 0 on the stack if n1 is less than n2, puts 1 otherwise"""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        if (n1 < n2):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('<', LessThan())


class EqualsZero(core.Word):
    """(n -- f) Puts 1 on the stack if the TOS is zero, 0 otherwise."""
    def execute(self, interp):
        n = interp.stack.pop()
        if (n == 0):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('0=', EqualsZero())


class MoreThanZero(core.Word):
    """(n -- f) Puts 1 on the stack if the TOS > zero, 0 otherwise."""
    def execute(self, interp):
        n = interp.stack.pop()
        if (n > 0):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('0>', MoreThanZero())


class LessThanZero(core.Word):
    """(n -- f) Puts 1 on the stack if the TOS < zero, 0 otherwise."""
    def execute(self, interp):
        n = interp.stack.pop()
        if (n < 0):
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('0<', LessThanZero())


class Not(core.Word):
    """(f -- f) If TOS is 0, put 1 (else put 0). (Essentially same as 0=)"""
    def execute(self, interp):
        n = interp.stack.pop()
        if n == 0:
            interp.stack.push(1)
        else:
            interp.stack.push(0)
core.registerWord('NOT', Not())


class And(core.Word):
    """(n1 n2 -- f) Logical And (Both must be non-zero)."""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        v = 0
        if n1 != 0 and n2 != 0:
            v = 1
        interp.stack.push(v)
core.registerWord('AND', And())


class Or(core.Word):
    """(n1 n2 -- f) Logical Or (At least one must be non-zero)."""
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        v = 0
        if n1 != 0 or n2 != 0:
            v = 1
        interp.stack.push(v)
core.registerWord('OR', Or())


class NonZeroDup(core.Word):
    """(n -- n n) or (0 -- 0) Duplicates only if n is non-zero."""
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n)
        if n != 0:
            interp.stack.push(n)
core.registerWord('?DUP', NonZeroDup())
