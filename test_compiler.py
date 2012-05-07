from compiler import *
from lang import *
import unittest


class TestFactor(unittest.TestCase):

    def setUp(self):
        self.compiler = Compiler()

    def testLiterals(self):
        "So this should be fairly simple right?"

        factor = Factor(FactorTypeLiteral, createTypedValue(5))
        res = self.compiler.compileFactor(factor)
        self.assertEquals(['5'], res)
    # testLiterals

    def testTerms(self):
        "Simpler...maybe."

        term = Term(Factor(FactorTypeLiteral, createTypedValue(6)))
        term.addFactor(TermOperatorPlus, Factor(FactorTypeLiteral, createTypedValue(11)))
        res = self.compiler.compileTerm(term)
        self.assertEquals(['6', '11', '+'], res)
    
    def testExpression(self):

        # (5+8) * (6-4)
        term1 = Term(Factor(FactorTypeLiteral, createTypedValue(5)), TermOperatorPlus, Factor(FactorTypeLiteral, createTypedValue(8)))
        term2 = Term(Factor(FactorTypeLiteral, createTypedValue(6)), TermOperatorMinus, Factor(FactorTypeLiteral, createTypedValue(4)))
        expression = Expression(term1, ExpressionOperatorMultiply, term2)
        resStr = self.compiler.codeToStr(self.compiler.compileExpression(expression))
        self.assertEquals('5 8 + 6 4 - *', resStr)
    # testTerms


def main():
    unittest.main()

if __name__ == '__main__':
    main()
