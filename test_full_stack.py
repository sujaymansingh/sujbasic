import parser
import compiler.compiler
import forth.core
import unittest
import sys

#class TestPrint(unittest.TestCase):
#
#    def setUp(self):
#        self.parser   = parser.BasicParser()
#        self.compiler = compiler.Compiler()
#        self.interp   = forth.Interpreter()
#
#    def testSimplePrint(self):
#        line = 'PRINT 5 + 3\n'
#        stmts = self.parser.parse(line)
#        stmt = stmts[0]
#        print '"%s" parses to "%s"' % (line.strip(), stmt)
#
#        pcodeStr = self.compiler.codeToStr(self.compiler.compileStatementPrint(stmt))
#        print '"%s" compiles to "%s"'  % (stmt, pcodeStr)
#
#        print 'Passing "%s" to interpeter' % (pcodeStr)
#        self.interp.processString(pcodeStr)


class CodeHandler(object):
    def __init__(self):
        self.buffer = ''
    def handleCode(self, code):
        self.buffer += ' '.join(code)
        self.buffer += ' '
    def popCode(self):
        result = self.buffer.strip()
        self.buffer = ''
        return result


def run(line):
    codeHandler = CodeHandler()

    _parser   = parser.BasicParser()
    _compiler = compiler.compiler.Compiler(codeHandler)
    _interp   = forth.core.Interpreter()

    print "Compiling '%s'..." % (line)

    stmts = _parser.parse(line + '\n')
    i = 0
    for stmt in stmts:
        print "Statement %d parses to '%s'" % (i, stmt)

        _compiler.handleStatement(stmt)
        code = codeHandler.popCode()
        
        print "Statement %d compiles to '%s'" % (i, code)

        print "About to run through interpreter..."
        _interp.processString(code)


if __name__ == '__main__':
    for line in sys.argv[1:]:
        run(line)
