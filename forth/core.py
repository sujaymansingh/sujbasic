# Core stuff!
#

from util import *
import re
import sys

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
        self.waitingForStdinToken = None
        self.batches = Stack()
        self.consumeUptoChar = None

        # defaults?
        self.output = sys.stdout
        self.input  = sys.stdin


    def handleItem(self, item):
        if type(item) == str:
            self.handleToken(item)
        elif type(item) == Word:
            item.execute(self)


    def handleToken(self, token):

        if self.waitingForStdinToken != None:
            word = self.waitingForStdinToken
            self.waitingForStdinToken = None
            word.handleToken(token, self)

            # Right, unless we are still waiting on something
            if self.waitingForStdinToken == None and self.batches.isEmpty() == False:
                # Right we were waiting on stdin, now we aren't.
                # We should resume anything we paused.
                self.batches.top().resume(self)
            return

        if self.waitingForToken != None:
            word = self.waitingForToken
            self.waitingForToken = None
            word.handleToken(token, self)
            return

        # Right, nothing is waiting on anything. Execute that damned token.
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

    # Is anything waiting?
    def readyToExecute(self):
        return self.waitingForToken == None

    def giveNextTokenTo(self, word):
        self.waitingForToken = word

    def waitForStdinToken(self, word):
        if not self.batches.isEmpty():
            self.batches.top().pause(self)
        self.waitingForStdinToken = word

    def readUptoAndGiveTo(self, char, handlerWord):
        self.consumeUptoChar = char
        self.consumeHandler  = handlerWord
    def consumeUpto(self):
        return self.consumeUptoChar
    def handleConsumed(self, token):
        word = self.consumeHandler
        self.consumeHandler = None
        self.consumeUptoChar = None
        word.handleToken(token, self)

    def addWord(self, symbol, word):
        self.dictionary[symbol] = word

    def processString(self, line):
        tokens = ForthTokeniser(line)

        while tokens.hasMoreTokens():
            token = tokens.nextToken()
            if (token != ''):
                self.handleToken(token)
# end Interpreter


# Word
#
class Word(object):
    def execute(self, interp):
        pass
    def handleToken(self, token, interp):
        pass
# end Word


# end Batch
#
class Batch(object):
    def start(self, tokens, interp):
        self.currentToken = 0
        self.tokens = tokens
        interp.batches.push(self)
        self.resume(interp)
    def pause(self, interp):
        self.isPaused = True
    def resume(self, interp):
        self.isPaused = False
        while self.currentToken < len(self.tokens):
            interp.handleToken(self.tokens[self.currentToken])
            self.currentToken += 1
            # We might have been paused!
            if self.isPaused == True:
                break
        # Have we reached the end?!
        if self.currentToken <= len(self.tokens):
            interp.batches.pop()
# end Batch
