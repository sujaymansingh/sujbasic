#
#

class LineReader(object):

    def __init__(self):
        self.lines = []
        self.buffer = ''

    def write(self, s):
        for c in s:
            if (c == '\n'):
                self.lines.append(self.buffer)
                self.buffer = ''
            else:
                self.buffer = self.buffer + c

    def readline(self):
        line = self.lines[0]
        self.lines = self.lines[1:]
        return line
