import re

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
# end of Stack


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
# end of Queue


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
# end of MemoryHeap


#
#
class CharType(object):
    def matches(self):
        pass
class SpecificChar(CharType):
    def __init__(self, char):
        self.char = char
    def matches(self, char):
        return char == self.char
class WhiteSpace(CharType):
    def matches(self, char):
        return char == ' ' or char == '\t'
class NonWhiteSpace(CharType):
    def matches(self, char):
        return char != ' ' and char != '\t'
class Quote(CharType):
    def matches(self, char):
        return char == '"'

class Tokeniser(object):

    def __init__(self, line):
        self.line = line
        self.position = 0

    # Read upto (but not including!!) the char(type)
    def readUpto(self, charType):
        if self.eof():
            return
        c = self.line[self.position]
        while not charType.matches(c):
            self.position += 1
            if self.eof():
                break
            c = self.line[self.position]

    def eof(self):
        return self.position >= len(self.line)

    def hasMoreTokens(self):
        return not self.eof()

    def nextToken(self):
        self.readUpto(NonWhiteSpace())
        start = self.position
        self.readUpto(WhiteSpace())
        end = self.position
        result = self.line[start:end]

        # Right, as a courtesy, read all the way up to the next potential token.
        # This way if the string ends with a string of spaces, we won't get that returned as a token.
        self.readUpto(NonWhiteSpace())
        return result

    def returnUptoChar(self, char):
        start = self.position
        self.readUpto(SpecificChar(char))
        end = self.position

        result = self.line[start:end]

        # Now, we want to 'consume' the char we were supposed to read upto.
        # But not actually return it as part of the result. So unless we are
        # at the end of the string, the next char is the one we read upto.
        if not self.eof():
            self.position += 1

        return result
        

#

MAX_UINT = 4294967296
doubleRe = re.compile(r"^\d+\.\d*$")

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
