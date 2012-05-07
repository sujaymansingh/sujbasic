
import lang

class Compiler(object):


    def compileFactor(self, factor):

        value = factor.value
        
        if (factor.factorType == lang.FactorTypeLiteral):
            # For now, I can only deal with integers. Maybe.
            if (value.dataType == lang.DataTypeInteger):
                return [str(value.value)]
            elif (value.dataType == lang.DataTypeFloat):
                return ['TODO']
            elif (value.dataType == lang.DataTypeString):
                return ['TODO']

        elif (factor.factorType == lang.FactorTypeVariable):
            return ['TODO']

        elif (factor.factorType == lang.FactorTypeExpression):
            return self.compileExpression(value)
    # end of compileFactor


    def compileTerm(self, term):
        result = []

        # No matter what, we need to compile the first factor.
        primary_pcode = self.compileFactor(term.primaryFactor)

        # I guess we need to look at the type but for now we only care about ints.
        for p in primary_pcode:
            result.append(p)

        # Are there any other terms?
        if (term.secondaryFactor != None):
            secondary_pcode = self.compileFactor(term.secondaryFactor)
            for p in secondary_pcode:
                result.append(p)
            # Now the operator, which for now is just ints.
            if (term.operator == lang.TermOperatorPlus):
                result.append('+')
            elif (term.operator == lang.TermOperatorMinus):
                result.append('-')
            else:
                raise "Bad operator '%s'" % (term.operator)

        return result
    # end of compileTerm


    def compileExpression(self, expression):
        result = []

        # similar to terms...
        primary_pcode = self.compileTerm(expression.primaryTerm)

        # I guess we need to look at the type but for now we only care about ints.
        for p in primary_pcode:
            result.append(p)

        if (expression.secondaryTerm != None):
            secondary_pcode = self.compileTerm(expression.secondaryTerm)
            for p in secondary_pcode:
                result.append(p)
            # Now the operator, which for now is just ints.
            if (expression.operator == lang.ExpressionOperatorMultiply):
                result.append('*')
            elif (expression.operator == lang.ExpressionOperatorDivide):
                result.append('/')
            else:
                raise "Bad operator '%s'" % (expression.operator)


        return result
    # end of compileExpression

    def codeToStr(self, pcode):
        return ' '.join(pcode)

# end of Compiler

