# Simple (integer) arithmetic.
#

import core


class Plus(core.Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 + n1)
core.registerWord('+', Plus())


class Minus(core.Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 - n1)
core.registerWord('-', Minus())


class Multiply(core.Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 * n1)
core.registerWord('*', Multiply())


class Divide(core.Word):
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 / n1)
core.registerWord('/', Divide())
