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


class OnePlus(core.Word):
    "(n -- n1) Increment by 1"
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n + 1)
core.registerWord('1+', OnePlus())


class OneMinus(core.Word):
    "(n -- n1) Decrement by 1"
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n - 1)
core.registerWord('1-', OneMinus())


class TwoPlus(core.Word):
    "(n -- n1) Increment by 2"
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n + 2)
core.registerWord('2+', TwoPlus())


class TwoMinus(core.Word):
    "(n -- n1) Decrement by 2"
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n - 2)
core.registerWord('2-', TwoMinus())


class DivideByTwo(core.Word):
    "(n -- n1) Divide by two (int). == Right bit shift."
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(n / 2)
core.registerWord('2/', DivideByTwo())


class Abs(core.Word):
    "(n -- |n|) Returns the absolute value."
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(abs(n))
core.registerWord('ABS', Abs())


class Negate(core.Word):
    "(n -- -n) Change the sign."
    def execute(self, interp):
        n = interp.stack.pop()
        interp.stack.push(0 - n)
core.registerWord('NEGATE', Negate())


class Min(core.Word):
    "(n1 n2 -- n-min) Put whichever of n1 and n2 is smaller."
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        interp.stack.push(min(n1, n2))
core.registerWord('MIN', Min())


class Max(core.Word):
    "(n1 n2 -- n-max) Put whichever of n1 and n2 is bigger."
    def execute(self, interp):
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        interp.stack.push(max(n1, n2))
core.registerWord('MAX', Max())


class StarSlash(core.Word):
    "(n1 n2 n3 -- n-result) Multiplies and *then* divides. Uses a 32-bit intermediate."
    def execute(self, interp):
        n3 = interp.stack.pop()
        n2 = interp.stack.pop()
        n1 = interp.stack.pop()
        # TODO: The whole 32 bit thing.
        result = (n1*n2) / n3
        interp.stack.push(result)
core.registerWord('*/', StarSlash())


class StarSlashMod(core.Word):
    "(u1 u2 u3 -- u-rem u-quot) Multiplies and *then* divides. Returns the quotient and the remainder."
    def execute(self, interp):
        u3 = interp.stack.pop()
        u2 = interp.stack.pop()
        u1 = interp.stack.pop()
        u = u1 * u2
        rem  = u % u3
        quot = u / u3
        interp.stack.push(rem)
        interp.stack.push(quot)
core.registerWord('*/MOD', StarSlashMod())
