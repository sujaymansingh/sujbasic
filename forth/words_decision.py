# Words for conditional code.
#
import core



# If
#
class If(core.Word):
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
