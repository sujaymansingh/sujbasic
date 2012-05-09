import parser
import compiler
import forth
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


def run(line):
    _parser   = parser.BasicParser()
    _compiler = compiler.Compiler()
    _interp   = forth.Interpreter()

    print "Compiling '%s'..." % (line)

    stmts = _parser.parse(line + '\n')
    i = 0
    for stmt in stmts:
        print "Statement %d parses to '%s'" % (i, stmt)
        
        code = _compiler.codeToStr(_compiler.compileStatementPrint(stmt))
        print "Statement %d compiles to '%s'" % (i, code)

        print "About to run through interpreter..."
        _interp.processString(code)




if __name__ == '__main__':
    for line in sys.argv[1:]:
        run(line)
