"""
Yeah.
"""

import lang


class Compiler(object):


    def compileFactor(self, factor, targetType=None):
        "What we want to do is simply take a factor and compile it, but also make sure it is the correct type"
        value = factor.value

        # The resulting forth code for this...
        result = []

        if factor.factorType == lang.FactorTypeLiteral:
            if value.dataType == lang.DataTypeInteger:
                result.append(str(value.value))
            elif value.dataType == lang.DataTypeFloat:
                # Unfortunately Forth treats numbers with full stops in them as double value ints
                # rather than floats. So we have to represent this in scientific notation.
                # Also, use a ridiculous specifier (.20) otherwise we'll lose too much precision.
                result.append('%.20e' % (value.value))
            elif value.dataType == lang.DataTypeString:
                result.append('TODO')

        elif factor.factorType == lang.FactorTypeVariable:
            result.append('TODO')

        elif factor.factorType == lang.FactorTypeExpression:
            result.extend(self.compileExpression(factor.value))

        # Now do any converting that we need.
        if targetType != None:
            sourceType = self.typeObjFor(factor)
            result.extend(sourceType.convertTo(targetType))

        return result
    # end of compileFactor


    def compileTerm(self, term, targetType=None):
        combineDetails = self.combineDetails(term.primaryFactor, term.operator, term.secondaryFactor)
        (targetOperator, termTargetType) = combineDetails
        result = []

        result.extend(self.compileFactor(term.primaryFactor, termTargetType))
        if (term.secondaryFactor != None):
            result.extend(self.compileFactor(term.secondaryFactor, termTargetType))
        if (targetOperator != None):
            result.append(targetOperator)

        # Now do any converting that we need.
        if targetType != None:
            sourceType = self.typeObjFor(term)
            result.extend(sourceType.convertTo(targetType))

        return result
    # end of compileTerm


    def compileExpression(self, expression, targetType=None):
        combineDetails = self.combineDetails(expression.primaryTerm, expression.operator, expression.secondaryTerm)
        (targetOperator, expressionTargetType) = combineDetails
        result = []

        result.extend(self.compileTerm(expression.primaryTerm, expressionTargetType))
        if (expression.secondaryTerm != None):
            result.extend(self.compileTerm(expression.secondaryTerm, expressionTargetType))
        if (targetOperator != None):
            result.append(targetOperator)

        # Now do any converting that we need.
        if targetType != None:
            sourceType = self.typeObjFor(expression)
            result.extend(sourceType.convertTo(targetType))

        return result
    # end of compileExpression




    def combineDetails(self, primary, operator, secondary):
        sourceType1 = self.typeObjFor(primary)
        sourceType2 = self.typeObjFor(secondary)

        # Is there just one thing though?
        if (secondary == None):
            targetType = sourceType1
            targetOperator = None

        if (type(sourceType1) == ForthDataTypeInteger and type(sourceType2) == ForthDataTypeInteger):
            targetType = ForthDataTypeInteger()
            if operator == lang.TermOperatorMultiply:
                targetOperator = '*'
            elif operator == lang.TermOperatorDivide:
                targetOperator = '/'
            elif operator == lang.ExpressionOperatorPlus:
                targetOperator = '+'
            elif operator == lang.ExpressionOperatorMinus:
                targetOperator = '-'


        elif (
            (type(sourceType1) == ForthDataTypeInteger and type(sourceType2) == ForthDataTypeFloat) or 
            (type(sourceType1) == ForthDataTypeFloat and type(sourceType2) == ForthDataTypeInteger) or
            (type(sourceType1) == ForthDataTypeFloat and type(sourceType2) == ForthDataTypeFloat)
            ):
            targetType = ForthDataTypeFloat()
            if operator == lang.TermOperatorMultiply:
                targetOperator = 'F*'
            elif operator == lang.TermOperatorDivide:
                targetOperator = 'F/'
            elif operator == lang.ExpressionOperatorPlus:
                targetOperator = 'F+'
            elif operator == lang.ExpressionOperatorMinus:
                targetOperator = 'F-'

        return (targetOperator, targetType)
    # end of combineDetails


    def typeObjFor(self, item):
        # Factors might be simple...
        if type(item) == lang.Factor:
            if item.factorType == lang.FactorTypeLiteral:
                return self.toCompilerTypeObjFor(item.value.dataType)
            elif item.factorType == lang.FactorTypeVariable:
                return None
            elif item.factorType == lang.FactorTypeExpression:
                return self.typeObjFor(item.value)

        elif type(item) == lang.Term:
            (targetOperator, targetTypeObj) = self.combineDetails(item.primaryFactor, item.operator, item.secondaryFactor)
            return targetTypeObj

        elif type(item) == lang.Expression:
            (targetOperator, targetTypeObj) = self.combineDetails(item.primaryTerm, item.operator, item.secondaryTerm)
            return targetTypeObj
            
    # end of typeObjFor



    def toCompilerTypeObjFor(self, langDataType):
        if langDataType == lang.DataTypeInteger:
            return ForthDataTypeInteger()
        elif langDataType == lang.DataTypeFloat:
            return ForthDataTypeFloat()
        elif langDataType == lang.DataTypeString:
            return ForthDataTypeString()

    def compileStatementPrint(self, stmt):
        result = self.compileExpression(stmt.expression)
        # What about the type eh?
        typeObj = self.typeObjFor(stmt.expression)
        # Now simply add a "." to print!
        if type(typeObj) == ForthDataTypeInteger:
            result.append('.')
        elif type(typeObj) == ForthDataTypeFloat:
            result.append('F.')
        result.append('CR')
        return result

    def codeToStr(self, pcode):
        return " ".join(pcode)

