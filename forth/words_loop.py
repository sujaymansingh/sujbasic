# Words for loops.
#
import core

loopBodies = core.Stack()

#
#
class Do(core.Word):
    """(n1 n2 -- ) ..."""
    def execute(self, interp):
        # We've started a new loop body.
        loopBodies.push([])
        self.count = 1

        index = interp.stack.pop()
        limit = interp.stack.pop()

        interp.return_stack.push(limit)
        interp.return_stack.push(index)

        interp.giveNextTokenTo(self)

    def handleToken(self, token, interp):
        claimNextToken = True

        if token == 'LOOP' or token == '+LOOP':
            self.count -= 1
            if self.count == 0:
                claimNextToken = False
        elif token == 'DO':
            self.count += 1

        loopBodies.top().append(token)

        if claimNextToken == True:
            interp.giveNextTokenTo(self)
        else:
            # In Forth, the loop always runs once!
            core.Batch().start(loopBodies.top(), interp)
core.registerWord('DO', Do())


def isLoopFinished(limit, index, interp):
    if index >= limit:
        # We're done!
        loopBodies.pop()
        result = None
    else:
        # Add the items and batch.
        # Oh no, we're not done. Rebatch!
        result = loopBodies.top()
    return result
 
#
#
class Loop(core.Word):
    """(n? -- ) ..."""

    def __init__(self, readStepFromStack=False):
        self.readStepFromStack = readStepFromStack
        
    def execute(self, interp):
        index = interp.return_stack.pop()
        limit = interp.return_stack.pop()

        if self.readStepFromStack:
            step = interp.stack.pop()
        else:
            step = 1

        index += step

        tokensToRun = isLoopFinished(limit, index, interp)
        if tokensToRun != None:
            interp.return_stack.push(limit)
            interp.return_stack.push(index)
            core.Batch().start(tokensToRun, interp)
core.registerWord('LOOP', Loop())
core.registerWord('+LOOP', Loop(readStepFromStack=True))
