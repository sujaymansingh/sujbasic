# Basic Data Structures.
#


# Right, some basic data types.
#
class DataType(object):
    def __init__(self, c): self.c = c
    def __str__(self): return self.c
DataTypeString     = DataType('String')
DataTypeInteger    = DataType('Integer')
DataTypeFloat      = DataType('Float')

class TypedValue(object):
    def __init__(self, dataType, value):
        self.dataType = dataType
        self.value    = value

    def __str__(self):
        return '%s(%s)' % (str(self.dataType), str(self.value))

def createTypedValue(value):
    result = TypedValue(None, value)
    if (type(value) == int):
        result.dataType = DataTypeInteger
    elif (type(value) == str):
        result.dataType = DataTypeString
    elif (type(value) == float):
        result.dataType = DataTypeFloat
    return result
# end of data types.


# Factors!
#
class FactorType(object):
    def __init__(self, c): self.c = c
    def __str__(self): return self.c
FactorTypeExpression = FactorType('FactorTypeExpression')
FactorTypeVariable   = FactorType('FactorTypeVariable')
FactorTypeLiteral    = FactorType('FactorTypeLiteral')

# The simplest item.
class Factor(object):

    # The value clearly depends upon the factorType.
    # If a literal, then it's the value: 5, 'suj' etc.
    # If a variable, then it's the name of the variable.
    # If an expression, then it's the actual expression.
    def __init__(self, factorType, value):
        self.factorType = factorType
        self.value      = value

    def __str__(self):
        return 'Factor(%s, %s)' % (self.factorType, self.value)
# end of Factors


# Terms! These are basically (<Factor> [+-] <Factor>).
#
class TermOperator(object):
    def __init__(self, c): self.c = c
    def __str__(self): return self.c
TermOperatorMultiply   = TermOperator('*')
TermOperatorDivide     = TermOperator('/')

class Term(object):

    # The operator and secondaryFactor can clearly be None.
    # But not the primaryFactor.
    def __init__(self, primaryFactor, operator=None, secondaryFactor=None):
        self.primaryFactor   = primaryFactor
        self.operator        = operator
        self.secondaryFactor = secondaryFactor

    def addFactor(self, operator, secondaryFactor):
        self.operator = operator
        self.secondaryFactor = secondaryFactor

    def __str__(self):
        return 'Term(%s, %s, %s)' % (self.primaryFactor, self.operator, self.secondaryFactor)
# end of Terms


# Expressions! These are basically (<Term> [*/] <Term>).
#
class ExpressionOperator(object):
    def __init__(self, c): self.c = c
    def __str__(self): return self.c
ExpressionOperatorPlus     = ExpressionOperator('+')
ExpressionOperatorMinus    = ExpressionOperator('-')

class Expression(object):

    # The operator and secondaryTerm can clearly be None.
    # But not the primaryTerm
    def __init__(self, primaryTerm, operator=None, secondaryTerm=None):
        self.primaryTerm   = primaryTerm
        self.operator      = operator
        self.secondaryTerm = secondaryTerm

    def addTerm(self, operator, secondaryTerm):
        self.operator = operator
        self.secondaryTerm = secondaryTerm

    def __str__(self):
        return 'Expression(%s, %s, %s)' % (self.primaryTerm, self.operator, self.secondaryTerm)
# end of Expressions


# Statement
#
class Statement(object):

    # A default of 1.
    def blockLevel(self):
        return 0
# end of Statement


# Print Statement
class StatementPrint(Statement):

    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return 'StatementPrint( %s )' % (self.expression)
# end of Print Statement
