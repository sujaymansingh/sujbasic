import re
import sys
import ply.lex
from ply.lex import TOKEN
import ply.yacc

import lang



class BasicLexer(object):
    """ A simply lexer for my version of Basic. """

    def __init__(self, error_func, type_lookup_func):
        """ TODO """
        self.error_func = error_func
        self.type_lookup_func = type_lookup_func


    def build(self, **kwargs):
        """ Build the lexer based around ourself. """
        self.lexer = ply.lex.lex(object=self, **kwargs)

    def resetLineNumber(self):
        """ Reset our internal line counter. """
        self.lexer.lineno = 1


    def input(self, text):
        self.lexer.input(text)


    def token(self):
        token = self.lexer.token()
        return token

    reserved = {
        'for'      : 'FOR',
        'print'    : 'PRINT',
        'to'       : 'TO',
        'next'     : 'NEXT'
    }

    # Define our list of tokens.
    tokens = (
        'VARNAME',
        'NUMBER',
        'CR',

        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'EQUALS',
        'LPAREN',
        'RPAREN',
        'QUOTE',
        'COLON',
    
        'FOR',
        'TO',
        'NEXT',
        'PRINT'
    )

    # The simple literals.
    t_PLUS     = r'\+'
    t_MINUS    = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE   = r'/'
    t_EQUALS   = '='
    t_LPAREN   = '\('
    t_RPAREN   = '\)'
    t_QUOTE    = '\"'
    t_COLON    = ':'

    # Keywords.
    t_FOR   = 'FOR'
    t_PRINT = 'PRINT'

    def t_CR(self, t):
        r'\n'
        # TODO: increase the line number?
        t.lexer.lineno += t.value.count('\n')
        return t

    # A number.
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    # An identifier
    def t_VARNAME(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_-]*'
        t.type = self.reserved.get(t.value.lower(), 'VARNAME')
        return t
    
    t_ignore = ' \t'
    
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)


class BasicParser(object):

    def __init__(self):
        """ Init! """
        self.lexer = BasicLexer(error_func = self.lexerErrorFunc, type_lookup_func = self.lexerTypeLookupFunc)
        self.lexer.build()
        self.tokens = self.lexer.tokens

        self.parser = ply.yacc.yacc(module=self, start='program')


    def parse(self, text):
        """Parses some basic code and returns a list of statements."""
        self.lexer.resetLineNumber()

        return self.parser.parse(text, lexer=self.lexer)


    def lexerErrorFunc(self, msg, a, b):
        sys.write(msg + '\n')
        sys.exit()

    def lexerTypeLookupFunc(self, named):
        return False()

    def handleStatement(self, statement):
        #print 'Just read ',statement
        pass


    def p_program(self, p):
        'program : statements'
        p[0] = p[1]
    
    def p_statements_statements(self, p):
        'statements : statement CR statements'
        #print 'just read statements %s and %s' % (p[1], p[3])
        p[0] = [p[1]] + p[3]
    
    def p_statements_statement(self, p):
        'statements : statement CR'
        #print 'just read statement ',p[1]
        p[0] = [p[1]]
    
    #def p_statement(self, p):
    #    'statement : statement'
    #    p[0] = p[1]
    
    def p_statement_print(self, p):
        'statement : PRINT expression'
        p[0] = lang.StatementPrint(p[2])

    def p_statement_for(self, p):
        'statement : FOR VARNAME EQUALS NUMBER TO NUMBER CR statements NEXT CR'
        p[0] = lang.StatementFor(p[2], p[4], p[6], p[8])


    # Expression/terms/factors.
    #
    def p_expression_plus(self, p):
        'expression : term PLUS term'
        p[0] = lang.Expression(p[1])
        p[0].addTerm(lang.ExpressionOperatorPlus, p[3])
    
    def p_expression_minus(self, p):
        'expression : term MINUS term'
        p[0] = lang.Expression(p[1])
        p[0].addTerm(lang.ExpressionOperatorMinus, p[3])
    
    def p_expression(self, p):
        'expression : term'
        p[0] = lang.Expression(p[1])
    
    def p_term_multiply(self, p):
        'term : factor MULTIPLY factor'
        p[0] = lang.Term(p[1])
        p[0].addFactor(lang.TermOperatorMultiply, p[3])
    
    def p_term_divide(self, p):
        'term : factor DIVIDE factor'
        p[0] = lang.Term(p[1])
        p[0].addFactor(lang.TermOperatorDivide, p[3])
    
    def p_term(self, p):
        'term : factor'
        p[0] = lang.Term(p[1])
    
    def p_factor_expression(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = lang.Factor(lang.FactorTypeExpression, p[2])
    
    def p_factor_varname(self, p):
        'factor : VARNAME'
        p[0] = lang.Factor(lang.FactorTypeVariable, p[1])
    
    def p_factor_literal(self, p):
        'factor : NUMBER'
        p[0] = lang.Factor(lang.FactorTypeLiteral, lang.createTypedValue(p[1]))

