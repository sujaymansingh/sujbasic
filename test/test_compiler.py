from compiler import *
from lang import *
import unittest


class TestFactor(unittest.TestCase):

    def setUp(self):
        self.compiler = Compiler()

    def createLiteral(self, val):
        return Factor(FactorTypeLiteral, createTypedValue(val))

    def createTerm(self, v1, op=None, v2=None):
        t = Term(self.createLiteral(v1))
        if (op != None and v2 != None):
            t.addFactor(op, self.createLiteral(v2))
        return t

    def testTypeObjFor(self):
        # Right, let's test very simple factors.
        f1 = self.createLiteral(5)
        self.assertTrue(type(self.compiler.typeObjFor(f1)) == ForthDataTypeInteger)
        f2 = self.createLiteral(5.0)
        self.assertTrue(type(self.compiler.typeObjFor(f2)) == ForthDataTypeFloat)
        f3 = self.createLiteral("five")
        self.assertTrue(type(self.compiler.typeObjFor(f3)) == ForthDataTypeString)

        # Terms...
        items = []
        items.append([5.0, 5, ForthDataTypeFloat])
        items.append([5, 5.0, ForthDataTypeFloat])
        items.append([5.0, 5.0, ForthDataTypeFloat])
        items.append([5, 5, ForthDataTypeInteger])

        for item in items:
            t1 = self.createTerm(item[0], TermOperatorDivide, item[1])
            res = self.compiler.typeObjFor(t1)
            self.assertEquals(type(res), item[2])



    def testLiterals(self):

        f1 = self.createLiteral(5)
        self.assertEquals(self.compiler.compileFactor(f1, None), ['5'])
        # To float?
        self.assertEquals(self.compiler.compileFactor(f1, ForthDataTypeFloat()), ['5', 'S>D', 'D>F'])
        # To String? Hehehe.
        # TODO

        f2 = self.createLiteral(42.4)
        f_str = '%.20e' % (42.4)
        self.assertEquals(self.compiler.compileFactor(f2, None), [f_str])
        # To int...
        self.assertEquals(self.compiler.compileFactor(f2, ForthDataTypeInteger()), [f_str, 'F>D', 'D>S'])
    # testLiterals


    def testCombineDetails(self):

        # int * float
        f1 = self.createLiteral(4)
        f2 = self.createLiteral(4.0)
        res = self.compiler.combineDetails(f1, TermOperatorMultiply, f2)
        self.assertTrue(res[0] == 'F*')
        self.assertTrue(type(res[1]) == ForthDataTypeFloat)

        # float * int
        f1 = self.createLiteral(6.0)
        f2 = self.createLiteral(40)
        res = self.compiler.combineDetails(f1, TermOperatorMultiply, f2)
        self.assertTrue(res[0] == 'F*')
        self.assertTrue(type(res[1]) == ForthDataTypeFloat)

        # int / int
        f1 = self.createLiteral(60)
        f2 = self.createLiteral(40)
        res = self.compiler.combineDetails(f1, TermOperatorDivide, f2)
        self.assertTrue(res[0] == '/')
        self.assertTrue(type(res[1]) == ForthDataTypeInteger)
    # testCombineDetails


    def testCompileTerm(self):

        # 5.0 / 3
        t1 = self.createTerm(5.0, TermOperatorDivide, 3)
        res = self.compiler.compileTerm(t1)
        # Don't care about the first item, it's going to be some crazy float representation.
        # But the 2nd item should be 3, converted to a float.
        self.assertEquals("3", res[1])
        self.assertEquals("S>D", res[2])
        self.assertEquals("D>F", res[3])
        # Finally, a *float* divide.
        self.assertEquals("F/", res[4])

        # 4 * 4
        t1 = self.createTerm(4, TermOperatorMultiply, 4)
        res = self.compiler.compileTerm(t1)
        self.assertEquals("4", res[0])
        self.assertEquals("4", res[1])
        # Finally, a int multiply.
        self.assertEquals("*", res[2])

        # Simple: 5
        t1 = self.createTerm(5)
        res = self.compiler.compileTerm(t1)
        self.assertEquals(['5'], res)
    # testCompileTerm


    def testCompileExpression(self):
        # 5 + 5.5
        t1 = self.createTerm(5)
        t2 = self.createTerm(5.5)
        e = Expression(t1, ExpressionOperatorPlus, t2)
        comb = self.compiler.combineDetails(e.primaryTerm, e.operator, e.secondaryTerm)
        self.assertEquals(comb[0], 'F+')
        self.assertEquals(type(comb[1]), ForthDataTypeFloat)
        res = self.compiler.compileExpression(e)
        self.assertEquals(res[0], '5')
        self.assertEquals(res[1], 'S>D')
        self.assertEquals(res[2], 'D>F')
        # item 3 will be some very long silly float repr
        self.assertEquals(res[4], 'F+')

        # 5 + 5
        t1 = self.createTerm(5)
        t2 = self.createTerm(5)
        e = Expression(t1, ExpressionOperatorPlus, t2)
        comb = self.compiler.combineDetails(e.primaryTerm, e.operator, e.secondaryTerm)
        self.assertEquals(comb[0], '+')
        self.assertEquals(type(comb[1]), ForthDataTypeInteger)
        res = self.compiler.compileExpression(e)
        self.assertEquals(res[0], '5')
        self.assertEquals(res[1], '5')
        self.assertEquals(res[2], '+')

        

        



    # testCompileExpression



def main():
    unittest.main()

if __name__ == '__main__':
    main()

    # testCombineDetails


def main():
    unittest.main()

if __name__ == '__main__':
    main()
