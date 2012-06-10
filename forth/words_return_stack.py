# Dealing with the return stack.
#

import core


class OntoReturn(core.Word):
    """(n -- ) Move an item from the top of the parameter stack to the return stack."""
    def execute(self, interp):
        n = interp.stack.pop()
        interp.return_stack.push(n)
core.registerWord('>R', OntoReturn())


class FromReturn(core.Word):
    """( -- n) Move an item from the top of the return stack to the parameter stack."""
    def execute(self, interp):
        n = interp.return_stack.pop()
        interp.stack.push(n)
core.registerWord('R>', FromReturn())


class CopyFirst(core.Word):
    """( -- n) Copy the first item from the return stack onto the parameter stack."""
    def execute(self, interp):
        items = interp.return_stack.copyOfItems()
        n = interp.stack.push(items[-1])
core.registerWord('I', CopyFirst())


class CopySecond(core.Word):
    """( -- n) Copy the second item from the return stack onto the parameter stack."""
    def execute(self, interp):
        items = interp.return_stack.copyOfItems()
        n = interp.stack.push(items[-2])
core.registerWord("I'", CopySecond())


class CopyThird(core.Word):
    """( -- n) Copy the third item from the return stack onto the parameter stack."""
    def execute(self, interp):
        items = interp.return_stack.copyOfItems()
        n = interp.stack.push(items[-3])
core.registerWord("J", CopyThird())
