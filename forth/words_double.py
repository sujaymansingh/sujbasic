# Words to handle double-ints and stuff like that.
#
import core


class TwoSwap(core.Word):
    """(d1 d2 -- d2 d1) Reverses the top pair of numbers."""
    def execute(self, interp):
        d2b = interp.stack.pop()
        d2a = interp.stack.pop()
        d1b = interp.stack.pop()
        d1a = interp.stack.pop()
        for d in [d2a, d2b, d1a, d1b]:
            interp.stack.push(d)
core.registerWord('2SWAP', TwoSwap())


class TwoDup(core.Word):
    """(d -- d d) Duplicate the top pair of numbers."""
    def execute(self, interp):
        db = interp.stack.pop()
        da = interp.stack.pop()
        for d in [da, db, da, db]:
            interp.stack.push(d)
core.registerWord('2DUP', TwoDup())


class TwoOver(core.Word):
    """(d1 d2 --- d1 d2 d1) Makes a copy of the 2nd pair and pushes it on the top."""
    def execute(self, interp):
        d2b = interp.stack.pop()
        d2a = interp.stack.pop()
        d1b = interp.stack.pop()
        d1a = interp.stack.pop()
        for d in [d1a, d1b, d2a, d2b, d1a, d1b]:
            interp.stack.push(d)
core.registerWord('2OVER', TwoOver())


class TwoDrop(core.Word):
    """(d -- ) Discard the top pair of numbers."""
    def execute(self, interp):
        interp.stack.pop()
        interp.stack.pop()
core.registerWord('2DROP', TwoDrop())
