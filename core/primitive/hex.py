## @file

from .integer import *

## machine hexadecimal number
## @ingroup primitive
class Hex(Integer):
    def __init__(self, V):
        super().__init__(V)
