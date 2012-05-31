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
