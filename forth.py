

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


# Oh my. Now what?
#
class Interpreter(object):

    def __init__(self):
        self.stack = Stack()

        # A dictionary of known words.
        self.dictionary = {}

        self.dictionary['+'] = Plus()
        self.dictionary['-'] = Minus()
        self.dictionary['*'] = Multiply()
        self.dictionary['/'] = Divide()
        self.dictionary['.'] = Dot()

    def handleWord(self, wordStr):

        if (wordStr in self.dictionary):
            word = self.dictionary[wordStr]
            word.execute(self)
        else:
            # Try this as a number.
            n = int(wordStr)
            # Woohoo! Onto the stack.
            self.stack.push(n)

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
class Minus(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 - n1)
class Multiply(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 * n1)
class Divide(Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 / n1)
# end simple arithmetic words.

class Dot(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.outStream.write(str(v))
        interp.outStream.write('\n')
class Dup(Word):
    def execute(self, interp):
        v = interp.stack.pop()
        interp.stack.push(v)
        interp.stack.push(v)
class Swap(Word):
    def execute(self, interp):
        n1 = self.interp.stack.pop()
        n2 = self.interp.stack.pop()
        self.interp.stack.push(n1)
        self.interp.stack.push(n2)
