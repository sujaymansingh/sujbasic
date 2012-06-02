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
