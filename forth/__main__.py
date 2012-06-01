import sys, os
import traceback

sys.path.append(os.getcwd())
import core

if __name__ == '__main__':

    interp = core.Interpreter()

    keepGoing = True

    while keepGoing:
        try:
            line = raw_input('forth> ')
            try:
                interp.processString(line)
                interp.output.write("ok\n")
            except Exception as e:
                print 'Encountered erroe ',e
                traceback.print_exc(file=sys.stdout)
        except EOFError:
            keepGoing = False
