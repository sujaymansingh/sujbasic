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


    def _handleToken(self, token, fromInternal=False):
        # Has something claimed the token in advance?
        if (self.waitingForExternalToken != None):
            if fromInternal == True:
                # Right, if this is from an internal source (i.e. not the main input) then we simply have to wait
                # until the waiting word gets the token it wants from the main input.
                self.tokenQueue.push(token)
                return
            else:
                # Aha, we have a token. Now nothing should be waiting for the token.
                waitingWord = self.waitingForToken

                # We clear the waitingForToken variable here before passing it to the waitingWord because, as part
                # of its handling of the token, the waitingWord could demand another token! (The greedy swine.)
                self.waitingForToken = None

                # Pass the fresh token to the word that was waiting on it. Note that it could ask for the next token!
                waitingWord.handleToken(token, self)
                self.processTokenQueue()
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

    def addWord(self, symbol, word):
        self.dictionary[symbol] = word

    def processString(self, line):
        for token in line.split():
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
