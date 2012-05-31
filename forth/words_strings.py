# How to handle strings. Yeesh.
#

import core

# Literals
# I.e. be able to do stuff like: ." Hello, World "
#
class StartLiteral(core.Word):
    # TODO: this should really be linked into to the tokeniser to avoid collapsing multiple spaces.

    def execute(self, interp):
        print 'executing ."',
        interp.readUptoAndGiveTo('"', self)
        print 'interp.consumeUpto=(%s) ' % (interp.consumeUpto())

    def handleToken(self, token, interp):
        print 'just handled "%s"' % (token)
        interp.output.write(token)
        return
        reachedEnd = False

        if token == '"':
            reachedEnd = True
        elif token.endswith('"'):
            self.buffer = self.buffer + ' ' + token[0:-1]
            reachedEnd = True
        else:
            self.buffer = self.buffer + ' ' + token

        if reachedEnd:
            interp.output.write(self.buffer)
        else:
            interp.giveNextTokenTo(self)
core.registerWord('."', StartLiteral())
