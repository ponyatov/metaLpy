## @file

from .integer import *

## bit string
## @ingroup primitive
class Bin(Integer):
    def __init__(self, V):
        super().__init__(V)
