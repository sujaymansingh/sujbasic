# Simple (integer) arithmetic.
#

import core


class Plus(core.Word):
    "(n1 n2 -- n) Add the top two numbers on the stack and push the result"
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 + n1)
core.registerWord('+', Plus())


class Minus(core.Word):
    "(n1 n2 -- n) Subtract n2 from n1 and push the result on the stack"
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 - n1)
core.registerWord('-', Minus())


class Multiply(core.Word):
    "(n1 n2 -- n) Multiply the top two numbers and push the result"
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 * n1)
core.registerWord('*', Multiply())


class Divide(core.Word):
    "(n1 n2 -- n) Put the integer result of n1/n2 onto the stack"
    def execute(self, interp):
        n1 = interp.stack.pop()
        n2 = interp.stack.pop()
        interp.stack.push(n2 / n1)
core.registerWord('/', Divide())


class SlashMod(core.Word):
    "(u1 u2 -- u-rem u-quot) Divide u1 by u2 and put the remainder and then quotient onto the stack"
    def execute(self, interp):
        u2 = interp.stack.pop()
        u1 = interp.stack.pop()
        rem  = u1 % u2
        quot = u1 / u2
        interp.stack.push(rem)
        interp.stack.push(quot)
core.registerWord('/MOD', SlashMod())


class Mod(core.Word):
    "(u1 u2 -- u-rem u-quot) Divide u1 by u2 and put the remainder onto the stack"
    def execute(self, interp):
        u2 = interp.stack.pop()
        u1 = interp.stack.pop()
        interp.stack.push(u1 % u2)
core.registerWord('MOD', Mod())
