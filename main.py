import parser
import compiler.compiler
import compiler.output
import forth.core
import unittest, sys
from optparse import OptionParser

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


def compile(input):
    codeOutput = compiler.output.OutputStatic()
    _parser    = parser.BasicParser()
    _compiler  = compiler.compiler.Compiler(codeOutput)

    lines = input.readlines()

    for line in lines:
        if line.strip() == '':
            continue
        stmts = _parser.parse(line)
        for stmt in stmts:
            _compiler.handleStatement(stmt)

    return codeOutput.generateEntireCode()
# end of compile


def interpret(code):
    _interp   = forth.core.Interpreter()
    _interp.processString(code)


if __name__ == '__main__':
    option_parser = OptionParser()
    option_parser.add_option('--compile-only', action='store_true', dest='compile_only', default=False, help="Only print the compiled code, rather than interpret it.")
    (options, filenames) = option_parser.parse_args()


    for filename in filenames:
        input = open(filename, "r")

        code = compile(input)
        input.close()

        if options.compile_only:
            print code
        else:
            interpret(code)
