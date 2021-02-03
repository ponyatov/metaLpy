## @file

from .object import *

## environment (binds variable names to its values)
## @ingroup core
class Env(Object):
    pass


env = Env('global')
env << env
env >> env
