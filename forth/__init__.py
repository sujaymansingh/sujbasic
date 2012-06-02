# Code for the forth interpreter!
#

__all__ = ['util', 'core', 'words_simple', 'words_arithmetic', 'words_double', 'words_strings', 'words_decision']

for submodule in __all__:
    # Just do a 'dummy' import of all non-util, non-core modules so that any modules that register words do so.
    if submodule == 'util' or submodule == 'core':
        continue

    # The __name__ of this module is probably forth, but it's dangerous to assume so :)
    __import__(__name__ + '.' + submodule)
