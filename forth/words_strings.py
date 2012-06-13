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
        address = interp.memoryHeap.currentAddress()
        startAddress = address
        interp.memoryHeap.allocate(len(token))

        for c in token:
            interp.memoryHeap.store(address, ord(c))
            address += 1

        interp.stack.push(startAddress)
        interp.stack.push(len(token))
core.registerWord('S"', StoreLiteral())


# Type out...
#
class Type(core.Word):
    """(addr n -- ) Types out n bytes from addr"""
    def execute(self, interp):
        n = interp.stack.pop()
        addr = interp.stack.pop()
        i = 0
        while i < n:
            char = chr(interp.memoryHeap.fetch(addr + i))
            interp.output.write(char)
            i += 1 
core.registerWord('TYPE', Type())
