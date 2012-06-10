"""
The compiler object.
"""

import lang
import data_types

# A placeholder object.
#
class CompiledStatement(object):
    def __init__(self, variables, statementCode):
        self.variables     = variables
        self.statementCode = statementCode
# end of CompiledStatement


#
#
class Variable(object):
    def __init__(self, basicName, dataType):
        self.basicName = basicName
        self.dataType = dataType
        # We won't know this yet...
        self.forthName = ''
# end of Variable


class Compiler(object):

    def __init__(self, codeOutput):
        self.statementBuffer   = []
        self.blockLevel        = 0
        self.codeOutput        = codeOutput
        self.variables         = {}
        self.variableIndex     = 0
    # end of __init__

    def registerVariable(self, variable):
        forthName = '__varname_%d' % (self.variableIndex)
        variable.forthName = forthName
        self.variables[variable.basicName] = variable
        self.variableIndex += 1
        return variable
    # end of registerVariable

    def variableForBasicName(self, basicName):
        return self.variables[basicName]
    # end of variableForBasicName

    def handleStatement(self, statement):
        compiledStatement = self.compileStatement(statement)

        for variable in compiledStatement.variables:
            # TODO, not always 1!!
            code = ['CREATE', variable.forthName, '1', 'ALLOT']
            self.codeOutput.addHeaderCode(code)

        if self.blockLevel == 0:
            self.codeOutput.beginStatement()

        # Now add to the buffers.
        self.blockLevel += statement.blockLevel()
        self.codeOutput.addBodyCode(compiledStatement.statementCode)

        # Can we finish off the statement?
        if self.blockLevel == 0:
            self.codeOutput.endStatement()
    # end of handleStatement

    def endProgram(self):
        pass
    # end of endProgram

    def compileStatement(self, stmt):
        if type(stmt) == lang.StatementPrint:
            return self.compileStatementPrint(stmt)
        elif type(stmt) == lang.StatementLet:
            return self.compileStatementLet(stmt)
            

    # end of compileStatement

    def compileStatementPrint(self, stmt):
        result = self.compileExpression(stmt.expression)
        # What about the type eh?
        typeObj = self.typeObjFor(stmt.expression)
        # Now simply add a "." to print!
        if type(typeObj) == data_types.Integer:
            result.append('.')
        elif type(typeObj) == data_types.Float:
            result.append('F.')
        result.append('CR')

        return CompiledStatement([], result)
    # end of compileStatementPrint

    def compileStatementLet(self, stmt):
        variable = self.registerVariable(Variable(stmt.varname, self.typeObjFor(stmt.expression)))

        statementCode   = self.compileExpression(stmt.expression)
        statementCode.extend([variable.forthName, '!'])
        return CompiledStatement([variable], statementCode)
    # end of compileStatementLet

    # Take a simple factor and compile it.
    #
    def compileFactor(self, factor, convertResultToType=None):
        "What we want to do is simply take a factor and compile it, but also make sure it is the correct type."
        value = factor.value

        # The resulting forth code for this...
        result = []

        # This is the simplest of all! A literal number or string is just the
        # number again in forth.
        if factor.factorType == lang.FactorTypeLiteral:
            if value.dataType == lang.DataTypeInteger:
                # Place the number token onto the stack.
                result.append(str(value.value))
            elif value.dataType == lang.DataTypeFloat:
                # Unfortunately Forth treats numbers with full stops in them
                # as double value ints # rather than floats. So we have to
                # represent this in scientific notation.
                # Also, use a ridiculous specifier (.20) otherwise we'll
                # lose too much precision.
                result.append('%.20e' % (value.value))
            elif value.dataType == lang.DataTypeString:
                result.append('TODO')

        # This is less simple. We need to grab the value and push it onto the
        # stack.
        elif factor.factorType == lang.FactorTypeVariable:
            variable = self.variableForBasicName(value)
            if variable == None:
                raise Exception('No variable found for %s')
            # Fetch the value of the variable.
            result.extend([variable.forthName, '@'])

        # Just compile the expression.
        elif factor.factorType == lang.FactorTypeExpression:
            result.extend(self.compileExpression(factor.value))

        # Now do any converting that we need.
        if convertResultToType != None:
            sourceType = self.typeObjFor(factor)
            result.extend(sourceType.convertTo(convertResultToType))

        return result
    # end of compileFactor

    # A term is factor op factor. But crucially we need to work out how to
    # combine the terms.
    #
    def compileTerm(self, term, convertResultToType=None):
        targetOperator, termType = self.howToCombine(term.primaryFactor, term.operator, term.secondaryFactor)
        result = []

        # There is always one factor. We convert it to the type of this term
        # so that the target operator can work on homogenous factors.
        result.extend(self.compileFactor(term.primaryFactor, termType))

        if (term.secondaryFactor != None):
            result.extend(self.compileFactor(term.secondaryFactor, termType))

        if (targetOperator != None):
            result.append(targetOperator)

        # Now do any converting that we need. Note that this is separate to the
        # termType. The termType is just for making sure that the factors are
        # homogenous so they can be used with the operator.
        if convertResultToType != None:
            sourceType = self.typeObjFor(term)
            result.extend(sourceType.convertTo(convertResultToType))

        return result
    # end of compileTerm

    # We handle expressions very similar to the way we handle terms.
    #
    def compileExpression(self, expression, convertResultToType=None):
        targetOperator, expressionType = self.howToCombine(expression.primaryTerm, expression.operator, expression.secondaryTerm)
        result = []

        result.extend(self.compileTerm(expression.primaryTerm, expressionType))

        if (expression.secondaryTerm != None):
            result.extend(self.compileTerm(expression.secondaryTerm, expressionType))

        if (targetOperator != None):
            result.append(targetOperator)

        # Now do any converting that we need.
        if convertResultToType != None:
            sourceType = self.typeObjFor(expression)
            result.extend(sourceType.convertTo(convertResultToType))

        return result
    # end of compileExpression

    #
    #
    def howToCombine(self, primary, operator, secondary):
        sourceType1 = self.typeObjFor(primary)
        sourceType2 = self.typeObjFor(secondary)

        # Is there just one thing though?
        if (secondary == None):
            targetType = sourceType1
            targetOperator = None

        if (type(sourceType1) == data_types.Integer and type(sourceType2) == data_types.Integer):
            targetType = data_types.Integer()
            if operator == lang.TermOperatorMultiply:
                targetOperator = '*'
            elif operator == lang.TermOperatorDivide:
                targetOperator = '/'
            elif operator == lang.ExpressionOperatorPlus:
                targetOperator = '+'
            elif operator == lang.ExpressionOperatorMinus:
                targetOperator = '-'

        elif (
            (type(sourceType1) == data_types.Integer and type(sourceType2) == data_types.Float) or 
            (type(sourceType1) == data_types.Float and type(sourceType2) == data_types.Integer) or
            (type(sourceType1) == data_types.Float and type(sourceType2) == data_types.Float)
            ):
            targetType = data_types.Float()
            if operator == lang.TermOperatorMultiply:
                targetOperator = 'F*'
            elif operator == lang.TermOperatorDivide:
                targetOperator = 'F/'
            elif operator == lang.ExpressionOperatorPlus:
                targetOperator = 'F+'
            elif operator == lang.ExpressionOperatorMinus:
                targetOperator = 'F-'

        return (targetOperator, targetType)
    # end of howToCombine

    def typeObjFor(self, item):
        # Factors might be simple...
        if type(item) == lang.Factor:
            if item.factorType == lang.FactorTypeLiteral:
                return self.compilerTypeObjFor(item.value.dataType)
            elif item.factorType == lang.FactorTypeVariable:
                # For now assume integer :(
                return data_types.Integer()
            elif item.factorType == lang.FactorTypeExpression:
                return self.typeObjFor(item.value)

        elif type(item) == lang.Term:
            targetOperator, targetTypeObj = self.howToCombine(item.primaryFactor, item.operator, item.secondaryFactor)
            return targetTypeObj

        elif type(item) == lang.Expression:
            targetOperator, targetTypeObj = self.howToCombine(item.primaryTerm, item.operator, item.secondaryTerm)
            return targetTypeObj
    # end of typeObjFor

    def compilerTypeObjFor(self, langDataType):
        if langDataType == lang.DataTypeInteger:
            return data_types.Integer()
        elif langDataType == lang.DataTypeFloat:
            return data_types.Float()
        elif langDataType == lang.DataTypeString:
            return data_types.String()

    def codeToStr(self, pcode):
        return " ".join(pcode)
