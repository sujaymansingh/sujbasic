# How to handle strings. Yeesh.
#

import core

# Literals
# I.e. be able to do stuff like: ." Hello, World "
#
class PrintLiteral(core.Word):
    def execute(self, interp):
        interp.giveNextTokenTo(self)

    def handleToken(self, token, interp):
        interp.output.write(token)
core.registerWord('."', PrintLiteral())


# Store the literal.
#
class StoreLiteral(core.Word):
    def execute(self, interp):
        interp.giveNextTokenTo(self)

    def handleToken(self, token, interp):
        store(token, interp)
core.registerWord('S"', StoreLiteral())


# Type out...
#
class Type(core.Word):
    """(addr n -- ) Types out n bytes from addr"""
    def execute(self, interp):
        interp.output.write(fetch(interp))
core.registerWord('TYPE', Type())


# String concatenation.
#
class StringConcat(core.Word):
    """(addr1 u1 addr2 u2 -- ) Concats the two strings, then push the result back on the stack."""
    def execute(self, interp):
        string2 = fetch(interp)
        string1 = fetch(interp)
        store(string1 + string2, interp)
core.registerWord('S+', StringConcat())


def store(string, interp):
    address = interp.memoryHeap.currentAddress()
    startAddress = address
    interp.memoryHeap.allocate(len(string))
    
    for c in string:
        interp.memoryHeap.store(address, ord(c))
        address += 1
    
    interp.stack.push(startAddress)
    interp.stack.push(len(string))


def fetch(interp):
    u    = interp.stack.pop()
    addr = interp.stack.pop()
    i = 0
    string = ''
    while i < u:
        char = chr(interp.memoryHeap.fetch(addr + i))
        string += char
        i += 1
    return string
