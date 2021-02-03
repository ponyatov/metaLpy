## @file

from core.primitive import *
from .io import *

## @defgroup net net
## @brief networking
## @ingroup io
## @{

class Net(IO):
    pass

## IP address
class IP(Net):
    pass

## IP port
class Port(Net, Integer):
    def __init__(self, V):
        assert isinstance(V, int)
        assert V >= 0 and V <= 65535

## network protocol
class Protocol(Net):
    pass

## TCP/IP
class TCP(Protocol):
    pass

## UDP/IP
class UDP(Protocol):
    pass

## @}
