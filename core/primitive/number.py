
from .primitive import *

## floating point number
## @ingroup primitive
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(float(V))
