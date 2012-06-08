#
#


class OutputStatic(object):

    def __init__(self):
        self.headerBuffer = ''
        self.bodyBuffer   = ''

    def addHeaderCode(self, headerCode):
        self.headerBuffer += ' '.join(headerCode)
        self.headerBuffer += ' '
    # end of addHeaderCode

    def addBodyCode(self, bodyCode):
        self.bodyBuffer += ' '.join(bodyCode)
        self.bodyBuffer += ' '
    # end of addBodyCode

    def beginStatement(self):
        pass
    # end of beginStatement

    def endStatement(self):
        pass
    # end of endStatement

    def generateEntireCode(self):
        output = ''
        output += self.headerBuffer

        output += ': __PROGRAM '
        output += self.bodyBuffer
        output += '; '

        # Now run it and exit.
        output += '__PROGRAM BYE '
        return output
    # end of build
# end of OutputStatic
