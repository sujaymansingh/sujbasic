from compiler import *
from lang import *
import unittest


class TestFactor(unittest.TestCase):

    def setUp(self):
        self.compiler = Compiler()

    def testTypeObjFor(self):
        # Right, let's test very simple factors.
        f1 = Factor(FactorTypeLiteral, createTypedValue(5))
        self.assertTrue(type(self.compiler.typeObjFor(f1)) == ForthDataTypeInteger)
        f2 = Factor(FactorTypeLiteral, createTypedValue(5.0))
        self.assertTrue(type(self.compiler.typeObjFor(f2)) == ForthDataTypeFloat)
        f3 = Factor(FactorTypeLiteral, createTypedValue("five"))
        self.assertTrue(type(self.compiler.typeObjFor(f3)) == ForthDataTypeString)


    def testLiterals(self):

        f1 = Factor(FactorTypeLiteral, createTypedValue(5))
        self.assertEquals(self.compiler.compileFactor(f1, None), ['5'])
        # To float?
        self.assertEquals(self.compiler.compileFactor(f1, ForthDataTypeFloat()), ['5', 'S>D', 'D>F'])
        # To String? Hehehe.
        # TODO

        f2 = Factor(FactorTypeLiteral, createTypedValue(42.4))
        f_str = '%.20e' % (42.4)
        self.assertEquals(self.compiler.compileFactor(f2, None), [f_str])
        # To int...
        self.assertEquals(self.compiler.compileFactor(f2, ForthDataTypeInteger()), [f_str, 'F>D', 'D>S'])


        pass
    # testLiterals


def main():
    unittest.main()

if __name__ == '__main__':
    main()
