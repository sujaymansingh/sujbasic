"""
Yeah.
"""

import lang


class Compiler(object):


    def compileFactor(self, factor, targetType):
        "What we want to do is simply take a factor and compile it, but also make sure it is the correct type"
        value = factor.value
        sourceType = self.typeObjFor(factor)

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
            result.extend(sourceType.convertTo(targetType))

        return result
    # end of compileFactor


    def compileTerm(self, term):
        combineDetails = self.combineDetails(term.primaryFactor, term.operator, term.secondaryFactor)
        

    # end of compileTerm




    def combineDetails(self, primary, operator, secondary):
        pass


    def typeObjFor(self, item):
        # Factors might be simple...
        if type(item) == lang.Factor:
            if item.factorType == lang.FactorTypeLiteral:
                return self.toCompilerTypeObjFor(item.value.dataType)
            elif item.factorType == lang.FactorTypeVariable:
                return None
            elif item.factorType == lang.FactorTypeExpression:
                return None



    def toCompilerTypeObjFor(self, langDataType):
        if langDataType == lang.DataTypeInteger:
            return ForthDataTypeInteger()
        elif langDataType == lang.DataTypeFloat:
            return ForthDataTypeFloat()
        elif langDataType == lang.DataTypeString:
            return ForthDataTypeString()

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

