# Data Types!
#
#
class DataType(object):
    def convertTo(self, otherDataType):
        pass
class Integer(DataType):
    def convertTo(self, otherDataType):
        if type(otherDataType) == Integer:
            # Nothing to do or see here!
            return []
        elif type(otherDataType) == DoubleInteger:
            # If the existing int is 'n', then we want 'n 0' on the stack.
            return ['S>D']
        elif type(otherDataType) == Float:
            return ['S>D', 'D>F']
        elif type(otherDataType) == String:
            return ['TODO']
# end of Integer
class DoubleInteger(DataType):
    def convertTo(self, otherDataType):
        if type(otherDataType) == Integer:
            return ['D>S']
        elif type(otherDataType) == DoubleInteger:
            # Nothing to do or see here!
            return ['']
        elif type(otherDataType) == Float:
            return ['D>F']
        elif type(otherDataType) == String:
            return ['TODO']
# end of DoubleInteger
class Float(DataType):
    def convertTo(self, otherDataType):
        if type(otherDataType) == Integer:
            return ['F>D', 'D>S']
        elif type(otherDataType) == DoubleInteger:
            return ['F>D']
        elif type(otherDataType) == Float:
            # Nothing to do or see here!
            return []
        elif type(otherDataType) == String:
            return ['TODO']
# end of Float
class String(DataType):
    def convertTo(self, otherDataType):
        if type(otherDataType) == Integer:
            return ['TODO']
        elif type(otherDataType) == DoubleInteger:
            return ['TODO']
        elif type(otherDataType) == Float:
            return ['TODO']
        elif type(otherDataType) == String:
            # Nothing to do or see here!
            return []
# end of Float
