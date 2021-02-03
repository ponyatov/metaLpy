## @file

from .number import *

## integer number
## @ingroup primitive
class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(int(V))