# Data Types!
#
#
class ForthDataType(object):
    def convertTo(self, otherForthDataType):
        pass
class ForthDataTypeInteger(ForthDataType):
    def convertTo(self, otherForthDataType):
        if type(otherForthDataType) == ForthDataTypeInteger:
            # Nothing to do or see here!
            return []
        elif type(otherForthDataType) == ForthDataTypeDoubleInteger:
            # If the existing int is 'n', then we want 'n 0' on the stack.
            return ['S>D']
        elif type(otherForthDataType) == ForthDataTypeFloat:
            return ['S>D', 'D>F']
        elif type(otherForthDataType) == ForthDataTypeString:
            return ['TODO']
# end of ForthDataTypeInteger
class ForthDataTypeDoubleInteger(ForthDataType):
    def convertTo(self, otherForthDataType):
        if type(otherForthDataType) == ForthDataTypeInteger:
            return ['D>S']
        elif type(otherForthDataType) == ForthDataTypeDoubleInteger:
            # Nothing to do or see here!
            return ['']
        elif type(otherForthDataType) == ForthDataTypeFloat:
            return ['D>F']
        elif type(otherForthDataType) == ForthDataTypeString:
            return ['TODO']
# end of ForthDataTypeDoubleInteger
class ForthDataTypeFloat(ForthDataType):
    def convertTo(self, otherForthDataType):
        if type(otherForthDataType) == ForthDataTypeInteger:
            return ['F>D', 'D>S']
        elif type(otherForthDataType) == ForthDataTypeDoubleInteger:
            return ['F>D']
        elif type(otherForthDataType) == ForthDataTypeFloat:
            # Nothing to do or see here!
            return []
        elif type(otherForthDataType) == ForthDataTypeString:
            return ['TODO']
# end of ForthDataTypeFloat
class ForthDataTypeString(ForthDataType):
    def convertTo(self, otherForthDataType):
        if type(otherForthDataType) == ForthDataTypeInteger:
            return ['TODO']
        elif type(otherForthDataType) == ForthDataTypeDoubleInteger:
            return ['TODO']
        elif type(otherForthDataType) == ForthDataTypeFloat:
            return ['TODO']
        elif type(otherForthDataType) == ForthDataTypeString:
            # Nothing to do or see here!
            return []
# end of ForthDataTypeFloat

