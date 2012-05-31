import parser

if __name__ == '__main__':
    p = parser.BasicParser()

    t = p.parse('PRINT 5+3\n')
    print t
